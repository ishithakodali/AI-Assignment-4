# CSP Assignment Implementation

This project implements four Constraint Satisfaction Problem (CSP) tasks:

1. Australia map coloring for `WA, NT, Q, SA, NSW, V, T`
2. Telangana map coloring for 33 districts
3. Sudoku solver using CSP
4. Cryptarithmetic puzzle: `TWO + TWO = FOUR`

## Files

- `csp_core.py`: Generic CSP solver (backtracking + MRV + forward checking)
- `map_coloring_australia.py`: Australia map-color CSP model
- `map_coloring_telangana.py`: Telangana 33-district map-color CSP model
- `sudoku_csp.py`: Sudoku CSP model and solver
- `cryptarithmetic_two_two_four.py`: Cryptarithmetic CSP model and solver
- `main.py`: Command-line runner

## Run

Run all four tasks:

```bash
python main.py
```

Run a specific task:

```bash
python main.py --problem australia
python main.py --problem telangana
python main.py --problem sudoku
python main.py --problem crypt
```

Run Sudoku with your own 9x9 puzzle (`0` for blanks):

```bash
python main.py --problem sudoku --sudoku 003020600 900305001 001806400 008102900 700000008 006708200 002609500 800203009 005010300
```

## Notes

- Multiple valid colorings can exist for map-coloring tasks.
- Telangana district adjacency is represented as a hardcoded undirected graph.
- Tasmania is intentionally isolated in the Australia map model, so it has no adjacency edges and can take any color.
- The cryptarithmetic solver enforces:
  - all letters have distinct digits,
  - `T` is non-zero and `F` is fixed to `1`,
  - column-wise carry constraints.
