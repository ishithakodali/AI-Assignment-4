from __future__ import annotations

from typing import Dict, List

from csp_core import CSP, all_different_constraint

LETTERS = ["T", "W", "O", "F", "U", "R"]
CARRIES = ["C1", "C2", "C3"]


def solve_two_two_four() -> Dict[str, int]:
    variables = LETTERS + CARRIES
    domains = {letter: list(range(10)) for letter in LETTERS}
    domains["F"] = [1]
    domains.update({carry: [0, 1] for carry in CARRIES})

    csp = CSP(variables=variables, domains=domains)

    csp.add_constraint(LETTERS, all_different_constraint(LETTERS), name="letters_all_diff")

    csp.add_constraint(["T"], lambda a: ("T" not in a) or a["T"] != 0, name="T_non_zero")

    # O + O = R + 10*C1
    csp.add_constraint(
        ["O", "R", "C1"],
        lambda a: ("O" not in a or "R" not in a or "C1" not in a)
        or (a["O"] + a["O"] == a["R"] + 10 * a["C1"]),
        name="col_ones",
    )

    # W + W + C1 = U + 10*C2
    csp.add_constraint(
        ["W", "C1", "U", "C2"],
        lambda a: ("W" not in a or "C1" not in a or "U" not in a or "C2" not in a)
        or (a["W"] + a["W"] + a["C1"] == a["U"] + 10 * a["C2"]),
        name="col_tens",
    )

    # T + T + C2 = O + 10*C3
    csp.add_constraint(
        ["T", "C2", "O", "C3"],
        lambda a: ("T" not in a or "C2" not in a or "O" not in a or "C3" not in a)
        or (a["T"] + a["T"] + a["C2"] == a["O"] + 10 * a["C3"]),
        name="col_hundreds",
    )

    # Leftmost carry forms F.
    csp.add_constraint(
        ["C3", "F"],
        lambda a: ("C3" not in a or "F" not in a) or (a["C3"] == a["F"]),
        name="col_thousands",
    )

    solution = csp.backtracking_search()
    if solution is None:
        raise RuntimeError("No solution found for TWO + TWO = FOUR.")

    typed_solution = {k: int(v) for k, v in solution.items()}
    if not validate_two_two_four(typed_solution):
        raise RuntimeError("Solver returned invalid TWO + TWO = FOUR assignment.")

    return typed_solution


def evaluate_words(solution: Dict[str, int]) -> Dict[str, int]:
    two = 100 * solution["T"] + 10 * solution["W"] + solution["O"]
    four = 1000 * solution["F"] + 100 * solution["O"] + 10 * solution["U"] + solution["R"]
    return {"TWO": two, "FOUR": four}


def validate_two_two_four(solution: Dict[str, int]) -> bool:
    if solution["T"] == 0 or solution["F"] == 0:
        return False

    letter_values = [solution[letter] for letter in LETTERS]
    if len(set(letter_values)) != len(letter_values):
        return False

    values = evaluate_words(solution)
    return values["TWO"] + values["TWO"] == values["FOUR"]


def format_crypt_solution(solution: Dict[str, int]) -> str:
    values = evaluate_words(solution)
    pairs = ", ".join(f"{letter}={solution[letter]}" for letter in LETTERS)
    return (
        f"Letter assignment: {pairs}\n"
        f"Check: {values['TWO']} + {values['TWO']} = {values['FOUR']}"
    )
