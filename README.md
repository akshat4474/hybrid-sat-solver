# Hybrid SAT Solver

A modular hybrid SAT solver combining CDCL, WalkSAT, and Brute Force strategies with a shared memory layer for clause learning, variable scoring, and assignment hint propagation. Designed for research and experimentation, the solver can adapt to SAT/UNSAT trends and supports dynamic benchmarking.

##  Features
- **CDCL Solver** with clause learning, VSIDS-style variable scoring, and restarts
- **WalkSAT Solver** with stochastic flips and heuristic guidance
- **Brute Force Solver** for small scoped CNFs (as reference or ground truth)
- **Shared Knowledge Layer** for clause sharing and variable interaction
- **Assignment Hints** passed between solvers to guide decision heuristics
- **Experiment-Ready Logging** with runtime stats, clause-to-variable ratios, and solver decisions

##  Project Structure
```
.
├── main.py                # CLI entrypoint for generating and solving CNFs
├── core/
│   |── controller.py      # Orchestrates solver logic and logging
│   └── cnf_parser.py      # Parses DIMACS CNF files
├── shared_memory.py       # In-memory clause, score, and hint exchange system
├── logger.py              # Logging utilities for solver runs and metadata
├── generate_cnf.py        # Random 3-CNF generator
├── test.py                # Batch experiment runner
├── data/
│   └── generated/         # Stores generated CNF files
|── logs/                  # Contains shared_memory.json, solver_log.csv, etc.
└── solvers/
│   ├── cdcl_solver.py     # Conflict-Driven Clause Learning solver
│   ├── walksat_solver.py  # WalkSAT heuristic solver
│   └── brute_solver.py    # Brute-force verifier for small CNFs
```

## Usage

### 1. Solve an existing CNF file:
```bash
python main.py --cnf data/examples/example.cnf
```

### 2. Generate a new 3-CNF and solve it:
```bash
python main.py --generate --vars 30 --clauses 120 --out data/generated/test.cnf
```

### 3. Run batch experiments:
```bash
python test.py --vars 30 40 --ratios 4.5 5.0 --repeats 3 --out data/generated/very_hard
```

##  Logs and Metadata(Automatically created when run)
- `logs/solver_log.csv` — performance stats for each solver per run
- `logs/shared_memory.json` — cross-run learned clauses, scores, hints
- `logs/cnf_metadata.csv` — clause/variable info and generation seeds

##  Citation
If you use this project in academic research, please cite:

```
@misc{bisht2024hybridsat,
  author = {Akshat Bisht},
  title = {Hybrid SAT Solver with Shared Clause Learning},
  year = {2024},
  howpublished = {GitHub repository},
  note = {https://github.com/akshat4474/hybrid-sat-solver}
}
```

##  License
Apache License 2.0 — see `LICENSE` file for details.

---
Contributions and issues welcome. Solver performance logs can be submitted to expand benchmarks!

---