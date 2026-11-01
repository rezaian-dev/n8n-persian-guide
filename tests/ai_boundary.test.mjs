import test from 'node:test';
import assert from 'node:assert/strict';
import { parseClassification, eligibleDocuments, proposalDigest, authorizeTool } from '../projects/ai_boundary.mjs';
const valid = { category: 'technical', needsHuman: true, summary: 'Needs review' };
const proposal = { tool: 'send_support_reply', tenant: 'a', recipient: 'support@example.test', body: 'Draft', requestId: 'r-1' };
const context = { tenant: 'a', allowedRecipients: ['support@example.test'], reviewers: ['reviewer-1'] };
const approval = () => ({ decision: 'approve', digest: proposalDigest(proposal), reviewer: 'reviewer-1', expiresAt: 100 });

test('strict classification accepts valid bounded output', () => {
  assert.deepEqual(parseClassification(JSON.stringify(valid)), valid);
});
test('classification rejects invalid syntax, fences and trailing text', () => {
  for (const raw of ['bad', '```json\n{}\n```', JSON.stringify(valid) + ' done']) assert.throws(() => parseClassification(raw));
});
test('classification rejects unknown fields and wrong enum/type', () => {
  for (const value of [{ ...valid, tool: 'send' }, { ...valid, category: 'admin' }, { ...valid, needsHuman: 'true' }, { ...valid, summary: '' }, { ...valid, summary: 'x'.repeat(501) }, null, []]) assert.throws(() => parseClassification(JSON.stringify(value)));
});
test('classification limits raw output size', () => assert.throws(() => parseClassification(' '.repeat(4097))));
test('ACL removes cross-tenant, deleted, missing and disallowed groups', () => {
  const rows = [
    { id: 1, tenant: 'a', deleted: false, groups: ['support'] },
    { id: 2, tenant: 'b', deleted: false, groups: ['support'] },
    { id: 3, tenant: 'a', deleted: true, groups: ['support'] },
    { id: 4, tenant: 'a', deleted: false, groups: ['finance'] },
    { id: 5, tenant: 'a', groups: ['support'] }
  ];
  assert.deepEqual(eligibleDocuments(rows, { tenant: 'a', groups: ['support'] }).map(r => r.id), [1]);
  assert.deepEqual(eligibleDocuments(rows, { tenant: 'a', groups: [] }), []);
});
test('ACL requires trusted-shaped context', () => assert.throws(() => eligibleDocuments([], { tenant: '', groups: [] })));
test('approval accepts exact proposal in allowed scope', () => assert.deepEqual(authorizeTool(proposal, approval(), context, 1), proposal));
test('changed body or request identity invalidates approval', () => {
  assert.throws(() => authorizeTool({ ...proposal, body: 'Changed' }, approval(), context, 1));
  assert.throws(() => authorizeTool({ ...proposal, requestId: 'r-2' }, approval(), context, 1));
});
test('unapproved recipient and tenant are denied', () => {
  assert.throws(() => authorizeTool({ ...proposal, recipient: 'elsewhere@example.test' }, approval(), context, 1));
  assert.throws(() => authorizeTool({ ...proposal, tenant: 'b' }, approval(), context, 1));
});
test('denied, expired and unauthorized reviewer approvals fail closed', () => {
  for (const patch of [{ decision: 'deny' }, { expiresAt: 1 }, { reviewer: 'stranger' }, { expiresAt: Infinity }]) assert.throws(() => authorizeTool(proposal, { ...approval(), ...patch }, context, 1));
});
test('extra proposal fields and arbitrary tools rejected', () => {
  assert.throws(() => proposalDigest({ ...proposal, tool: 'http_anywhere' }));
  assert.throws(() => proposalDigest({ ...proposal, extra: true }));
});
test('digest has explicit field order', () => assert.equal(proposalDigest({ ...proposal }), proposalDigest(Object.fromEntries(Object.entries(proposal).reverse()))));
