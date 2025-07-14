# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Structure

This is a personal programming practice repository containing:

- **codility/**: Algorithm practice problems from Codility platform
  - Contains text files with problem descriptions and Python solutions
  - Files include: binary_gap.txt, divisible_count.txt, fib_frog.txt, max_counters.txt, missing_integer.txt, odd_occurances_in_array.txt
  - Python implementations: sieve_of_era.py, triangle.py

- **py/**: General Python practice and Project Euler solutions
  - euler.py: Contains commented-out solutions to Project Euler problems
  - Individual problem files: eu3.py, eu4.py, eu5.py, eu6.py, eu7.py, eu8.py, eu9.py
  - Hello.py: Basic Python 2 hello world program
  - Various utility scripts: collatz.py, test.py

- **claude-practice/**: Practice exercises specifically for Claude AI
  - rps.py: Rock Paper Scissors implementation (currently empty)

## Development Environment

This repository uses Python for all implementations. The codebase contains both Python 2 and Python 3 code:
- Python 2 syntax found in Hello.py
- Python 3 syntax in most other files

## Common Commands

Since this is a practice repository without a formal build system:

```bash
# Run individual Python files
python filename.py

# For Python 2 files
python2 filename.py

# For Python 3 files  
python3 filename.py
```

## Code Patterns

- Algorithm implementations focus on performance optimization (see sieve_of_era.py with multiple sieve implementations)
- Project Euler solutions are typically self-contained in individual files
- Problem descriptions are often stored in accompanying .txt files
- Code includes performance timing for algorithm comparison