from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from itertools import combinations
from typing import Any, Callable, Deque, Dict, Iterable, List, Optional, Sequence, Set, Tuple

Assignment = Dict[str, Any]
Predicate = Callable[[Assignment], bool]


@dataclass(frozen=True)
class Constraint:
    scope: Tuple[str, ...]
    predicate: Predicate
    name: str = ""


class CSP:
    def __init__(self, variables: Sequence[str], domains: Dict[str, Iterable[Any]]) -> None:
        self.variables: List[str] = list(variables)
        self.domains: Dict[str, List[Any]] = {var: list(domains[var]) for var in self.variables}
        self.constraints_by_var: Dict[str, List[Constraint]] = {var: [] for var in self.variables}
        self.neighbors: Dict[str, Set[str]] = {var: set() for var in self.variables}

        missing_domains = [var for var in self.variables if var not in self.domains]
        if missing_domains:
            raise ValueError(f"Missing domains for variables: {missing_domains}")

    def add_constraint(self, scope: Sequence[str], predicate: Predicate, name: str = "") -> None:
        scope_tuple = tuple(scope)
        for var in scope_tuple:
            if var not in self.constraints_by_var:
                raise ValueError(f"Unknown variable in constraint scope: {var}")

        constraint = Constraint(scope=scope_tuple, predicate=predicate, name=name)
        for var in scope_tuple:
            self.constraints_by_var[var].append(constraint)

        for a, b in combinations(scope_tuple, 2):
            self.neighbors[a].add(b)
            self.neighbors[b].add(a)

    def is_consistent(self, variable: str, assignment: Assignment) -> bool:
        for constraint in self.constraints_by_var[variable]:
            if not constraint.predicate(assignment):
                return False
        return True

    def _degree(self, variable: str, assignment: Assignment) -> int:
        return sum(1 for n in self.neighbors[variable] if n not in assignment)

    def _select_unassigned_variable(self, assignment: Assignment, domains: Dict[str, List[Any]]) -> str:
        unassigned = [v for v in self.variables if v not in assignment]

        # Minimum Remaining Values with Degree tie-break.
        return min(unassigned, key=lambda var: (len(domains[var]), -self._degree(var, assignment)))

    def _related_constraints(self, xi: str, xj: str) -> List[Constraint]:
        return [constraint for constraint in self.constraints_by_var[xi] if xj in constraint.scope]

    def _revise(self, domains: Dict[str, List[Any]], xi: str, xj: str) -> bool:
        related = self._related_constraints(xi, xj)
        if not related:
            return False

        revised = False
        supported: List[Any] = []
        for value_x in domains[xi]:
            has_support = False
            for value_y in domains[xj]:
                partial = {xi: value_x, xj: value_y}
                if all(constraint.predicate(partial) for constraint in related):
                    has_support = True
                    break
            if has_support:
                supported.append(value_x)
            else:
                revised = True

        if revised:
            domains[xi] = supported

        return revised

    def _all_arcs(self) -> List[Tuple[str, str]]:
        arcs: List[Tuple[str, str]] = []
        for xi in self.variables:
            for xj in self.neighbors[xi]:
                arcs.append((xi, xj))
        return arcs

    def _ac3(
        self,
        domains: Dict[str, List[Any]],
        queue: Optional[Sequence[Tuple[str, str]]] = None,
    ) -> Optional[Dict[str, List[Any]]]:
        working_domains = {var: list(values) for var, values in domains.items()}
        arc_queue: Deque[Tuple[str, str]] = deque(queue if queue is not None else self._all_arcs())

        while arc_queue:
            xi, xj = arc_queue.popleft()
            if self._revise(working_domains, xi, xj):
                if not working_domains[xi]:
                    return None
                for xk in self.neighbors[xi]:
                    if xk != xj:
                        arc_queue.append((xk, xi))

        return working_domains

    def ac3_preprocess(self, domains: Optional[Dict[str, List[Any]]] = None) -> Optional[Dict[str, List[Any]]]:
        base = domains if domains is not None else {var: list(vals) for var, vals in self.domains.items()}
        return self._ac3(base)

    def _order_values(self, variable: str, domains: Dict[str, List[Any]]) -> List[Any]:
        return list(domains[variable])

    def _forward_check(
        self,
        assignment: Assignment,
        domains: Dict[str, List[Any]],
    ) -> Optional[Dict[str, List[Any]]]:
        new_domains = {var: list(values) for var, values in domains.items()}

        for var in self.variables:
            if var in assignment:
                continue

            supported_values: List[Any] = []
            for value in new_domains[var]:
                assignment[var] = value
                if self.is_consistent(var, assignment):
                    supported_values.append(value)
                del assignment[var]

            if not supported_values:
                return None

            new_domains[var] = supported_values

        return new_domains

    def backtracking_search(self) -> Optional[Assignment]:
        initial_domains = self.ac3_preprocess()
        if initial_domains is None:
            return None
        return self._backtrack(assignment={}, domains=initial_domains)

    def _backtrack(
        self,
        assignment: Assignment,
        domains: Dict[str, List[Any]],
    ) -> Optional[Assignment]:
        if len(assignment) == len(self.variables):
            return dict(assignment)

        variable = self._select_unassigned_variable(assignment, domains)

        for value in self._order_values(variable, domains):
            assignment[variable] = value
            if self.is_consistent(variable, assignment):
                branch_domains = {var: list(vals) for var, vals in domains.items()}
                branch_domains[variable] = [value]

                seed_arcs = [(neighbor, variable) for neighbor in self.neighbors[variable] if neighbor not in assignment]
                ac3_domains = self._ac3(branch_domains, queue=seed_arcs)
                if ac3_domains is not None:
                    pruned_domains = self._forward_check(assignment, ac3_domains)
                    if pruned_domains is not None:
                        result = self._backtrack(assignment, pruned_domains)
                        if result is not None:
                            return result
            del assignment[variable]

        return None


def all_different_constraint(scope: Sequence[str]) -> Predicate:
    scope_tuple = tuple(scope)

    def _predicate(assignment: Assignment) -> bool:
        seen = set()
        for var in scope_tuple:
            if var in assignment:
                value = assignment[var]
                if value in seen:
                    return False
                seen.add(value)
        return True

    return _predicate


def not_equal_constraint(a: str, b: str) -> Predicate:
    def _predicate(assignment: Assignment) -> bool:
        if a in assignment and b in assignment:
            return assignment[a] != assignment[b]
        return True

    return _predicate
