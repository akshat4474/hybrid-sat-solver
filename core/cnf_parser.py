# cnf_parser.py

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

            if line.startswith('c') or line == '':
                continue  # Skip comments or empty lines

            if line.startswith('p'):
                parts = line.split()
                if len(parts) != 4 or parts[1] != "cnf":
                    raise ValueError("Invalid problem line in CNF file.")
                continue  # Skip the problem line

            # Parse clause
            literals = list(map(int, line.split()))
            if literals[-1] != 0:
                raise ValueError(f"Clause line must end with 0. Got: {line}")
            literals = literals[:-1]  # Remove trailing 0

            for lit in literals:
                variables_set.add(abs(lit))

            clauses.append(literals)

    variables = sorted(list(variables_set))
    return clauses, variables


# Optional: Add a quick CLI runner
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python cnf_parser.py path/to/cnf_file.cnf")
        sys.exit(1)

    path = sys.argv[1]
    clauses, variables = parse_cnf_file(path)
    print(f"Parsed {len(clauses)} clauses using {len(variables)} variables.")
    print("Clauses:", clauses)
