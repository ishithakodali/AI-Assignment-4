from __future__ import annotations

from typing import Dict, List, Set, Tuple

from csp_core import CSP, not_equal_constraint

import geopandas as gpd
import matplotlib.pyplot as plt


DISTRICTS: List[str] = [
    "adilabad", "bhadradri kothagudem", "hanumakonda", "hyderabad",
    "jagitial", "jangoan", "jayashankar", "jogulamba gadwal",
    "kamareddy", "karimnagar", "khammam", "kumuram bheem asifabad",
    "mahabubabad", "mahabubnagar", "mancherial", "medak",
    "medchal malkajgiri", "mulugu", "nagarkurnool", "nalgonda",
    "narayanpet", "nirmal", "nizamabad", "peddapalli",
    "rajanna sircilla", "rangareddy", "sangareddy", "siddipet",
    "suryapet", "vikarabad", "wanaparthy", "warangal",
    "yadadri bhuvanagiri",
]

COLORS: List[str] = ["Green", "Teal", "Indigo", "Pink"]

COLOR_MAP = {
    "Green": "#A8F08E",
    "Teal": "#c0fff4",
    "Indigo": "#a99adb",
    "Pink": "#ffb2cd",
}


# 🔥 FIXED ADJACENCY (complete + symmetric)
ADJACENCY: Dict[str, Set[str]] = {
    "adilabad": {"kumuram bheem asifabad", "mancherial", "nirmal"},
    "bhadradri kothagudem": {"khammam", "mulugu", "jayashankar"},
    "hanumakonda": {"jangoan", "karimnagar", "mahabubabad", "warangal", "jayashankar", "siddipet"},
    "hyderabad": {"medchal malkajgiri", "rangareddy", "sangareddy"},
    "jagitial": {"nirmal", "mancherial", "peddapalli", "rajanna sircilla", "karimnagar", "nizamabad"},
    "jangoan": {"yadadri bhuvanagiri", "siddipet", "hanumakonda", "mahabubabad", "suryapet", "warangal"},    "jayashankar": {"warangal", "hanumakonda", "karimnagar", "peddapalli", "mancherial", "mulugu", "bhadradri kothagudem"},
    "jogulamba gadwal": {"narayanpet", "wanaparthy", "nagarkurnool"},
    "kamareddy": {"nizamabad", "rajanna sircilla", "siddipet", "medak", "sangareddy", "nirmal"},
    "karimnagar": {"jagitial", "peddapalli", "rajanna sircilla", "siddipet", "hanumakonda", "jayashankar"},
    "khammam": {"suryapet", "mahabubabad", "bhadradri kothagudem"},
    "kumuram bheem asifabad": {"adilabad", "mancherial", "nirmal"},    "mahabubabad": {"jangoan", "hanumakonda", "warangal", "mulugu", "khammam", "suryapet"},
    "mahabubnagar": {"narayanpet", "vikarabad", "rangareddy", "wanaparthy", "nagarkurnool", "nalgonda"},
    "mancherial": {"kumuram bheem asifabad", "adilabad", "nirmal", "jagitial", "peddapalli", "jayashankar"},
    "medak": {"sangareddy", "siddipet", "kamareddy"},
    "medchal malkajgiri": {"hyderabad", "rangareddy", "sangareddy", "yadadri bhuvanagiri"},
    "mulugu": {"jayashankar", "warangal", "mahabubabad", "bhadradri kothagudem"},
    "nagarkurnool": {"mahabubnagar", "wanaparthy", "jogulamba gadwal", "nalgonda", "suryapet"},
    "nalgonda": {"rangareddy", "mahabubnagar", "nagarkurnool", "suryapet", "yadadri bhuvanagiri"},
    "narayanpet": {"vikarabad", "rangareddy", "mahabubnagar", "wanaparthy", "jogulamba gadwal"},
    "nirmal": {"adilabad", "mancherial", "jagitial", "nizamabad", "kamareddy", "kumuram bheem asifabad"},    "nizamabad": {"nirmal", "kamareddy", "jagitial"},
    "peddapalli": {"jagitial", "karimnagar", "jayashankar", "mancherial"},
    "rajanna sircilla": {"karimnagar", "jagitial", "kamareddy", "siddipet"},
    "rangareddy": {
        "hyderabad", "medchal malkajgiri", "vikarabad",
        "mahabubnagar", "narayanpet", "sangareddy",
        "nalgonda", "yadadri bhuvanagiri"
    },
    "sangareddy": {"medak", "vikarabad", "rangareddy", "medchal malkajgiri", "hyderabad", "siddipet", "kamareddy"},
    "siddipet": {"rajanna sircilla", "karimnagar", "medak", "yadadri bhuvanagiri", "jangoan", "hanumakonda", "sangareddy", "kamareddy"},
    "suryapet": {"nalgonda", "yadadri bhuvanagiri", "jangoan", "khammam", "mahabubabad", "nagarkurnool"},
    "vikarabad": {"sangareddy", "rangareddy", "mahabubnagar", "narayanpet"},
    "wanaparthy": {"narayanpet", "mahabubnagar", "nagarkurnool", "jogulamba gadwal"},
    "warangal": {"hanumakonda", "mahabubabad", "mulugu", "jayashankar", "jangoan"},    
    "yadadri bhuvanagiri": {
        "nalgonda", "suryapet", "jangoan",
        "siddipet", "medchal malkajgiri",
        "rangareddy"
    },
}


def _build_edges(adjacency: Dict[str, Set[str]]) -> List[Tuple[str, str]]:
    edges = set()
    for a, neighbors in adjacency.items():
        for b in neighbors:
            edges.add(tuple(sorted((a, b))))
    return list(edges)


def plot_telangana(solution):
    gdf = gpd.read_file("telangana_districts (1).geojson")

    name_col = None
    for col in gdf.columns:
        if col.lower() in ["district", "name", "dtname"]:
            name_col = col
            break

    gdf[name_col] = gdf[name_col].str.lower()

    gdf["color"] = gdf[name_col].map(solution)
    gdf["color"] = gdf["color"].map(COLOR_MAP).fillna("#CCCCCC")

    fig, ax = plt.subplots(figsize=(8, 8))
    gdf.plot(color=gdf["color"], edgecolor="black", ax=ax)

    for _, row in gdf.iterrows():
        centroid = row.geometry.centroid
        ax.text(centroid.x, centroid.y, row[name_col], fontsize=5, ha="center")

    plt.title("Telangana Map Coloring (CSP)")
    plt.axis("off")
    plt.savefig("telangana_map.png")
    plt.show()


def solve_telangana_map_coloring() -> Dict[str, str]:
    edges = _build_edges(ADJACENCY)

    domains = {d: COLORS[:] for d in DISTRICTS}
    csp = CSP(DISTRICTS, domains)

    for a, b in edges:
        csp.add_constraint((a, b), not_equal_constraint(a, b))

    solution = csp.backtracking_search()
    if solution is None:
        raise RuntimeError("No solution found")

    solution = {k: solution[k] for k in DISTRICTS}

    plot_telangana(solution)

    return solution


def validate_telangana_solution(solution: Dict[str, str]) -> bool:
    for a, b in _build_edges(ADJACENCY):
        if solution[a] == solution[b]:
            return False
    return True