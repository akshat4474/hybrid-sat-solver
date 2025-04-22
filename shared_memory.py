# shared_memory.py

import json
import os
from typing import List, Dict, Tuple
from threading import Lock


class SharedMemory:
    def __init__(self, save_path: str = "logs/shared_memory.json"):
        self.lock = Lock()
        self.save_path = save_path

        # Knowledge Store
        self.learned_clauses: List[List[int]] = []
        self.failed_assignments: List[Dict[int, bool]] = []
        self.unsat_scopes: List[Tuple[int]] = []

        # Heuristics & Stats
        self.variable_scores: Dict[int, float] = {}
        self.flip_history: Dict[int, int] = {}
        self.assignment_hint: Dict[int, bool] = {}

        # Load previous session if available
        self.load()

    # -----------------------------
    # Clause & Conflict Sharing
    # -----------------------------

    def add_learned_clause(self, clause: List[int]):
        with self.lock:
            if clause not in self.learned_clauses:
                self.learned_clauses.append(clause)

    def get_learned_clauses(self) -> List[List[int]]:
        with self.lock:
            return list(self.learned_clauses)

    def add_failed_assignment(self, assignment: Dict[int, bool]):
        with self.lock:
            self.failed_assignments.append(assignment)

    def get_failed_assignments(self) -> List[Dict[int, bool]]:
        with self.lock:
            return list(self.failed_assignments)

    def add_unsat_scope(self, vars_tuple: Tuple[int]):
        with self.lock:
            self.unsat_scopes.append(vars_tuple)

    def get_unsat_scopes(self) -> List[Tuple[int]]:
        with self.lock:
            return list(self.unsat_scopes)

    # -----------------------------
    # Variable Scoring & Hints
    # -----------------------------

    def update_variable_score(self, var: int, delta: float):
        with self.lock:
            self.variable_scores[var] = self.variable_scores.get(var, 0.0) + delta

    def get_variable_scores(self) -> Dict[int, float]:
        with self.lock:
            return dict(self.variable_scores)

    def increment_flip_count(self, var: int):
        with self.lock:
            self.flip_history[var] = self.flip_history.get(var, 0) + 1

    def get_flip_history(self) -> Dict[int, int]:
        with self.lock:
            return dict(self.flip_history)

    def set_assignment_hint(self, var: int, value: bool):
        with self.lock:
            self.assignment_hint[var] = value

    def get_assignment_hints(self) -> Dict[int, bool]:
        with self.lock:
            return dict(self.assignment_hint)

    # -----------------------------
    # Persistence
    # -----------------------------

    def save(self):
        os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
        with open(self.save_path, 'w') as f:
            json.dump({
                "learned_clauses": self.learned_clauses,
                "failed_assignments": self.failed_assignments,
                "unsat_scopes": [list(scope) for scope in self.unsat_scopes],
                "variable_scores": self.variable_scores,
                "flip_history": self.flip_history,
                "assignment_hint": self.assignment_hint
            }, f, indent=2)
        print(f" Shared memory saved to {self.save_path}")

    def load(self):
        if os.path.exists(self.save_path):
            with open(self.save_path, 'r') as f:
                data = json.load(f)
                self.learned_clauses = data.get("learned_clauses", [])
                self.failed_assignments = data.get("failed_assignments", [])
                self.unsat_scopes = [tuple(x) for x in data.get("unsat_scopes", [])]
                self.variable_scores = data.get("variable_scores", {})
                self.flip_history = data.get("flip_history", {})
                self.assignment_hint = data.get("assignment_hint", {})
            print(f" Loaded shared memory from {self.save_path}")
        else:
            print(f" No shared memory file found. Starting fresh.")

    def reset(self):
        with self.lock:
            self.learned_clauses.clear()
            self.failed_assignments.clear()
            self.unsat_scopes.clear()
            self.variable_scores.clear()
            self.flip_history.clear()
            self.assignment_hint.clear()
        print("🧹 Shared memory reset.")

