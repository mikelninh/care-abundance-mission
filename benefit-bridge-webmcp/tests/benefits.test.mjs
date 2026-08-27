import test from 'node:test';
import assert from 'node:assert/strict';
import { evaluateHousehold, normalizeHousehold } from '../lib/benefits.mjs';

test('single parent Berlin example exposes anchors without pretending KiZ is exact', () => {
  const result = evaluateHousehold({
    adults: 1,
    children: [{ age: 7 }, { age: 12 }],
    monthlyGrossIncome: 2000,
    warmRent: 1100,
    receivesKindergeld: true
  });
  assert.equal(result.ok, true);
  assert.equal(result.summary.knownMonthly, 518);
  assert.equal(result.summary.potentialAdditionalMax, 594);
  assert.equal(result.benefits.find((b) => b.id === 'kiz').amountKind, 'maximum_potential_not_entitlement');
  assert.equal(result.benefits.find((b) => b.id === 'wohngeld').monthlyAmount, null);
});

test('KiZ precheck uses the official minimum-income floor', () => {
  const low = evaluateHousehold({ adults: 1, children: [{ age: 5 }], monthlyGrossIncome: 500, warmRent: 700, receivesKindergeld: true });
  assert.equal(low.benefits.find((b) => b.id === 'kiz').status, 'unlikely_from_demo_inputs');

  const pass = evaluateHousehold({ adults: 1, children: [{ age: 5 }], monthlyGrossIncome: 600, warmRent: 700, receivesKindergeld: true });
  assert.equal(pass.benefits.find((b) => b.id === 'kiz').status, 'potential');
});

test('normalization clamps unsupported values and infers single parent from one adult', () => {
  const h = normalizeHousehold({ adults: 1, monthlyGrossIncome: '2000', children: [{ age: '8' }] });
  assert.equal(h.singleParent, true);
  assert.equal(h.monthlyGrossIncome, 2000);
  assert.equal(h.children[0].age, 8);
});

test('invalid household is rejected deterministically', () => {
  const result = evaluateHousehold({ adults: 1, children: [], monthlyGrossIncome: 1200 });
  assert.equal(result.ok, false);
  assert.ok(result.errors.length > 0);
});

test('same household yields stable trace id', () => {
  const input = { adults: 2, children: [{ age: 3 }], monthlyGrossIncome: 1800, warmRent: 800, receivesKindergeld: true };
  assert.equal(evaluateHousehold(input).traceId, evaluateHousehold(input).traceId);
});
