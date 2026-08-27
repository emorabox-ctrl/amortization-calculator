# Loan Amortization Calculator

Python program that calculates a loan's amortization schedule, showing 
payment, interest, principal, and remaining balance month by month. 
Includes support for extra payments, fixed vs. variable rate comparison, 
and exporting results to Excel.

## Motivation

As a credit analyst, I work with amortization calculations on a daily basis. 
This project is my first step into software development, applying that 
domain knowledge to build a useful tool from scratch.

## Features

- Fixed monthly payment calculation (French amortization system)
- Full amortization schedule: payment, interest, principal, and balance per month
- Handling of the special case of a 0% interest rate
- Simulation of extra payments to principal, which shorten the loan term
- Comparison between a fixed-rate scenario and a variable-rate scenario (with 
  user-defined rate tiers), including automatic payment recalculation when 
  the rate changes
- Export of the amortization schedule to an Excel file (.xlsx)
- Interactive menu to choose between a simple amortization calculation or 
  a scenario comparison
- User input validation (rejects invalid text and negative values)
- Suite of 9 automated tests with pytest

## How to run it

Requirements: Python 3.x, along with the `openpyxl` library:

```bash
python -m pip install openpyxl
```

Then run the program:

```bash
python main.py
```

The program shows a menu with two options:

**1. Calculate amortization schedule (fixed rate)**
Asks for loan amount, annual rate, and term, with the option to simulate 
extra payments to principal (specifying the month and amount of each). 
At the end, it allows exporting the resulting schedule to an Excel file.

**2. Compare fixed rate vs variable rate**
Asks for amount, term, a reference fixed rate, and the variable rate tiers 
(month the rate changes and new rate). Shows the total paid and total 
interest for each scenario, and which one is cheaper.

## How to run the tests

```bash
python -m pytest
```

## Project structure

- `main.py`: user interaction (menu, data input, results display)
- `loan_amortization.py`: calculation logic (payment, amortization schedule, 
  extra payments, variable rate, scenario comparison, Excel export)
- `test_loan_amortization.py`: automated tests with pytest

## Future improvements

- Simple web interface with Streamlit