import crypto from 'node:crypto';

export const POLICY_VERSION = 'DE-2026-08-27-demo';

export const SOURCES = {
  kindergeld: {
    label: 'Bundesagentur für Arbeit — Kindergeld 2026',
    url: 'https://www.arbeitsagentur.de/news/kindergeld-steigt-2026',
    fact: '€259 per eligible child per month from January 2026.'
  },
  kiz: {
    label: 'Bundesagentur für Arbeit — Kinderzuschlag',
    url: 'https://www.arbeitsagentur.de/familie-und-kinder/kinderzuschlag-verstehen/kinderzuschlag-anspruch-hoehe-dauer',
    fact: 'Up to €297 per child per month; minimum gross income €600 for single parents and €900 for couples.'
  },
  wohngeld: {
    label: 'Bundesministerium — Wohngeld',
    url: 'https://www.bmwsb.bund.de/wohngeld',
    fact: 'Eligibility depends on household size, income, rent and local rent level; this demo does not reproduce the official calculation.'
  }
};

function number(value, fallback = 0) {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : fallback;
}

export function normalizeHousehold(raw = {}) {
  const children = Array.isArray(raw.children)
    ? raw.children.map((child, index) => ({
        id: child?.id || `child-${index + 1}`,
        age: Math.max(0, Math.round(number(child?.age, 0)))
      }))
    : [];

  const adults = Math.min(2, Math.max(1, Math.round(number(raw.adults, raw.singleParent ? 1 : 2))));
  const singleParent = raw.singleParent === true || adults === 1;

  return {
    adults,
    singleParent,
    children,
    monthlyGrossIncome: Math.max(0, number(raw.monthlyGrossIncome)),
    warmRent: Math.max(0, number(raw.warmRent)),
    receivesKindergeld: raw.receivesKindergeld !== false,
    city: String(raw.city || 'Berlin').slice(0, 120)
  };
}

export function validateHousehold(household) {
  const errors = [];
  if (!household.children.length) errors.push('Add at least one child for this family-benefit demo.');
  if (household.children.some((c) => c.age > 30)) errors.push('Child ages must be realistic.');
  if (household.monthlyGrossIncome > 100000) errors.push('Monthly gross income is outside the supported demo range.');
  if (household.warmRent > 20000) errors.push('Warm rent is outside the supported demo range.');
  return errors;
}

function traceIdFor(household) {
  const stable = JSON.stringify(household);
  return `bb_${crypto.createHash('sha256').update(stable).digest('hex').slice(0, 10)}`;
}

