from typing import List, Dict, Optional
from shared_memory import SharedMemory


class CDCLSolver:
    def __init__(self, clauses: List[List[int]], variables: List[int], shared_memory: Optional[SharedMemory] = None, debug: bool = False):
        self.clauses = clauses
        self.variables = variables
        self.assignment: Dict[int, Optional[bool]] = {}
        self.decision_stack = []
        self.shared_memory = shared_memory if shared_memory else SharedMemory()
        self.debug = debug

        self.stats = {
            "conflicts": 0,
            "decisions": 0,
            "unit_propagations": 0,
            "learned_clauses": 0,
            "restarts": 0,
            "solved": False
        }

    def is_clause_satisfied(self, clause: List[int]) -> bool:
        return any(
            (lit > 0 and self.assignment.get(abs(lit)) is True) or
            (lit < 0 and self.assignment.get(abs(lit)) is False)
            for lit in clause
        )

    def is_clause_conflict(self, clause: List[int]) -> bool:
        return all(
            (lit > 0 and self.assignment.get(abs(lit)) is False) or
            (lit < 0 and self.assignment.get(abs(lit)) is True)
            for lit in clause if abs(lit) in self.assignment
        )

    def is_fully_assigned(self) -> bool:
        return all(var in self.assignment for var in self.variables)

    def unit_propagate(self) -> bool:
        changed = True
        all_clauses = self.clauses + self.shared_memory.get_learned_clauses()
        while changed:
            changed = False
            for clause in all_clauses:
                if self.is_clause_satisfied(clause):
                    continue
                unassigned = [lit for lit in clause if abs(lit) not in self.assignment]
                if len(unassigned) == 1:
                    unit_lit = unassigned[0]
                    var = abs(unit_lit)
                    value = unit_lit > 0
                    if var in self.assignment:
                        if self.assignment[var] != value:
                            self.stats["conflicts"] += 1
                            for lit in clause:
                                self.shared_memory.update_variable_score(abs(lit), 1.0)
                            if clause not in self.shared_memory.get_learned_clauses():
                                self.shared_memory.add_learned_clause(clause)
                                self.stats["learned_clauses"] += 1
                                if self.debug:
                                    print(f"Learned clause (unit conflict): {clause}")
                            return False
                    else:
                        self.assignment[var] = value
                        self.decision_stack.append((var, value, True))
                        changed = True
                        self.stats["unit_propagations"] += 1
                elif self.is_clause_conflict(clause):
                    self.stats["conflicts"] += 1
                    for lit in clause:
                        self.shared_memory.update_variable_score(abs(lit), 1.0)
                    if clause not in self.shared_memory.get_learned_clauses():
                        self.shared_memory.add_learned_clause(clause)
                        self.stats["learned_clauses"] += 1
                        if self.debug:
                            print(f"Learned clause (full conflict): {clause}")
                    return False
        return True

    def choose_unassigned_variable(self) -> Optional[int]:
        hints = self.shared_memory.get_assignment_hints()
        scored = self.shared_memory.get_variable_scores()
        unassigned = [v for v in self.variables if v not in self.assignment]
        for var in unassigned:
            if var in hints:
                return var
        if scored:
            return max(unassigned, key=lambda v: scored.get(v, 0.0))
        return unassigned[0] if unassigned else None

    def backtrack(self) -> bool:
        while self.decision_stack:
            var, value, implied = self.decision_stack.pop()
            del self.assignment[var]
            if not implied:
                self.assignment[var] = not value
                self.decision_stack.append((var, not value, False))
                return True
        return False

    def solve(self) -> bool:
        # Restart every 100 conflicts
        if self.stats["conflicts"] > 0 and self.stats["conflicts"] % 100 == 0:
            self.assignment.clear()
            self.decision_stack.clear()
            self.stats["restarts"] += 1
            if self.debug:
                print(f"[Restart] After {self.stats['conflicts']} conflicts")

        # Optional score decay for VSIDS
        if self.stats["conflicts"] > 0 and self.stats["conflicts"] % 50 == 0:
            for var in self.variables:
                self.shared_memory.update_variable_score(var, -0.1)

        if not self.unit_propagate():
            return self.backtrack() and self.solve()

        if self.is_fully_assigned():
            self.stats["solved"] = True
            return True

        var = self.choose_unassigned_variable()
        if var is None:
            return self.is_fully_assigned()

        hint_val = self.shared_memory.get_assignment_hints().get(var)
        for value in ([hint_val, not hint_val] if hint_val is not None else [True, False]):
            self.assignment[var] = value
            self.decision_stack.append((var, value, False))
            self.stats["decisions"] += 1
            if self.debug:
                print(f"Decision: var {var} = {value}")
            if self.solve():
                return True
            self.assignment.pop(var)
            self.decision_stack.pop()

        return self.backtrack() and self.solve()

    def get_assignment(self) -> Dict[int, bool]:
        return self.assignment

    def get_stats(self) -> Dict:
        return self.stats