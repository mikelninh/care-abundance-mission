"""Rights-safe agentic public-service proof.

The module demonstrates a narrow operating contract for agentic assistance in
public administration. The agent may orient, prepare, explain and coordinate.
It may not make binding entitlement decisions, submit consequential actions
without explicit confirmation, or silently erase the provenance of an action.
"""

from dataclasses import dataclass, field
from typing import Dict, Tuple


ALLOWED_ROLES = (
    "ORIENTATION",
    "APPLICATION_PREP",
    "PROCEDURE",
    "COMMUNICATION",
    "ORCHESTRATION",
    "MONITORING",
)


@dataclass(frozen=True)
class PlannedAction:
    action_id: str
    role: str
    label: str
    impact: str  # INFORM, PREPARE, SUBMIT, DECIDE, AGGREGATE
    source: str
    explanation: str


@dataclass(frozen=True)
class ActionReceipt:
    action_id: str
    outcome: str
    role: str
    source: str
    confirmed_by_user: bool
    explanation: str


@dataclass
class RightsSafeAgent:
    receipts: list[ActionReceipt] = field(default_factory=list)

    def plan_for_life_event(self, life_event: str) -> Tuple[PlannedAction, ...]:
        event = life_event.strip().lower()
        if not event:
            raise ValueError("life_event is required")

        # Synthetic service names keep this proof independent of live legal rules.
        return (
            PlannedAction(
                "orient-1",
                "ORIENTATION",
                "Map life event to possible public services",
                "INFORM",
                "versioned-service-catalog",
                "Creates options, not an eligibility decision.",
            ),
            PlannedAction(
                "prepare-1",
                "APPLICATION_PREP",
                "Prepare a reusable facts-and-evidence packet",
                "PREPARE",
                "citizen-approved-evidence",
                "Collect once; show missing facts before any submission.",
            ),
            PlannedAction(
                "procedure-1",
                "PROCEDURE",
                "Explain current status, deadlines and next required step",
                "INFORM",
                "procedure-status-feed",
                "Status explanation remains distinguishable from a legal decision.",
            ),
            PlannedAction(
                "communicate-1",
                "COMMUNICATION",
                "Translate an authority request into plain language",
                "INFORM",
                "authority-message",
                "Preserves the original message and identifies the explanation layer.",
            ),
            PlannedAction(
                "orchestrate-1",
                "ORCHESTRATION",
                "Prepare cross-agency hand-off package",
                "PREPARE",
                "service-routing-registry",
                "Coordinates steps without inventing authority or silently submitting.",
            ),
            PlannedAction(
                "monitor-1",
                "MONITORING",
                "Aggregate bottlenecks without taking action against individuals",
                "AGGREGATE",
                "de-identified-process-events",
                "Monitoring is systemic; it is not an enforcement score for a person.",
            ),
        )

    def execute(self, action: PlannedAction, confirmed: bool = False) -> ActionReceipt:
        if action.role not in ALLOWED_ROLES:
            raise ValueError("unknown agent role")

        if action.impact == "DECIDE":
            return self._record(action, "BLOCKED_BINDING_DECISION", confirmed)

        if action.impact == "SUBMIT" and not confirmed:
            return self._record(action, "AWAITING_EXPLICIT_CONFIRMATION", False)

        if action.impact == "AGGREGATE" and action.role != "MONITORING":
            return self._record(action, "BLOCKED_ROLE_MISMATCH", confirmed)

        return self._record(action, "EXECUTED", confirmed)

    def _record(
        self, action: PlannedAction, outcome: str, confirmed: bool
    ) -> ActionReceipt:
        receipt = ActionReceipt(
            action_id=action.action_id,
            outcome=outcome,
            role=action.role,
            source=action.source,
            confirmed_by_user=confirmed,
            explanation=action.explanation,
        )
        self.receipts.append(receipt)
        return receipt


def consequential_submit_action() -> PlannedAction:
    return PlannedAction(
        "submit-demo",
        "APPLICATION_PREP",
        "Submit prepared application",
        "SUBMIT",
        "citizen-approved-application",
        "Consequential external action requires explicit user confirmation.",
    )


def forbidden_decision_action() -> PlannedAction:
    return PlannedAction(
        "decision-demo",
        "ORCHESTRATION",
        "Decide legal entitlement",
        "DECIDE",
        "none",
        "Binding entitlement decisions are outside this agent's authority.",
    )
