from __future__ import annotations

from typing import Dict, List, Tuple

from csp_core import CSP, not_equal_constraint

REGIONS: List[str] = ["WA", "NT", "Q", "SA", "NSW", "V", "T"]
COLORS: List[str] = ["Red", "Green", "Blue", "Yellow"]
EDGES: List[Tuple[str, str]] = [
    ("WA", "NT"),
    ("WA", "SA"),
    ("NT", "SA"),
    ("NT", "Q"),
    ("Q", "SA"),
    ("Q", "NSW"),
    ("SA", "NSW"),
    ("SA", "V"),
    ("NSW", "V"),
]


def solve_australia_map_coloring() -> Dict[str, str]:
    domains = {region: COLORS for region in REGIONS}
    csp = CSP(variables=REGIONS, domains=domains)

    for a, b in EDGES:
        csp.add_constraint((a, b), not_equal_constraint(a, b), name=f"{a}!={b}")

    solution = csp.backtracking_search()
    if solution is None:
        raise RuntimeError("No solution found for Australia map coloring CSP.")

    return {region: str(solution[region]) for region in REGIONS}


def validate_australia_solution(solution: Dict[str, str]) -> bool:
    if set(solution.keys()) != set(REGIONS):
        return False

    for a, b in EDGES:
        if solution[a] == solution[b]:
            return False

    return True
