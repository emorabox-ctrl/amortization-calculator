# Loan Amortization Calculator

Python program that calculates a loan's amortization schedule, showing 
payment, interest, principal, and remaining balance month by month. 
Includes support for extra payments, fixed vs. variable rate comparison, 
exporting results to Excel, and an interactive web interface built with 
Streamlit.

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
- Interactive command-line menu, plus a web app built with Streamlit
- User input validation (rejects invalid text and negative values)
- Suite of 9 automated tests with pytest

## Requirements

Python 3.x, plus the dependencies listed in `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

## How to run it (command line)

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

## Web app (Streamlit)

There's also an interactive web version of this calculator:

```bash
streamlit run app.py
```

This opens a browser-based interface where you can calculate amortization 
schedules, simulate extra payments, compare fixed vs variable rates, and 
download the results as Excel — all without using the terminal.

## How to run the tests

```bash
python -m pytest
```

## Project structure

- `main.py`: command-line interaction (menu, data input, results display)
- `app.py`: interactive web interface built with Streamlit
- `loan_amortization.py`: calculation logic (payment, amortization schedule, 
  extra payments, variable rate, scenario comparison, Excel export)
- `test_loan_amortization.py`: automated tests with pytest
- `requirements.txt`: project dependencies

## Future improvements

- Deploy the Streamlit app online (e.g. Streamlit Community Cloud)
- Add charts to visualize balance and interest over time