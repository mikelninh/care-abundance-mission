import { evaluateHousehold } from '../lib/benefits.mjs';

const result = evaluateHousehold({
  adults: 1,
  singleParent: true,
  children: [{ age: 7 }, { age: 12 }],
  monthlyGrossIncome: 2000,
  warmRent: 1100,
  receivesKindergeld: true,
  city: 'Berlin'
});

if (!result.ok) throw new Error('Smoke case failed');
if (result.summary.knownMonthly !== 518) throw new Error(`Expected €518 known, got ${result.summary.knownMonthly}`);
if (result.summary.potentialAdditionalMax !== 594) throw new Error(`Expected €594 KiZ max, got ${result.summary.potentialAdditionalMax}`);
if (!result.traceId.startsWith('bb_')) throw new Error('Missing trace id');
console.log(JSON.stringify({ ok: true, headline: result.summary.headline, traceId: result.traceId }, null, 2));
