const form = document.querySelector('#household-form');
const childrenList = document.querySelector('#children-list');
const resultContent = document.querySelector('#result-content');
const emptyState = document.querySelector('#empty-state');
const statusEl = document.querySelector('#webmcp-status');
const outputEl = document.querySelector('#tool-output');
const toolButtons = document.querySelector('#tool-buttons');
let latestResult = null;
let childCounter = 0;
const traceStore = new Map();
const localTools = new Map();

function addChild(age = 8) {
  childCounter += 1;
  const row = document.createElement('div');
  row.className = 'child-row';
  row.dataset.child = String(childCounter);
  row.innerHTML = `<label>Age <input type="number" min="0" max="30" value="${age}" aria-label="Child age"></label><button type="button" class="remove-child" aria-label="Remove child">×</button>`;
  row.querySelector('.remove-child').addEventListener('click', () => row.remove());
  childrenList.appendChild(row);
}

function householdFromForm() {
  const singleParent = form.elements.householdType.value === 'single';
  return {
    adults: singleParent ? 1 : 2,
    singleParent,
    children: [...childrenList.querySelectorAll('input')].map((input) => ({ age: Number(input.value) })),
    monthlyGrossIncome: Number(document.querySelector('#income').value),
    warmRent: Number(document.querySelector('#rent').value),
    receivesKindergeld: document.querySelector('#kindergeld').checked,
    city: 'Berlin'
  };
}

async function evaluate(household = householdFromForm()) {
  const response = await fetch('/api/evaluate', {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ household })
  });
  const result = await response.json();
  if (!response.ok || !result.ok) throw new Error(result.errors?.join(' ') || result.error || 'Evaluation failed');
  latestResult = result;
  traceStore.set(result.traceId, result);
  renderResult(result);
  return result;
}

function signalLabel(status) {
  return ({ known: 'known', potential: 'worth checking', check_officially: 'official check', not_prioritised: 'low signal', unlikely_from_demo_inputs: 'low signal', check: 'check' })[status] || status;
}

function renderResult(result) {
  emptyState.classList.add('hidden');
  resultContent.classList.remove('hidden');
  document.querySelector('#trace-badge').textContent = result.traceId;
  document.querySelector('#summary-headline').textContent = result.summary.headline;
  document.querySelector('#summary-boundary').textContent = result.boundary;

  document.querySelector('#benefit-cards').innerHTML = result.benefits.map((b) => `
    <article class="benefit-card">
      <div class="benefit-top"><h4>${b.title}</h4><span class="signal ${b.status}">${signalLabel(b.status)}</span></div>
      <div class="benefit-amount">${b.monthlyAmount == null ? '—' : `€${b.monthlyAmount}`} ${b.monthlyAmount != null ? '<small>/ month</small>' : ''}</div>
      <p>${b.note}</p>
      <a class="source-link" href="${b.source.url}" target="_blank" rel="noreferrer">Official source ↗</a>
    </article>`).join('');

  document.querySelector('#evidence-list').innerHTML = result.missingEvidence.map((item) => `
    <div class="stack-item"><strong>${item.label}</strong><p>${item.reason}</p></div>`).join('') || '<div class="stack-item"><p>No additional evidence flagged by this demo.</p></div>';

  document.querySelector('#next-steps').innerHTML = result.nextSteps.map((item) => `
    <div class="stack-item"><strong>${item.priority}. ${item.title}</strong><p>${item.why}</p>${item.url ? `<a href="${item.url}" target="_blank" rel="noreferrer">Open official service ↗</a>` : ''}</div>`).join('');

  document.querySelector('#trace-list').innerHTML = result.trace.map((item, index) => `
    <div class="trace-step"><span>${index + 1}</span><div><strong>${item.step}</strong><p>${item.outcome}</p></div></div>`).join('');
}

function compactResult(result) {
  return {
    traceId: result.traceId,
    policyVersion: result.policyVersion,
    headline: result.summary.headline,
    benefits: result.benefits.map(({ id, status, monthlyAmount, amountKind, note, source }) => ({ id, status, monthlyAmount, amountKind, note, source: source.url })),
    boundary: result.boundary
  };
}

async function ensureResult(input = {}) {
  if (input.traceId && traceStore.has(input.traceId)) return traceStore.get(input.traceId);
  if (input.household) return evaluate(input.household);
  if (latestResult) return latestResult;
  return evaluate();
}

