import random
from typing import List, Dict, Optional

class WalkSATSolver:
    def __init__(
        self,
        clauses: List[List[int]],
        variables: List[int],
        max_flips: int = 10000,
        p_random_flip: float = 0.5,
        shared_memory: Optional[dict] = None
    ):
        self.clauses = clauses
        self.variables = variables
        self.assignment: Dict[int, bool] = {}
        self.max_flips = max_flips
        self.p_random_flip = p_random_flip
        self.shared_memory = shared_memory if shared_memory is not None else {}

    def initialize_random_assignment(self):
        self.assignment = {var: random.choice([True, False]) for var in self.variables}

    def is_clause_satisfied(self, clause: List[int]) -> bool:
        return any(
            (lit > 0 and self.assignment.get(abs(lit), False)) or
            (lit < 0 and not self.assignment.get(abs(lit), True))
            for lit in clause
        )

    def get_unsatisfied_clauses(self) -> List[List[int]]:
        return [clause for clause in self.clauses if clause and not self.is_clause_satisfied(clause)]

    def flip_variable(self, var: int):
        self.assignment[var] = not self.assignment[var]

    def best_flip_in_clause(self, clause: List[int]) -> int:
        """
        Heuristically select the variable in the clause whose flip satisfies most clauses.
        """
        if not clause:
            return random.choice(self.variables)  # fallback to avoid IndexError

        max_satisfied = -1
        best_var = abs(clause[0])
        for lit in clause:
            var = abs(lit)
            self.flip_variable(var)
            satisfied_count = sum(self.is_clause_satisfied(c) for c in self.clauses)
            self.flip_variable(var)  # revert
            if satisfied_count > max_satisfied:
                max_satisfied = satisfied_count
                best_var = var
        return best_var

    def solve(self) -> bool:
        self.initialize_random_assignment()

        for step in range(self.max_flips):
            unsat_clauses = self.get_unsatisfied_clauses()
            if not unsat_clauses:
                return True  # All clauses satisfied

            clause = random.choice(unsat_clauses)

            if not clause:
                continue  # skip empty clause if any slip through

            if random.random() < self.p_random_flip:
                var_to_flip = abs(random.choice(clause))
            else:
                var_to_flip = self.best_flip_in_clause(clause)

            self.flip_variable(var_to_flip)

        return False  # Max flips reached without solving

    def get_assignment(self) -> Dict[int, bool]:
        return self.assignment
