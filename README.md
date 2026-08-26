# CARE — Germany Abundance Mission

**Produce more. Make essentials abundant. Give people ownership. Prove that value reached them.**

> **Promise != delivery. Verified receipt = delivery.**

## Highest priority: OpenWork

> **Work is funded → you can start.**

OpenWork is the work/income layer of CARE. It turns unmet public and social needs into **fully funded, fairly paid employment**:

`Need → Fund → Qualify → Contract → Work → Verify → Pay → Employ`

### Hard rules

- no GREEN/startable mission until 100% of fully loaded employment cost has **binding funding and payroll liquidity**;
- **€20 gross/hour OpenWork Fair Floor or higher applicable tariff** — a product standard, not a current universal legal entitlement;
- `Learn → Check → Prove → Unlock → Paid Work` for non-regulated tasks;
- regulated work still requires the legally necessary credential;
- productive sample work is paid;
- at **120 paid hours or 12 weeks recurring demand**, trigger a job-transition review;
- grants/subsidies may only be stacked where their rules allow it;
- submitted applications are never guaranteed money.

### V0 now includes

- [`openwork/index.html`](openwork/index.html) interactive worker/funding prototype;
- [`engine/openwork_engine.py`](engine/openwork_engine.py) deterministic funding guarantee engine;
- [`tests/test_openwork.py`](tests/test_openwork.py) guarantee invariants + 200 synthetic funding stress cases;
- [`openwork/simulate.py`](openwork/simulate.py) end-to-end failure/success scenarios;
- [`docs/OPENWORK.md`](docs/OPENWORK.md) operating model;
- [`docs/OPENWORK_WORKFLOWS.md`](docs/OPENWORK_WORKFLOWS.md) stakeholder workflows;
- [`docs/OPENWORK_SOURCES.md`](docs/OPENWORK_SOURCES.md) verified programme facts vs product rules;
- [`data/openwork_funding_sources.json`](data/openwork_funding_sources.json) starter funding registry;
- [`agents/openwork_funding_watch.md`](agents/openwork_funding_watch.md) funding watch specification;
- GitHub Actions proof workflow.

### The V1 promise

> **If a mission is GREEN, the contractual gross wage at or above the OpenWork Fair Floor is fully funded and payroll liquidity is reserved before the person starts.**

OpenWork does **not** yet claim a universal legal right to a €20/hour job, a guaranteed net wage, automatic grant stacking, or a live employer/payroll service.

## CARE ecosystem

| Product | Core question |
|---|---|
| **OpenWork** | What useful work needs doing, who can do it, and is fair pay guaranteed before start? |
| **CARE** | What does this person deserve, and did they actually receive it? |
| **Abundance Engine** | How can Germany produce dramatically more real value? |
| **Policy Proof** | What does a proposal mean for a household in euros, duration and funding? |
| **Growth Corridors** | Where can Germany create additional wealth through international cooperation? |

Expanded chain:

`Produce → Fund Useful Work → Pay People → Deliver → Verify → Grow`

## Run

Open `openwork/index.html` for the OpenWork prototype.

```bash
python -m pytest -q tests/test_openwork.py
python openwork/simulate.py
```

## Build order

1. **OpenWork 100 Berlin:** validate three real mission families and their actual funding stacks.
2. Secure one employer/payroll partner and one bridge-liquidity mechanism.
3. Turn one real need into a genuinely GREEN mission before recruiting workers.
4. Run the first person through skill check → contract → paid work → evidence → payroll.
5. Scale to 10, then 100 workers; measure pay, quality and conversion into regular jobs.
6. Continue CARE household/Policy Proof and national abundance work in parallel.

See [`ROADMAP.md`](ROADMAP.md).

**Bake more cake. Give everyone a stake in the bakery. Show the receipts.**