const toolDefinitions = [
  {
    name: 'check_eligibility',
    title: 'Check family-benefit pathways',
    description: 'Check a German household against Benefit Bridge preliminary family-benefit gates. Use this for orientation only; it returns sources, uncertainty and never asserts a legal entitlement.',
    inputSchema: { type: 'object', properties: { household: { type: 'object', description: 'Household with adults, children ages, monthlyGrossIncome, warmRent and receivesKindergeld.' } }, required: ['household'], additionalProperties: false },
    annotations: { readOnlyHint: true },
    execute: async ({ household }) => compactResult(await evaluate(household))
  },
  {
    name: 'calculate_support',
    title: 'Calculate anchored support amounts',
    description: 'Return only amounts Benefit Bridge can justify from its pinned 2026 anchors, separating known amounts from maximum potential amounts and values that require an official calculator.',
    inputSchema: { type: 'object', properties: { household: { type: 'object' } }, required: ['household'], additionalProperties: false },
    annotations: { readOnlyHint: true },
    execute: async ({ household }) => {
      const r = await evaluate(household);
      return { traceId: r.traceId, summary: r.summary, amounts: r.benefits.map(({ id, monthlyAmount, amountKind, confidence }) => ({ id, monthlyAmount, amountKind, confidence })), boundary: r.boundary };
    }
  },
  {
    name: 'list_missing_evidence',
    title: 'List evidence to prepare',
    description: 'List the evidence categories flagged by the latest or supplied Benefit Bridge household evaluation. This does not upload or submit documents.',
    inputSchema: { type: 'object', properties: { traceId: { type: 'string' }, household: { type: 'object' } }, additionalProperties: false },
    annotations: { readOnlyHint: true },
    execute: async (input) => { const r = await ensureResult(input); return { traceId: r.traceId, missingEvidence: r.missingEvidence, boundary: r.boundary }; }
  },
  {
    name: 'explain_result',
    title: 'Explain a Benefit Bridge result',
    description: 'Explain why a Benefit Bridge result was produced using the stored rule trace and official-source anchors. Prefer this over inferring rationale from the visual page.',
    inputSchema: { type: 'object', properties: { traceId: { type: 'string' } }, required: ['traceId'], additionalProperties: false },
    annotations: { readOnlyHint: true },
    execute: async ({ traceId }) => {
      const r = traceStore.get(traceId);
      if (!r) return { error: 'Trace not found in this browser session.' };
      return { traceId, headline: r.summary.headline, explanation: r.trace, sources: r.benefits.map((b) => ({ benefit: b.title, url: b.source.url, fact: b.source.fact })), boundary: r.boundary };
    }
  },
  {
    name: 'prepare_next_steps',
    title: 'Prepare safe next steps',
    description: 'Return ordered, human-reviewable next actions and official service links for a Benefit Bridge trace. This tool cannot submit an application or act on the user’s behalf.',
    inputSchema: { type: 'object', properties: { traceId: { type: 'string' } }, required: ['traceId'], additionalProperties: false },
    annotations: { readOnlyHint: true },
    execute: async ({ traceId }) => {
      const r = traceStore.get(traceId);
      if (!r) return { error: 'Trace not found in this browser session.' };
      return { traceId, nextSteps: r.nextSteps, requiresHumanAction: true, boundary: r.boundary };
    }
  },
  {
    name: 'replay_case',
    title: 'Replay the evaluation trace',
    description: 'Replay the exact Benefit Bridge rule trace for a trace ID so a human or agent can inspect what inputs and deterministic steps produced the result.',
    inputSchema: { type: 'object', properties: { traceId: { type: 'string' } }, required: ['traceId'], additionalProperties: false },
    annotations: { readOnlyHint: true },
    execute: async ({ traceId }) => {
      const r = traceStore.get(traceId);
      if (!r) return { error: 'Trace not found in this browser session.' };
      return { traceId, policyVersion: r.policyVersion, household: r.household, trace: r.trace, result: compactResult(r) };
    }
  }
];

function installTestingShim() {
  if (document.modelContext) return false;
  const registry = new Map();
  Object.defineProperty(document, 'modelContext', { configurable: true, value: {
    async registerTool(definition, options = {}) {
      registry.set(definition.name, definition);
      options.signal?.addEventListener('abort', () => registry.delete(definition.name), { once: true });
    },
    async getTools() { return [...registry.values()].map(({ execute, ...rest }) => rest); },
    async executeTool(tool, inputJson) {
      const definition = registry.get(tool.name || tool);
      if (!definition) throw new Error('Tool not found');
      const input = typeof inputJson === 'string' ? JSON.parse(inputJson) : inputJson;
      return definition.execute(input || {});
    }
  }});
  return true;
}

async function registerWebMCP() {
  const shimmed = installTestingShim();
  const controller = new AbortController();
  for (const definition of toolDefinitions) {
    localTools.set(definition.name, definition);
    await document.modelContext.registerTool(definition, { signal: controller.signal });
  }
  statusEl.classList.add('ready');
  statusEl.innerHTML = `<span class="status-dot"></span>${shimmed ? 'WebMCP test shim · 6 tools' : 'WebMCP native · 6 tools'}`;
  renderToolButtons();
  return controller;
}

function renderToolButtons() {
  toolButtons.innerHTML = [...localTools.values()].map((tool) => `<button class="tool-button" data-tool="${tool.name}"><code>${tool.name}</code><span>run →</span></button>`).join('');
  toolButtons.querySelectorAll('button').forEach((button) => button.addEventListener('click', async () => {
    const tool = localTools.get(button.dataset.tool);
    if (!latestResult && !['check_eligibility', 'calculate_support'].includes(tool.name)) {
      outputEl.textContent = 'Run a household check first so this tool has a trace to inspect.';
      return;
    }
    const args = ['check_eligibility', 'calculate_support'].includes(tool.name)
      ? { household: householdFromForm() }
      : { traceId: latestResult.traceId };
    outputEl.textContent = 'Running…';
    try { outputEl.textContent = JSON.stringify(await tool.execute(args), null, 2); }
    catch (error) { outputEl.textContent = `Error: ${error.message}`; }
  }));
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const button = document.querySelector('#evaluate-button');
  button.disabled = true;
  button.firstElementChild.textContent = 'Checking…';
  try { await evaluate(); }
  catch (error) { alert(error.message); }
  finally { button.disabled = false; button.firstElementChild.textContent = 'Check support pathways'; }
});

document.querySelector('#add-child').addEventListener('click', () => addChild(6));
document.querySelector('#load-demo').addEventListener('click', () => {
  document.querySelector('input[name="householdType"][value="single"]').checked = true;
  document.querySelector('#income').value = 2000;
  document.querySelector('#rent').value = 1100;
  document.querySelector('#kindergeld').checked = true;
  childrenList.innerHTML = ''; childCounter = 0; addChild(7); addChild(12);
});

addChild(7); addChild(12);
registerWebMCP().catch((error) => {
  statusEl.textContent = `WebMCP registration failed: ${error.message}`;
  console.error(error);
});
