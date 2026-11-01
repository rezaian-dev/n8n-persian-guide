/** Isolated deterministic policy lab. No model, vector DB, identity provider,
 * MCP server, n8n runtime or external tool is called here.
 */
import { createHash } from 'node:crypto';

const object = value => value !== null && typeof value === 'object' && !Array.isArray(value);
const keysAre = (value, keys) => object(value) && Object.keys(value).length === keys.length && keys.every(key => Object.hasOwn(value, key));

export function parseClassification(raw) {
  if (typeof raw !== 'string' || raw.length > 4096) throw new TypeError('bounded JSON string required');
  const value = JSON.parse(raw);
  if (!keysAre(value, ['category', 'needsHuman', 'summary']) ||
      !['billing', 'technical', 'other'].includes(value.category) ||
      typeof value.needsHuman !== 'boolean' ||
      typeof value.summary !== 'string' || !value.summary.trim() || value.summary.length > 500) {
    throw new TypeError('classification schema violation');
  }
  return Object.freeze(value);
}

/** context MUST be supplied by trusted authentication/authorization middleware,
 * never copied from a request body or model output. Rows come from a trusted DB.
 */
export function eligibleDocuments(rows, context) {
  if (!object(context) || typeof context.tenant !== 'string' || !context.tenant ||
      !Array.isArray(context.groups) || context.groups.some(g => typeof g !== 'string')) {
    throw new TypeError('trusted context required');
  }
  return rows.filter(row => row.tenant === context.tenant && row.deleted === false &&
    Array.isArray(row.groups) && row.groups.some(group => context.groups.includes(group)));
}

function proposalBytes(proposal) {
  if (!keysAre(proposal, ['tool', 'tenant', 'recipient', 'body', 'requestId']) ||
      proposal.tool !== 'send_support_reply' ||
      ['tenant', 'recipient', 'body', 'requestId'].some(k => typeof proposal[k] !== 'string' || !proposal[k].trim()) ||
      proposal.body.length > 2000 || proposal.recipient.length > 254 || proposal.tenant.length > 200 || proposal.requestId.length > 200) {
    throw new TypeError('invalid proposal');
  }
  // Explicit field ordering avoids generic object-order canonicalization.
  return JSON.stringify([proposal.tool, proposal.tenant, proposal.recipient, proposal.body, proposal.requestId]);
}

export function proposalDigest(proposal) {
  return createHash('sha256').update(proposalBytes(proposal)).digest('hex');
}

/** approval MUST be loaded from a trusted audit/approval store. A digest is NOT
 * a signature and a caller-supplied reviewer name is NOT authentication.
 * This pure check does not consume an approval or guarantee one-time execution.
 */
export function authorizeTool(proposal, approval, context, now) {
  const digest = proposalDigest(proposal);
  if (!Number.isFinite(now) || !object(context) || typeof context.tenant !== 'string' ||
      !Array.isArray(context.allowedRecipients) || !Array.isArray(context.reviewers) ||
      proposal.tenant !== context.tenant || !context.allowedRecipients.includes(proposal.recipient)) {
    throw new Error('tool scope denied');
  }
  if (!object(approval) || approval.decision !== 'approve' || approval.digest !== digest ||
      !context.reviewers.includes(approval.reviewer) || !Number.isFinite(approval.expiresAt) ||
      approval.expiresAt <= now) throw new Error('valid matching approval required');
  return Object.freeze({ ...proposal });
}
