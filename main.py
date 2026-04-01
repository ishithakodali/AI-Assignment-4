from __future__ import annotations

import argparse
from typing import List

from cryptarithmetic_two_two_four import format_crypt_solution, solve_two_two_four
from map_coloring_australia import solve_australia_map_coloring, validate_australia_solution
from map_coloring_telangana import solve_telangana_map_coloring, validate_telangana_solution
from sudoku_csp import DEFAULT_PUZZLE, format_grid, solve_sudoku


def _print_map_solution(title: str, solution: dict[str, str]) -> None:
    print(title)
    for region in sorted(solution):
        print(f"  {region:25s} -> {solution[region]}")
    print()


def run_australia() -> None:
    solution = solve_australia_map_coloring()
    if not validate_australia_solution(solution):
        raise RuntimeError("Australia solution failed validation.")

    _print_map_solution("Australia Map Coloring (WA, NT, Q, SA, NSW, V, T)", solution)


def run_telangana() -> None:
    solution = solve_telangana_map_coloring()
    if not validate_telangana_solution(solution):
        raise RuntimeError("Telangana solution failed validation.")

    _print_map_solution("Telangana 33-District Map Coloring", solution)


def run_sudoku(sudoku_lines: List[str]) -> None:
    solved = solve_sudoku(sudoku_lines)
    print("Sudoku CSP Solution")
    print(format_grid(solved))
    print()


def run_crypt() -> None:
    solution = solve_two_two_four()
    print("Cryptarithmetic CSP (TWO + TWO = FOUR)")
    print(format_crypt_solution(solution))
    print()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CSP assignment runner")
    parser.add_argument(
        "--problem",
        choices=["australia", "telangana", "sudoku", "crypt", "all"],
        default="all",
        help="Select which CSP problem to run.",
    )
    parser.add_argument(
        "--sudoku",
        nargs=9,
        metavar="ROW",
        help="Optional Sudoku input as 9 rows of 9 digits (0 means blank).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    sudoku_input = args.sudoku if args.sudoku else DEFAULT_PUZZLE

    if args.problem in {"australia", "all"}:
        run_australia()
    if args.problem in {"telangana", "all"}:
        run_telangana()
    if args.problem in {"sudoku", "all"}:
        run_sudoku(sudoku_input)
    if args.problem in {"crypt", "all"}:
        run_crypt()


if __name__ == "__main__":
    main()
