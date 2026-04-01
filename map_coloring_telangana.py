from __future__ import annotations

from typing import Dict, List, Set, Tuple

from csp_core import CSP, not_equal_constraint

DISTRICTS: List[str] = [
    "Adilabad",
    "Bhadradri Kothagudem",
    "Hanamkonda",
    "Hyderabad",
    "Jagtial",
    "Jangaon",
    "Jayashankar Bhupalpally",
    "Jogulamba Gadwal",
    "Kamareddy",
    "Karimnagar",
    "Khammam",
    "Komaram Bheem Asifabad",
    "Mahabubabad",
    "Mahabubnagar",
    "Mancherial",
    "Medak",
    "Medchal Malkajgiri",
    "Mulugu",
    "Nagarkurnool",
    "Nalgonda",
    "Narayanpet",
    "Nirmal",
    "Nizamabad",
    "Peddapalli",
    "Rajanna Sircilla",
    "Rangareddy",
    "Sangareddy",
    "Siddipet",
    "Suryapet",
    "Vikarabad",
    "Wanaparthy",
    "Warangal",
    "Yadadri Bhuvanagiri",
]

COLORS: List[str] = ["Saffron", "Teal", "Indigo", "Maroon"]

ADJACENCY: Dict[str, Set[str]] = {
    "Adilabad": {"Komaram Bheem Asifabad", "Mancherial", "Nirmal"},
    "Bhadradri Kothagudem": {"Khammam", "Mulugu", "Jayashankar Bhupalpally"},
    "Hanamkonda": {"Jangaon", "Karimnagar", "Mahabubabad", "Warangal", "Jayashankar Bhupalpally", "Siddipet"},
    "Hyderabad": {"Medchal Malkajgiri", "Rangareddy", "Sangareddy"},
    "Jagtial": {"Nirmal", "Mancherial", "Peddapalli", "Rajanna Sircilla", "Karimnagar", "Nizamabad"},
    "Jangaon": {"Yadadri Bhuvanagiri", "Siddipet", "Hanamkonda", "Mahabubabad", "Suryapet"},
    "Jayashankar Bhupalpally": {"Warangal", "Hanamkonda", "Karimnagar", "Peddapalli", "Mancherial", "Mulugu", "Bhadradri Kothagudem"},
    "Jogulamba Gadwal": {"Narayanpet", "Wanaparthy", "Nagarkurnool"},
    "Kamareddy": {"Nizamabad", "Rajanna Sircilla", "Siddipet", "Medak", "Sangareddy", "Nirmal"},
    "Karimnagar": {"Jagtial", "Peddapalli", "Rajanna Sircilla", "Siddipet", "Hanamkonda", "Jayashankar Bhupalpally"},
    "Khammam": {"Suryapet", "Mahabubabad", "Bhadradri Kothagudem"},
    "Komaram Bheem Asifabad": {"Adilabad", "Mancherial"},
    "Mahabubabad": {"Jangaon", "Hanamkonda", "Warangal", "Mulugu", "Khammam", "Suryapet"},
    "Mahabubnagar": {"Narayanpet", "Vikarabad", "Rangareddy", "Wanaparthy", "Nagarkurnool", "Nalgonda"},
    "Mancherial": {"Komaram Bheem Asifabad", "Adilabad", "Nirmal", "Jagtial", "Peddapalli", "Jayashankar Bhupalpally"},
    "Medak": {"Sangareddy", "Siddipet", "Kamareddy"},
    "Medchal Malkajgiri": {"Hyderabad", "Rangareddy", "Sangareddy", "Yadadri Bhuvanagiri"},
    "Mulugu": {"Jayashankar Bhupalpally", "Warangal", "Mahabubabad", "Bhadradri Kothagudem"},
    "Nagarkurnool": {"Mahabubnagar", "Wanaparthy", "Jogulamba Gadwal", "Nalgonda", "Suryapet"},
    "Nalgonda": {"Rangareddy", "Mahabubnagar", "Nagarkurnool", "Suryapet", "Yadadri Bhuvanagiri"},
    "Narayanpet": {"Vikarabad", "Rangareddy", "Mahabubnagar", "Wanaparthy", "Jogulamba Gadwal"},
    "Nirmal": {"Adilabad", "Mancherial", "Jagtial", "Nizamabad", "Kamareddy"},
    "Nizamabad": {"Nirmal", "Kamareddy", "Jagtial"},
    "Peddapalli": {"Jagtial", "Karimnagar", "Jayashankar Bhupalpally", "Mancherial"},
    "Rajanna Sircilla": {"Karimnagar", "Jagtial", "Kamareddy", "Siddipet"},
    "Rangareddy": {"Hyderabad", "Medchal Malkajgiri", "Vikarabad", "Mahabubnagar", "Narayanpet", "Sangareddy", "Nalgonda"},
    "Sangareddy": {"Medak", "Vikarabad", "Rangareddy", "Medchal Malkajgiri", "Hyderabad", "Siddipet", "Kamareddy"},
    "Siddipet": {"Rajanna Sircilla", "Karimnagar", "Medak", "Yadadri Bhuvanagiri", "Jangaon", "Hanamkonda", "Sangareddy", "Kamareddy"},
    "Suryapet": {"Nalgonda", "Yadadri Bhuvanagiri", "Jangaon", "Khammam", "Mahabubabad", "Nagarkurnool"},
    "Vikarabad": {"Sangareddy", "Rangareddy", "Mahabubnagar", "Narayanpet"},
    "Wanaparthy": {"Narayanpet", "Mahabubnagar", "Nagarkurnool", "Jogulamba Gadwal"},
    "Warangal": {"Hanamkonda", "Mahabubabad", "Mulugu", "Jayashankar Bhupalpally"},
    "Yadadri Bhuvanagiri": {"Nalgonda", "Suryapet", "Jangaon", "Siddipet", "Medchal Malkajgiri"},
}


def _build_edges(adjacency: Dict[str, Set[str]]) -> List[Tuple[str, str]]:
    edges: Set[Tuple[str, str]] = set()

    for district, neighbors in adjacency.items():
        if district not in DISTRICTS:
            raise ValueError(f"Unknown district in adjacency map: {district}")

        for neighbor in neighbors:
            if neighbor not in DISTRICTS:
                raise ValueError(f"Unknown district referenced in adjacency map: {neighbor}")
            edge = tuple(sorted((district, neighbor)))
            edges.add(edge)

    return sorted(edges)


def solve_telangana_map_coloring() -> Dict[str, str]:
    if set(DISTRICTS) != set(ADJACENCY.keys()):
        missing = sorted(set(DISTRICTS) - set(ADJACENCY.keys()))
        extra = sorted(set(ADJACENCY.keys()) - set(DISTRICTS))
        raise ValueError(f"Adjacency coverage mismatch. Missing={missing}, Extra={extra}")

    edges = _build_edges(ADJACENCY)
    domains = {district: COLORS for district in DISTRICTS}
    csp = CSP(variables=DISTRICTS, domains=domains)

    for a, b in edges:
        csp.add_constraint((a, b), not_equal_constraint(a, b), name=f"{a}!={b}")

    solution = csp.backtracking_search()
    if solution is None:
        raise RuntimeError("No solution found for Telangana map coloring CSP.")

    return {district: str(solution[district]) for district in sorted(DISTRICTS)}


def validate_telangana_solution(solution: Dict[str, str]) -> bool:
    if set(solution.keys()) != set(DISTRICTS):
        return False

    for a, b in _build_edges(ADJACENCY):
        if solution[a] == solution[b]:
            return False

    return True
