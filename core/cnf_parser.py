from typing import List, Tuple

def parse_cnf_file(filepath: str) -> Tuple[List[List[int]], List[int]]:
    """
    Parses a DIMACS CNF file and returns the clause list and variable list.

    Returns:
        - clauses: List of clauses (each clause is a list of literals)
        - variables: List of unique variable numbers
    """
    clauses: List[List[int]] = []
    variables_set = set()

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith(('c', 'p', '%')):
                continue  # Skip comments, problem lines, end-of-input markers

            try:
                tokens = list(map(int, line.split()))
            except ValueError:
                print(f"Skipping malformed line: {line}")
                continue

            if not tokens or tokens[-1] != 0:
                print(f"Warning: clause does not end with 0 → {line}")
                continue

            literals = tokens[:-1]  # Remove trailing 0

            for lit in literals:
                variables_set.add(abs(lit))

            clauses.append(literals)

    variables = sorted(list(variables_set))
    return clauses, variables

# Optional: CLI runner for quick tests
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python cnf_parser.py path/to/cnf_file.cnf")
        sys.exit(1)

    path = sys.argv[1]
    clauses, variables = parse_cnf_file(path)
    print(f"Parsed {len(clauses)} clauses using {len(variables)} variables.")
    print("Clauses:", clauses)
