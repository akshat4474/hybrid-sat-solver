import argparse
import os
import subprocess
from itertools import product

def run_batch_test(vars_list, ratio_list, repeats, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for num_vars, ratio in product(vars_list, ratio_list):
        num_clauses = int(num_vars * ratio)

        for i in range(repeats):
            filename = f"v{num_vars}_r{ratio}_run{i+1}.cnf"
            out_path = os.path.join(output_dir, filename)

            # Build CLI command for main.py
            cmd = [
                "python", "main.py",
                "--generate",
                "--vars", str(num_vars),
                "--clauses", str(num_clauses),
                "--out", out_path
            ]

            print("Running:", " ".join(cmd))
            subprocess.run(cmd)

def main():
    parser = argparse.ArgumentParser(description="Run batch SAT tests using main.py")
    parser.add_argument('--vars', nargs='+', type=int, default=[20, 30], help="List of variable counts")
    parser.add_argument('--ratios', nargs='+', type=float, default=[2.5, 3.5, 4.2, 4.5], help="List of clause-to-variable ratios")
    parser.add_argument('--repeats', type=int, default=3, help="Number of repetitions per combination")
    parser.add_argument('--out', type=str, default="data/generated/test_batch", help="Output directory for CNF files")

    args = parser.parse_args()
    run_batch_test(args.vars, args.ratios, args.repeats, args.out)

if __name__ == "__main__":
    main()
