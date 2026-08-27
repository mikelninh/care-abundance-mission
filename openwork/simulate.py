import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.openwork_engine import FundingSource, Mission, job_transition_required, qualification_path


def pack(name, m):
    return {
        'scenario': name,
        'cost': m.fully_loaded_cost,
        'binding': m.binding_funding,
        'liquid': m.liquid_binding_funding,
        'state': m.state,
        'startable': m.startable,
    }


def run():
    scenarios = [
        pack(
            'submitted grant',
            Mission(
                'Community docs',
                100,
                funding_sources=[FundingSource('grant application', 10000, False, False)],
            ),
        ),
        pack(
            'approved but illiquid',
            Mission(
                'Accessibility',
                100,
                funding_sources=[FundingSource('approved reimbursement', 10000, True, False)],
            ),
        ),
        pack(
            'fully funded and liquid',
            Mission(
                'Digital helper',
                100,
                training_cost=300,
                supervision_cost=500,
                funding_sources=[FundingSource('reserved payroll pool', 10000, True, True)],
            ),
        ),
        {'scenario': 'regulated work', **qualification_path(regulated=True, productive_sample=False)},
        {'scenario': 'productive sample', **qualification_path(regulated=False, productive_sample=True)},
        {
            'scenario': 'recurring work',
            'job_transition_required': job_transition_required(paid_hours=120, recurring_weeks=8),
        },
    ]

    assert scenarios[0]['state'] != 'GREEN'
    assert scenarios[0]['startable'] is False
    assert scenarios[1]['state'] != 'GREEN'
    assert scenarios[1]['startable'] is False
    assert scenarios[2]['state'] == 'GREEN'
    assert scenarios[2]['startable'] is True
    assert scenarios[3]['allowed'] is False
    assert scenarios[4]['sample_must_be_paid'] is True
    assert scenarios[5]['job_transition_required'] is True
    return scenarios


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, ensure_ascii=False))
    print('OPENWORK_E2E=PASS')
