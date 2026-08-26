# CARE Berlin Action Watch

## Purpose

Keep the public CARE Club action router useful **today**, not merely correct when it was built.

The agent's job is to observe public sources and produce an evidence-backed change set. It is not a caseworker and must never autonomously decide whether a child/family deserves essential support.

## Daily checks

1. **Route health**
   - Are public help URLs still reachable?
   - Did addresses, phone numbers, opening times or eligibility instructions change?
   - Are distribution sites temporarily closed or not accepting new registrations?

2. **Capacity signals**
   - Look for explicit statements such as `no new registrations`, `closed`, `urgent volunteers needed`, `special donation needed`.
   - Classify as `ROUTE_OK`, `CAPACITY_WARNING`, `ROUTE_CLOSED`, `UNKNOWN`.

3. **Help opportunities**
   - Current volunteer needs.
   - Current food/sach donation needs.
   - Corporate volunteering opportunities.
   - Public family-service access changes.

4. **Funding opportunities**
   - New Berlin, federal, ESF+, foundation or corporate calls relevant to Food Guarantee, Family Guarantee or OpenWork.
   - Never count an application/call as committed funding.

5. **Gap detection**
   - Identify times/areas where current routes do not satisfy CARE guarantee invariants: same-day access, evening/weekend/holiday coverage, accessibility, medically necessary diet support.
   - Report gaps at system/area level. Never expose vulnerable household locations or identities.

## Output

For each changed item:

```text
source
observed_at
old_state
new_state
evidence
impact_on_router
recommended_action
confidence
human_review_required
```

## Action policy

### May do automatically

- propose source/route updates;
- flag stale content;
- produce a daily diff;
- rank non-sensitive outreach opportunities;
- draft partner/funder messages;
- prepare public aggregate impact reports from already verified receipts.

### Human review required

- change a critical emergency route;
- publish a new guarantee claim;
- contact a vulnerable person/family;
- publish case-level information;
- represent CARE as formally partnered with an organisation;
- commit money or sign a funding/employment agreement.

### Never do

- deny food/family support;
- determine fraud;
- make child-protection decisions;
- publish sensitive personal data;
- relabel another organisation's outcomes as CARE impact.

## Success metric

**No known stale/broken critical action route remains publicly presented as available after the next verification cycle.**
