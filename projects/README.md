# Independent learning labs

These small, dependency-free labs make two hard concepts reproducible without paid APIs. **They are not n8n integrations or production services.** Run from the repository root. Use synthetic data only.

## Lab 1 — durable intake and transactional outbox

**Runtime:** Python 3.10+ with its standard-library SQLite support.

**Invariant:** a new `(source, event_id)` creates one receipt and one delivery intent in the same local transaction. Reusing an identity with different content raises `Conflict`. A worker may update a leased job only with the current, unexpired token.

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
```

Worked experiment:

```python
from projects.durable_intake import connect, receive, claim, ack

db = connect(':memory:')
print(receive(db, 'form', 'event-1', {'name': 'Synthetic'}))  # True
print(receive(db, 'form', 'event-1', {'name': 'Synthetic'}))  # False
first = claim(db, now=0, lease_seconds=10)
print(claim(db, now=9))                                    # None
# Simulate a crash: intentionally do not acknowledge the first delivery.
second = claim(db, now=10, lease_seconds=10)
print(first['id'] == second['id'])                         # True
print(ack(db, first['id'], first['token'], now=11))         # False
print(ack(db, second['id'], second['token'], now=11))       # True
print(claim(db, now=100))                                  # None
db.close()
```

### Failure experiments and expected evidence

| Experiment | Expected evidence | What it does not prove |
| --- | --- | --- |
| Eight concurrent duplicate receives | One newly created receipt/intent | Single external effect |
| Reuse identity with different payload | Conflict; original data unchanged | Source authenticity |
| Abort outbox insertion | Receipt insert also rolls back | Distributed transaction |
| Reopen the database file | Pending intent remains available | Host/disk disaster recovery |
| Worker dies without ack | Reclaim after lease expiry | External request was not sent |
| Old worker tries ack/retry | Old token is rejected | Old external effect was prevented |
| Retry with delay | Intent is unavailable until that time | Automatic retry policy or dead-letter handling |

The code does **not** call an external destination. A crash after external success but before ack permits repeat delivery: downstream idempotency, fencing where applicable, or reconciliation remains necessary. `source` must be derived from trusted authentication, not arbitrary user JSON. The serialization is Python-local, not a cross-language signature standard. Payload quotas, authentication, migrations, monitoring, backup, retention, automatic attempt caps, dead-letter handling, WAL tuning and deployment hardening are deliberately out of scope. SQLite here is not n8n Queue mode configuration.

**Exercise:** add a maximum-attempt policy and an inspectable terminal state. Write tests for the last allowed attempt, exhausted jobs, authorized replay and stale-worker rejection. Do not silently discard a failed intent.

## Lab 2 — AI trust boundaries and tool approval

**Runtime:** Node.js 20+. No model, embedding service, MCP server, vector database or identity provider is connected.

```bash
node --test tests/ai_boundary.test.mjs
```

```bash
node --input-type=module <<'JS'
import { parseClassification, proposalDigest, authorizeTool } from './projects/ai_boundary.mjs';
console.log(parseClassification('{"category":"technical","needsHuman":true,"summary":"Review required"}'));
const proposal = {
  tool: 'send_support_reply', tenant: 'demo', recipient: 'support@example.test',
  body: 'Synthetic draft', requestId: 'request-1'
};
// Trusted server-side fixtures, NOT objects accepted from an anonymous request.
const context = { tenant: 'demo', allowedRecipients: ['support@example.test'], reviewers: ['reviewer-1'] };
const approval = { decision: 'approve', digest: proposalDigest(proposal), reviewer: 'reviewer-1', expiresAt: 100 };
console.log(authorizeTool(proposal, approval, context, 1).requestId); // request-1
try {
  authorizeTool({ ...proposal, body: 'Changed after approval' }, approval, context, 1);
} catch { console.log('changed proposal denied'); }
JS
```

### Boundaries under test

1. **Untrusted model output:** bounded JSON parsing, exact keys, enum/type/length checks. Valid JSON alone is not permission.
2. **Document eligibility:** tenant, group scope and deletion state are checked before documents may enter context. This is a synthetic predicate, not a vector-search implementation.
3. **Tool scope:** fixed tool, server-derived tenant and allowed recipient list.
4. **Approval binding:** exact proposal digest, authorized reviewer and expiry. A changed body or request identity needs a new approval.

A hash is **not** a signature or authenticated approval. Context and approval must come from trusted authentication, authorization and audit systems. This pure function does not validate identity tokens, consume approval atomically, prevent one approval from being checked repeatedly, enforce one-time execution or send the reply. Real delivery still needs durable state, downstream idempotency and failure handling. Do not expose it directly as an authorization endpoint accepting caller-supplied context.

**Exercise:** implement an authenticated approval store and atomic proposal consumption in a separate test application. Test concurrent execution, expired approvals, changed parameters and crashes after delivery. Keep identity, policy and delivery guarantees distinct.

## Evidence and publication

The repository currently includes 12 Python tests for durable intake, 12 Node.js tests for the AI boundary and 10 existing Node.js tests for lead validation/workflow structure. Passing these **34 independent tests** is not evidence of workflow import, Docker startup, external-provider integration, load capacity or production readiness. Those require their own tests in the target environment.
