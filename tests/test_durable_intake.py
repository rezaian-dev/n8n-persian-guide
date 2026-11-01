import concurrent.futures
import tempfile
import unittest
from pathlib import Path
from projects.durable_intake import connect, receive, claim, ack, retry, Conflict


class DurableIntakeTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.path = Path(self.directory.name) / 'lab.sqlite'
        self.db = connect(self.path)

    def tearDown(self):
        self.db.close()
        self.directory.cleanup()

    def seed(self):
        return receive(self.db, 'form', 'evt-1', {'name': 'test'})

    def test_duplicate_is_one_intent(self):
        self.assertTrue(self.seed())
        self.assertFalse(self.seed())
        self.assertEqual(self.db.execute('select count(*) from outbox').fetchone()[0], 1)

    def test_conflict_keeps_original(self):
        self.seed()
        with self.assertRaises(Conflict):
            receive(self.db, 'form', 'evt-1', {'name': 'different'})
        self.assertEqual(claim(self.db, 0)['payload'], {'name': 'test'})

    def test_source_namespace(self):
        self.seed()
        receive(self.db, 'other', 'evt-1', {'name': 'test'})
        self.assertEqual(self.db.execute('select count(*) from receipts').fetchone()[0], 2)

    def test_receipt_rollback_if_outbox_insert_fails(self):
        self.db.execute("CREATE TRIGGER fail_insert BEFORE INSERT ON outbox BEGIN SELECT RAISE(ABORT, 'injected'); END")
        with self.assertRaises(Exception):
            self.seed()
        self.assertEqual(self.db.execute('select count(*) from receipts').fetchone()[0], 0)

    def test_claim_exclusive_until_expiry(self):
        self.seed()
        self.assertIsNotNone(claim(self.db, 10))
        self.assertIsNone(claim(self.db, 11))

    def test_reclaim_stale_ack_rejected(self):
        self.seed()
        old = claim(self.db, 0, 10)
        new = claim(self.db, 10, 10)
        self.assertNotEqual(old['token'], new['token'])
        self.assertFalse(ack(self.db, old['id'], old['token'], 11))
        self.assertTrue(ack(self.db, new['id'], new['token'], 11))
        self.assertIsNone(claim(self.db, 100))

    def test_expired_ack_rejected_even_before_reclaim(self):
        self.seed()
        job = claim(self.db, 0, 10)
        self.assertFalse(ack(self.db, job['id'], job['token'], 10))

    def test_retry_delay_and_stale_retry(self):
        self.seed()
        job = claim(self.db, 0)
        self.assertTrue(retry(self.db, job['id'], job['token'], 1, 10))
        self.assertFalse(retry(self.db, job['id'], job['token'], 2, 10))
        self.assertIsNone(claim(self.db, 10))
        self.assertIsNotNone(claim(self.db, 11))

    def test_reopen_preserves_intent(self):
        self.seed()
        self.db.close()
        self.db = connect(self.path)
        self.assertIsNotNone(claim(self.db, 0))

    def test_concurrent_receive(self):
        def attempt(_):
            db = connect(self.path)
            try:
                return receive(db, 'form', 'evt-1', {'name': 'test'})
            finally:
                db.close()
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            self.assertEqual(sum(pool.map(attempt, range(8))), 1)

    def test_unknown_external_result_can_repeat_delivery(self):
        self.seed()
        first = claim(self.db, 0, 10)
        # External call happened; worker dies before ack. No exactly-once claim.
        second = claim(self.db, 10, 10)
        self.assertEqual(first['id'], second['id'])
        self.assertEqual(self.db.execute('select attempts from outbox').fetchone()[0], 2)

    def test_invalid_clock_and_payload(self):
        with self.assertRaises(ValueError):
            claim(self.db, float('nan'))
        with self.assertRaises(ValueError):
            receive(self.db, '', 'event', {})
        with self.assertRaises(ValueError):
            receive(self.db, 'form', 'event', {'bad': float('nan')})


if __name__ == '__main__':
    unittest.main()
