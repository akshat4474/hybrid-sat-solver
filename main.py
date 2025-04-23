import argparse
import os
from generate_cnf import generate_random_cnf
from core.cnf_parser import parse_cnf_file
from core.controller import SolverController
from logger import log_cnf_metadata


def run_solver(cnf_path: str, brute_scope_limit: int = 14):
    if not os.path.exists(cnf_path):
        print(f"File not found: {cnf_path}")
        return

    clauses, variables = parse_cnf_file(cnf_path)
    print(f"CNF File: {cnf_path}")
    print(f"Variables: {len(variables)}")
    print(f"Clauses: {len(clauses)}")
    if len(variables) > 0:
        print(f"Clause-to-Variable Ratio: {len(clauses)/len(variables):.2f}")

    controller = SolverController(clauses, variables, brute_scope_limit=brute_scope_limit, source_file=cnf_path)
    if controller.run_all():
        print("SATISFIABLE")
        print("Assignment:", controller.get_assignment())
    else:
        print("UNSATISFIABLE or no solver succeeded")

def main():
    parser = argparse.ArgumentParser(description="Hybrid SAT Solver")
    parser.add_argument("--cnf", type=str, help="Path to existing CNF file")
    parser.add_argument("--generate", action="store_true", help="Generate a random CNF before solving")
    parser.add_argument("--vars", type=int, default=20, help="Number of variables for generated CNF")
    parser.add_argument("--clauses", type=int, default=85, help="Number of clauses for generated CNF")
    parser.add_argument("--out", type=str, default="data/generated/test.cnf", help="Output path for generated CNF")
    parser.add_argument("--brute_limit", type=int, default=10, help="Max variables allowed for Brute Force Solver")

    args = parser.parse_args()

    if args.generate:
        print(f"Generating CNF: {args.vars} vars, {args.clauses} clauses")
        metadata = generate_random_cnf(args.vars, args.clauses, args.out)
        log_cnf_metadata(metadata)
        run_solver(args.out, brute_scope_limit=args.brute_limit)
    elif args.cnf:
        run_solver(args.cnf, brute_scope_limit=args.brute_limit)
    else:
        print("Please provide either --cnf <path> or --generate")

if __name__ == "__main__":
    main()
