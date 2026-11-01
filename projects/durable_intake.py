"""Isolated SQLite teaching lab; not an n8n integration or production queue.

Receipt and outbox intent are atomic locally. Delivery is at-least-once: a
crash after external delivery but before ack can repeat that delivery.
Caller supplies time to make lease behavior deterministic in tests.
"""
import hashlib
import json
import math
import sqlite3
import uuid


class Conflict(ValueError):
    """An existing event identity was reused with different content."""


def _text(value, name):
    if not isinstance(value, str) or not value.strip() or len(value) > 200:
        raise ValueError(f"invalid {name}")
    return value


def _time(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
        raise ValueError("invalid clock value")
    return value


def connect(path):
    db = sqlite3.connect(path, timeout=5, isolation_level=None)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    db.executescript("""
        CREATE TABLE IF NOT EXISTS receipts (
            source TEXT NOT NULL, event_id TEXT NOT NULL,
            fingerprint TEXT NOT NULL, payload TEXT NOT NULL,
            PRIMARY KEY (source, event_id)
        );
        CREATE TABLE IF NOT EXISTS outbox (
            id INTEGER PRIMARY KEY,
            source TEXT NOT NULL, event_id TEXT NOT NULL,
            state TEXT NOT NULL DEFAULT 'pending'
                CHECK (state IN ('pending', 'leased', 'done')),
            attempts INTEGER NOT NULL DEFAULT 0,
            available_at REAL NOT NULL DEFAULT 0,
            lease_until REAL, token TEXT,
            UNIQUE (source, event_id),
            FOREIGN KEY (source, event_id) REFERENCES receipts(source, event_id)
        );
    """)
    return db


def receive(db, source, event_id, payload):
    """source must come from an authenticated server-side context.

    Canonicalization is deliberately Python-local, not an interoperable JSON
    signing standard. Only object payloads containing JSON values are allowed.
    """
    _text(source, "source")
    _text(event_id, "event_id")
    if not isinstance(payload, dict):
        raise ValueError("object payload required")
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    digest = hashlib.sha256(raw.encode()).hexdigest()
    db.execute("BEGIN IMMEDIATE")
    try:
        old = db.execute("SELECT fingerprint FROM receipts WHERE source=? AND event_id=?", (source, event_id)).fetchone()
        if old:
            if old["fingerprint"] != digest:
                raise Conflict("event identity reused with different payload")
            created = False
        else:
            db.execute("INSERT INTO receipts VALUES (?,?,?,?)", (source, event_id, digest, raw))
            db.execute("INSERT INTO outbox(source,event_id) VALUES (?,?)", (source, event_id))
            created = True
        db.execute("COMMIT")
        return created
    except BaseException:
        db.execute("ROLLBACK")
        raise


def claim(db, now, lease_seconds=30):
    _time(now)
    _time(lease_seconds)
    if lease_seconds == 0:
        raise ValueError("positive lease required")
    db.execute("BEGIN IMMEDIATE")
    try:
        row = db.execute("""SELECT o.id, o.source, o.event_id, r.payload FROM outbox o
            JOIN receipts r USING(source,event_id)
            WHERE (o.state='pending' AND o.available_at<=?)
               OR (o.state='leased' AND o.lease_until<=?)
            ORDER BY o.id LIMIT 1""", (now, now)).fetchone()
        if row is None:
            db.execute("COMMIT")
            return None
        token = uuid.uuid4().hex
        db.execute("UPDATE outbox SET state='leased',token=?,lease_until=?,attempts=attempts+1 WHERE id=?",
                   (token, now + lease_seconds, row["id"]))
        db.execute("COMMIT")
        return {**dict(row), "token": token, "payload": json.loads(row["payload"])}
    except BaseException:
        db.execute("ROLLBACK")
        raise


def ack(db, job_id, token, now):
    _time(now)
    return db.execute("""UPDATE outbox SET state='done', token=NULL, lease_until=NULL
        WHERE id=? AND state='leased' AND token=? AND lease_until>?""",
        (job_id, token, now)).rowcount == 1


def retry(db, job_id, token, now, delay):
    _time(now)
    _time(delay)
    return db.execute("""UPDATE outbox SET state='pending', token=NULL, lease_until=NULL, available_at=?
        WHERE id=? AND state='leased' AND token=? AND lease_until>?""",
        (now + delay, job_id, token, now)).rowcount == 1
