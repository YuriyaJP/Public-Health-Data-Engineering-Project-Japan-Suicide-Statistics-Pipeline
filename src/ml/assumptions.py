# assumptions.py

"""
Assumptions module for economic modeling of suicide impact in Japan.

All assumptions should be documented when used in analyses or visualizations.
Sources (salary data): GaijinPot, A-Realty salary breakdown by age groups
    https://blog.gaijinpot.com/what-is-the-average-salary-in-japan/  (2025)
    https://arealty.jp/blog/average-salary-in-japan-a-2025/  (2025)
"""

# -----------------------------------------------------------------------------
# Salary assumptions (average annual earnings by age bracket, in JPY)
# -----------------------------------------------------------------------------
# These approximate typical wage patterns in Japan, peaking in mid-career.
SALARY_BY_AGE = {
    '0-9': 0,          # no workforce participation
    '10-19': 1_500_000,  # part-time or early earnings
    '20-29': 3_000_000,
    '30-39': 4_000_000,
    '40-49': 5_000_000,
    '50-59': 6_000_000,
    '60-69': 3_000_000,
    '70-79': 2_500_000,
    '80+': 2_500_000,
}

# -----------------------------------------------------------------------------
# Expected working life remaining assumptions by age bracket (years)
# -----------------------------------------------------------------------------
# Simplified remaining years in workforce.
WORK_YEARS_LEFT = {
    '0-9': 45,    # assume potential life years until 65
    '10-19': 40,
    '20-29': 35,
    '30-39': 25,
    '40-49': 15,
    '50-59': 7,
    '60-69': 3,
    '70-79': 0,
    '80+': 0,
}

# -----------------------------------------------------------------------------
# Policy scenario assumptions
# -----------------------------------------------------------------------------
# Example reduction in suicide incidence from intervention
SUICIDE_REDUCTION_RATE = 0.15  # 15% reduction

# Hypothetical annual intervention costs (policy/program spend) by age
INTERVENTION_COST_BY_AGE = {
    '0-9': 1_000_000_000,
    '10-19': 3_000_000_000,
    '20-29': 5_000_000_000,
    '30-39': 5_000_000_000,
    '40-49': 4_000_000_000,
    '50-59': 3_000_000_000,
    '60-69': 2_000_000_000,
    '70-79': 1_000_000_000,
    '80+': 500_000_000,
}

# -----------------------------------------------------------------------------
# Functions for policy scenario losses
# -----------------------------------------------------------------------------
def baseline_loss(annual_loss_yen: float) -> float:
    """Return baseline loss without intervention."""
    return annual_loss_yen

def reduced_loss(annual_loss_yen: float) -> float:
    """Return expected loss after policy intervention."""
    return annual_loss_yen * (1 - SUICIDE_REDUCTION_RATE)