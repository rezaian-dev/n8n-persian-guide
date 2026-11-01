import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
const code = readFileSync(new URL('../examples/normalize-lead.js', import.meta.url), 'utf8');
const run = bodies => new Function('$input', code)({all: () => bodies.map(body => ({json: {body}}))});
const good = {eventId: 'evt-001', name: 'کاربر آزمایشی', email: ' DEMO@Example.com '};
test('normalizes a valid lead; explicitly does not persist it', () => {
 const [out] = run([good]); assert.equal(out.json.statusCode, 200);
 assert.equal(out.json.response.lead.email, 'demo@example.com');
 assert.equal(out.json.response.persisted, false);
});
test('rejects malformed email', () => assert.equal(run([{...good, email:'bad'}])[0].json.statusCode,422));
test('rejects missing input', () => assert.equal(run([undefined])[0].json.statusCode,422));
test('rejects array input', () => assert.equal(run([[good]])[0].json.statusCode,422));
test('does not coerce objects to strings', () => assert.equal(run([{...good,name:{}}])[0].json.statusCode,422));
test('rejects oversized fields', () => assert.equal(run([{...good,name:'x'.repeat(101)}])[0].json.statusCode,422));
test('rejects unsafe event IDs', () => assert.equal(run([{...good,eventId:'../../secret'}])[0].json.statusCode,422));
test('drops unknown fields', () => assert.equal(run([{...good,password:'not-a-real-secret'}])[0].json.response.lead.password,undefined));
test('retains one-to-one item linkage', () => {
 const out=run([good,{...good,eventId:'evt-002'}]);assert.equal(out.length,2);
 assert.deepEqual(out[1].pairedItem,{item:1});
});
test('workflow code and graph match source', () => {
 const w=JSON.parse(readFileSync(new URL('../workflows/lead-intake.json',import.meta.url),'utf8'));
 assert.equal(w.active,false); assert.deepEqual(w.pinData,{});
 assert.equal(w.nodes.find(n=>n.type==='n8n-nodes-base.code').parameters.jsCode,code);
 const names=new Set(w.nodes.map(n=>n.name));
 for(const [source,links] of Object.entries(w.connections)) {
  assert.ok(names.has(source)); for(const group of links.main) for(const edge of group) assert.ok(names.has(edge.node));
 }
 assert.ok(w.nodes.every(n=>!n.credentials));
});
