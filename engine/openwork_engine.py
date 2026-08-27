from dataclasses import dataclass, field
from typing import List, Literal

FundingState = Literal["RED", "YELLOW", "GREEN"]

@dataclass(frozen=True)
class FundingSource:
    name: str
    amount: float
    binding: bool
    liquid_now: bool
    notes: str = ""

@dataclass
class Mission:
    name: str
    hours: float
    hourly_wage: float = 20.0
    employer_cost_rate: float = 0.25
    training_cost: float = 0.0
    supervision_cost: float = 0.0
    equipment_admin_cost: float = 0.0
    contingency_rate: float = 0.05
    funding_sources: List[FundingSource] = field(default_factory=list)

    @property
    def gross_wages(self): return round(self.hours * self.hourly_wage, 2)
    @property
    def employer_costs(self): return round(self.gross_wages * self.employer_cost_rate, 2)
    @property
    def base_cost(self): return round(self.gross_wages + self.employer_costs + self.training_cost + self.supervision_cost + self.equipment_admin_cost, 2)
    @property
    def fully_loaded_cost(self): return round(self.base_cost * (1 + self.contingency_rate), 2)
    @property
    def binding_funding(self): return round(sum(s.amount for s in self.funding_sources if s.binding), 2)
    @property
    def liquid_binding_funding(self): return round(sum(s.amount for s in self.funding_sources if s.binding and s.liquid_now), 2)
    @property
    def funding_gap(self): return round(max(0.0, self.fully_loaded_cost - self.binding_funding), 2)
    @property
    def liquidity_gap(self): return round(max(0.0, self.fully_loaded_cost - self.liquid_binding_funding), 2)
    @property
    def state(self) -> FundingState:
        if self.binding_funding >= self.fully_loaded_cost and self.liquid_binding_funding >= self.fully_loaded_cost:
            return "GREEN"
        if self.funding_sources:
            return "YELLOW"
        return "RED"
    @property
    def startable(self): return self.state == "GREEN"

def job_transition_required(*, paid_hours: float, recurring_weeks: float) -> bool:
    return paid_hours >= 120 or recurring_weeks >= 12

def qualification_path(*, regulated: bool, productive_sample: bool) -> dict:
    if regulated:
        return {"allowed": False, "reason": "Statutory/professional credential required before OpenWork skill unlock."}
    return {"allowed": True, "steps": ["learn", "scenario_check", "sample", "unlock", "paid_work"], "sample_must_be_paid": productive_sample}