export function evaluateHousehold(raw = {}) {
  const household = normalizeHousehold(raw);
  const errors = validateHousehold(household);
  if (errors.length) {
    return { ok: false, policyVersion: POLICY_VERSION, errors };
  }

  const eligibleKindergeldChildren = household.children.filter((c) => c.age < 18);
  const kindergeldMonthly = household.receivesKindergeld ? eligibleKindergeldChildren.length * 259 : 0;

  const kizChildren = household.children.filter((c) => c.age < 25);
  const kizMinimumIncome = household.singleParent ? 600 : 900;
  const kizPassesIncomeFloor = household.monthlyGrossIncome >= kizMinimumIncome;
  const kizPotential = household.receivesKindergeld && kizChildren.length > 0 && kizPassesIncomeFloor;
  const kizMaxMonthly = kizPotential ? kizChildren.length * 297 : 0;

  const rentShare = household.monthlyGrossIncome > 0
    ? household.warmRent / household.monthlyGrossIncome
    : household.warmRent > 0 ? 1 : 0;
  const wohngeldSignal = household.warmRent > 0 && (rentShare >= 0.25 || household.monthlyGrossIncome <= 3500);

  const missingEvidence = [];
  if (household.receivesKindergeld) {
    missingEvidence.push({ id: 'children', label: 'Child / household details', reason: 'Needed to verify family-benefit eligibility.' });
  }
  if (kizPotential) {
    missingEvidence.push(
      { id: 'income', label: 'Recent income evidence', reason: 'KiZ depends on household income.' },
      { id: 'housing', label: 'Rent and housing-cost evidence', reason: 'Housing costs affect the full family calculation.' }
    );
  }
  if (wohngeldSignal) {
    missingEvidence.push({ id: 'wohngeld', label: 'Income + rent details for official Wohngeld check', reason: 'The official calculation is more detailed than this demo.' });
  }

  const benefits = [
    {
      id: 'kindergeld',
      title: 'Kindergeld',
      status: household.receivesKindergeld && eligibleKindergeldChildren.length ? 'known' : 'check',
      monthlyAmount: kindergeldMonthly,
      amountKind: 'deterministic_anchor',
      confidence: household.receivesKindergeld ? 'high' : 'medium',
      note: household.receivesKindergeld
        ? `${eligibleKindergeldChildren.length} child${eligibleKindergeldChildren.length === 1 ? '' : 'ren'} × €259.`
        : 'Marked as not currently received; verify eligibility with Familienkasse.',
      source: SOURCES.kindergeld
    },
    {
      id: 'kiz',
      title: 'Kinderzuschlag (KiZ)',
      status: kizPotential ? 'potential' : 'unlikely_from_demo_inputs',
      monthlyAmount: kizMaxMonthly,
      amountKind: 'maximum_potential_not_entitlement',
      confidence: 'medium',
      note: kizPotential
        ? `Preliminary gate passed. Up to €${kizMaxMonthly}/month across ${kizChildren.length} child${kizChildren.length === 1 ? '' : 'ren'}; actual KiZ requires the official calculation.`
        : `Preliminary gate not passed in this demo. Minimum gross-income floor used: €${kizMinimumIncome}/month.`,
      source: SOURCES.kiz
    },
    {
      id: 'wohngeld',
      title: 'Wohngeld',
      status: wohngeldSignal ? 'check_officially' : 'not_prioritised',
      monthlyAmount: null,
      amountKind: 'not_calculated',
      confidence: 'low',
      note: wohngeldSignal
        ? 'Worth an official check. This prototype deliberately does not reproduce the statutory Wohngeld formula.'
        : 'Not prioritised by the demo heuristic; an official check can still be appropriate.',
      source: SOURCES.wohngeld
    }
  ];

  const knownMonthly = benefits
    .filter((b) => b.amountKind === 'deterministic_anchor')
    .reduce((sum, b) => sum + (b.monthlyAmount || 0), 0);

  const potentialAdditionalMax = benefits
    .filter((b) => b.amountKind === 'maximum_potential_not_entitlement')
    .reduce((sum, b) => sum + (b.monthlyAmount || 0), 0);

  const nextSteps = [
    ...(kizPotential ? [{
      priority: 1,
      title: 'Run the official KiZ check',
      why: 'The preliminary income/family gate passed; the exact amount needs the Familienkasse calculation.',
      url: 'https://www.kinderzuschlag.de/'
    }] : []),
    ...(wohngeldSignal ? [{
      priority: 2,
      title: 'Check Wohngeld with the official service',
      why: 'Rent and income suggest it is worth checking; this demo refuses to guess the statutory amount.',
      url: 'https://www.bmwsb.bund.de/wohngeld'
    }] : []),
    {
      priority: 3,
      title: 'Collect the evidence once',
      why: 'Income, rent and household details recur across benefit applications. Benefit Bridge keeps the checklist visible instead of asking an agent to infer it.'
    }
  ].sort((a, b) => a.priority - b.priority);

  const trace = [
    { step: 'normalize', outcome: 'Household input normalized.' },
    { step: 'kindergeld_anchor', outcome: `Applied €259 × ${eligibleKindergeldChildren.length} eligible child(ren).` },
    { step: 'kiz_precheck', outcome: `Applied €${kizMinimumIncome} minimum-income gate and €297/child maximum anchor.` },
    { step: 'wohngeld_boundary', outcome: 'Heuristic only; exact statutory calculation intentionally delegated to official service.' },
    { step: 'human_boundary', outcome: 'No application was submitted and no legal entitlement was asserted.' }
  ];

  return {
    ok: true,
    traceId: traceIdFor(household),
    policyVersion: POLICY_VERSION,
    generatedAt: new Date().toISOString(),
    household,
    summary: {
      knownMonthly,
      potentialAdditionalMax,
      headline: potentialAdditionalMax
        ? `€${knownMonthly}/month known + up to €${potentialAdditionalMax}/month worth checking`
        : `€${knownMonthly}/month known from the demo inputs`
    },
    benefits,
    missingEvidence,
    nextSteps,
    trace,
    boundary: 'Prototype orientation only. Not a benefits decision, legal advice, or substitute for the responsible authority.'
  };
}
