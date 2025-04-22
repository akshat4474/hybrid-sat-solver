from typing import List, Optional, Dict
from solvers.cdcl_solver import CDCLSolver
from solvers.walksat_solver import WalkSATSolver
from solvers.brute_solver import BruteForceSolver
from shared_memory import SharedMemory
import time
from logger import log_solver_result


class SolverController:
    def __init__(self, clauses: List[List[int]], variables: List[int], brute_scope_limit: int = 10, source_file: str = "unknown",debug: bool = False):
        self.clauses = clauses
        self.variables = variables
        self.shared_memory = SharedMemory()
        self.result_assignment: Optional[Dict[int, bool]] = None
        self.brute_scope_limit = brute_scope_limit
        self.source_file = source_file
        self.debug = debug

        # Flags
        self.cdcl_enabled = True
        self.walksat_enabled = True
        self.brute_enabled = len(variables) <= brute_scope_limit
        self.stats: Dict = {}

    def run_cdcl(self) -> bool:
        print(" Running CDCL Solver...")
        cdcl = CDCLSolver(self.clauses, self.variables, shared_memory=self.shared_memory, debug=self.debug)
        if cdcl.solve():
            self.result_assignment = cdcl.get_assignment()
            self.stats = cdcl.get_stats()
            print(" CDCL solved the problem.")
            return True
        self.stats = cdcl.get_stats()
        print(" CDCL failed to solve.")
        return False

    def run_walksat(self, max_flips=10000) -> bool:
        print(" Running WalkSAT Solver...")
        walksat = WalkSATSolver(self.clauses, self.variables, max_flips=max_flips, shared_memory=self.shared_memory)
        if hasattr(walksat, 'get_stats'):
            self.stats = walksat.get_stats()
        if walksat.solve():
            self.result_assignment = walksat.get_assignment()
            if hasattr(walksat, 'get_stats'):
                self.stats = walksat.get_stats()
            print(" WalkSAT solved the problem.")
            for var, val in self.result_assignment.items():
                self.shared_memory.set_assignment_hint(var, val)
            return True
        if hasattr(walksat, 'get_stats'):
            self.stats = walksat.get_stats()
        print(" WalkSAT failed to solve.")
        return False

    def run_brute_force(self) -> bool:
        print(" Running Brute Force Solver...")
        brute = BruteForceSolver(self.clauses, self.variables, shared_memory=self.shared_memory)
        if brute.solve():
            self.result_assignment = brute.get_assignment()
            self.stats = brute.get_stats()
            print(" Brute Force solved the problem.")
            return True
        self.stats = brute.get_stats()
        print(" Brute Force failed or scope too large.")
        return False

    def run_all(self) -> bool:
        print("\n Starting Hybrid SAT Solver...")
        start_time = time.time()

        print(" Loaded learned clauses:", len(self.shared_memory.get_learned_clauses()))
        print(" Loaded variable scores:", len(self.shared_memory.get_variable_scores()))
        print(" Loaded assignment hints:", len(self.shared_memory.get_assignment_hints()))

        if self.cdcl_enabled:
            if self.run_cdcl():
                self.log_result("CDCL", start_time, "success")
                return True

        if self.walksat_enabled:
            if self.run_walksat():
                self.log_result("WalkSAT", start_time, "success")
                return True

        if self.brute_enabled:
            if self.debug:
                print(f" Brute Force is ENABLED (variables = {len(self.variables)}, limit = {self.brute_scope_limit})")
            if self.run_brute_force():
                self.log_result("Brute Force", start_time, "success")
                return True
        else:
            if self.debug:
                print(f" Brute Force is SKIPPED (variables = {len(self.variables)}, limit = {self.brute_scope_limit})")


        self.log_result("None", start_time, "failure")
        return False

    def log_result(self, solver_name: str, start_time: float, status: str):
        duration = time.time() - start_time
        print(f"\n Result Summary:")
        print(f"  → Solved by: {solver_name}")
        print(f"  → Time taken: {duration:.3f} seconds")
        print(f"  → Assignment: {self.result_assignment}")

        self.shared_memory.save()
        self.write_log(solver_name, status, duration)

    def get_assignment(self) -> Optional[Dict[int, bool]]:
        return self.result_assignment

    def write_log(self, solver_name: str, status: str, duration: float):
        log_data = {
            "source_file": self.source_file,
            "solver": solver_name,
            "status": status,
            "runtime_sec": round(duration, 4),
            "variables": len(self.variables),
            "clauses": len(self.clauses),
            "clause_var_ratio": round(len(self.clauses) / max(len(self.variables), 1), 2),
            "assignment_found": "Yes" if self.result_assignment else "No"
        }

        if self.stats:
            for k, v in self.stats.items():
                log_data[f"stat_{k}"] = v

        log_solver_result(log_data)
