from __future__ import annotations

from typing import Dict, List, Sequence, Tuple

from csp_core import CSP, all_different_constraint

ROWS = "ABCDEFGHI"
COLS = "123456789"
DIGITS = "123456789"

DEFAULT_PUZZLE: List[str] = [
    "003020600",
    "900305001",
    "001806400",
    "008102900",
    "700000008",
    "006708200",
    "002609500",
    "800203009",
    "005010300",
]


def _cell_name(r: int, c: int) -> str:
    return f"{ROWS[r]}{COLS[c]}"


def parse_puzzle(lines: Sequence[str]) -> List[List[int]]:
    if len(lines) != 9:
        raise ValueError("Sudoku puzzle must have exactly 9 rows.")

    grid: List[List[int]] = []
    for row in lines:
        if len(row) != 9:
            raise ValueError("Each Sudoku row must have exactly 9 characters.")
        if not all(ch in "0123456789" for ch in row):
            raise ValueError("Sudoku rows must contain digits only (0 for blank).")
        grid.append([int(ch) for ch in row])

    return grid


def _sudoku_units() -> List[Tuple[str, ...]]:
    units: List[Tuple[str, ...]] = []

    for r in range(9):
        units.append(tuple(_cell_name(r, c) for c in range(9)))

    for c in range(9):
        units.append(tuple(_cell_name(r, c) for r in range(9)))

    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            unit = []
            for r in range(br, br + 3):
                for c in range(bc, bc + 3):
                    unit.append(_cell_name(r, c))
            units.append(tuple(unit))

    return units


def solve_sudoku(puzzle_lines: Sequence[str]) -> List[List[int]]:
    grid = parse_puzzle(puzzle_lines)
    variables = [_cell_name(r, c) for r in range(9) for c in range(9)]

    domains: Dict[str, List[int]] = {}
    for r in range(9):
        for c in range(9):
            name = _cell_name(r, c)
            value = grid[r][c]
            domains[name] = [value] if value != 0 else [int(d) for d in DIGITS]

    csp = CSP(variables=variables, domains=domains)

    for unit in _sudoku_units():
        csp.add_constraint(unit, all_different_constraint(unit), name="all_diff")

    solution = csp.backtracking_search()
    if solution is None:
        raise RuntimeError("No Sudoku solution exists for the provided puzzle.")

    solved_grid = [[int(solution[_cell_name(r, c)]) for c in range(9)] for r in range(9)]
    if not validate_sudoku(solved_grid):
        raise RuntimeError("Sudoku solver returned an invalid solution.")

    return solved_grid


def validate_sudoku(grid: List[List[int]]) -> bool:
    target = set(range(1, 10))

    for row in grid:
        if set(row) != target:
            return False

    for c in range(9):
        if {grid[r][c] for r in range(9)} != target:
            return False

    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            block = {
                grid[r][c]
                for r in range(br, br + 3)
                for c in range(bc, bc + 3)
            }
            if block != target:
                return False

    return True


def format_grid(grid: List[List[int]]) -> str:
    lines: List[str] = []
    for r, row in enumerate(grid):
        if r in {3, 6}:
            lines.append("------+-------+------")

        chunks = [" ".join(str(n) for n in row[i : i + 3]) for i in range(0, 9, 3)]
        lines.append(" | ".join(chunks))

    return "\n".join(lines)
