from typing import List, Dict, Optional
import itertools
from shared_memory import SharedMemory


class BruteForceSolver:
    def __init__(
        self,
        clauses: List[List[int]],
        variables: List[int],
        scope_limit: int = 14,
        shared_memory: Optional[SharedMemory] = None,
        debug: bool = False
    ):
        """
        clauses: List of clauses (e.g., [[1, -2, 3], [-1, 4, 5]])
        variables: Full list of variables in the formula
        scope_limit: Max number of variables to brute force (default 10)
        shared_memory: SharedMemory object for storing known unsatisfiable scopes
        debug: Enable print debugging of tested assignments
        """
        if len(variables) > scope_limit:
            raise ValueError(f"Too many variables ({len(variables)}) for brute force. Limit is {scope_limit}.")
        self.clauses = clauses
        self.variables = variables
        self.shared_memory = shared_memory if shared_memory else SharedMemory()
        self.assignment: Dict[int, bool] = {}
        self.debug = debug

        self.stats = {
            "evaluations": 0,
            "assignments_tested": 0,
            "solved": False
        }

    def evaluate_clause(self, clause: List[int], assignment: Dict[int, bool]) -> bool:
        return any(
            (lit > 0 and assignment.get(abs(lit), False)) or
            (lit < 0 and not assignment.get(abs(lit), True))
            for lit in clause
        )

    def evaluate_formula(self, assignment: Dict[int, bool]) -> bool:
        self.stats["evaluations"] += 1
        return all(self.evaluate_clause(clause, assignment) for clause in self.clauses)

    def solve(self) -> bool:
        """
        Brute-force all combinations of truth assignments for scoped variables.
        Returns True if a satisfying assignment is found.
        """
        for bits in itertools.product([False, True], repeat=len(self.variables)):
            current_assignment = {var: val for var, val in zip(self.variables, bits)}
            self.stats["assignments_tested"] += 1
            if self.debug:
                print(f"Testing assignment: {current_assignment}")
            if self.evaluate_formula(current_assignment):
                self.assignment = current_assignment
                self.stats["solved"] = True
                return True

        # If no assignment works, optionally store unsat scope
        self.shared_memory.add_unsat_scope(tuple(sorted(self.variables)))
        return False

    def get_assignment(self) -> Dict[int, bool]:
        return self.assignment

    def get_stats(self) -> Dict:
        return self.stats