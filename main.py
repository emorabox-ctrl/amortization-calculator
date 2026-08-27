from loan_amortization import generate_amortization_schedule, generate_variable_rate_schedule, compare_scenarios, export_to_excel


def ask_number(message, value_type=float):
    while True:
        entry = input(message)
        try:
            value = value_type(entry)
            if value <= 0:
                print("The value must be greater than 0. Try again.\n")
                continue
            return value
        except ValueError:
            print("That's not a valid number. Try again.\n")


def ask_loan_data():
    amount = ask_number("Loan amount: ", float)
    annual_rate = ask_number("Annual interest rate (%): ", float)
    term_months = ask_number("Term in months: ", int)
    return amount, annual_rate, term_months


def ask_extra_payments():
    extra_payments = {}
    answer = input("\nDo you want to simulate extra payments to principal? (y/n): ").strip().lower()
    
    if answer != "y":
        return extra_payments
    
    print("Enter the extra payments one by one. When done, leave the month blank and press Enter.\n")
    
    while True:
        month_text = input("Month of the extra payment (or Enter to finish): ").strip()
        if month_text == "":
            break
        try:
            month = int(month_text)
        except ValueError:
            print("That's not a valid month. Try again.\n")
            continue
        
        extra_amount = ask_number(f"Extra payment amount for month {month}: ", float)
        extra_payments[month] = extra_amount
    
    return extra_payments


def ask_rate_tiers():
    print("\nDefine the variable rate tiers. The first tier must start at month 1.")
    print("When done, leave the month blank and press Enter.\n")
    
    tiers = {}
    while True:
        month_text = input("Month from which this rate applies (or Enter to finish): ").strip()
        if month_text == "":
            break
        try:
            month = int(month_text)
        except ValueError:
            print("That's not a valid month. Try again.\n")
            continue
        
        rate = ask_number(f"Annual rate (%) starting month {month}: ", float)
        tiers[month] = rate
    
    if 1 not in tiers:
        print("\nWarning: you didn't set a rate for month 1. The first rate you gave will be used from the start.")
    
    return tiers


def show_schedule(schedule):
    has_rate = "annual_rate" in schedule[0]
    
    if has_rate:
        print("\n{:<5} {:<8} {:<12} {:<12} {:<12} {:<14} {:<12}".format(
            "Month", "Rate%", "Payment", "Interest", "Principal", "Extra Payment", "Balance"
        ))
        print("-" * 78)
        for row in schedule:
            print("{:<5} {:<8} {:<12.2f} {:<12.2f} {:<12.2f} {:<14.2f} {:<12.2f}".format(
                row["month"], row["annual_rate"], row["payment"], row["interest"],
                row["principal"], row["extra_payment"], row["balance"]
            ))
    else:
        print("\n{:<5} {:<12} {:<12} {:<12} {:<14} {:<12}".format(
            "Month", "Payment", "Interest", "Principal", "Extra Payment", "Balance"
        ))
        print("-" * 70)
        for row in schedule:
            print("{:<5} {:<12.2f} {:<12.2f} {:<12.2f} {:<14.2f} {:<12.2f}".format(
                row["month"], row["payment"], row["interest"], row["principal"],
                row["extra_payment"], row["balance"]
            ))
    
    print(f"\nTotal months paid: {len(schedule)}")


def show_comparison(result):
    print("\n===== Comparison: Fixed Rate vs Variable Rate =====")
    print(f"Total paid (fixed rate):      {result['total_paid_fixed']:.2f}")
    print(f"Total paid (variable rate):   {result['total_paid_variable']:.2f}")
    print(f"Total interest (fixed rate):  {result['total_interest_fixed']:.2f}")
    print(f"Total interest (variable rate): {result['total_interest_variable']:.2f}")
    
    difference = result["difference"]
    if difference > 0:
        print(f"\nThe variable rate is MORE EXPENSIVE by {difference:.2f}")
    elif difference < 0:
        print(f"\nThe variable rate is CHEAPER by {abs(difference):.2f}")
    else:
        print("\nBoth scenarios cost exactly the same.")


def ask_export(schedule):
    answer = input("\nDo you want to export this schedule to Excel? (y/n): ").strip().lower()
    if answer == "y":
        file_name = input("File name (Enter to use 'amortization_schedule.xlsx'): ").strip()
        if file_name == "":
            file_name = "amortization_schedule.xlsx"
        if not file_name.endswith(".xlsx"):
            file_name += ".xlsx"
        generated_file = export_to_excel(schedule, file_name)
        print(f"File saved as: {generated_file}")


def regular_amortization_flow():
    amount, annual_rate, term_months = ask_loan_data()
    extra_payments = ask_extra_payments()
    schedule = generate_amortization_schedule(amount, annual_rate, term_months, extra_payments)
    show_schedule(schedule)
    ask_export(schedule)


def comparison_flow():
    amount = ask_number("Loan amount: ", float)
    term_months = ask_number("Term in months: ", int)
    fixed_rate = ask_number("Fixed annual rate (%) for the fixed scenario: ", float)
    variable_rate_tiers = ask_rate_tiers()
    
    result = compare_scenarios(amount, fixed_rate, variable_rate_tiers, term_months)
    show_comparison(result)


def main():
    print("=== Loan Amortization Calculator ===\n")
    print("1. Calculate amortization schedule (fixed rate)")
    print("2. Compare fixed rate vs variable rate")
    
    option = input("\nChoose an option (1 or 2): ").strip()
    
    if option == "1":
        regular_amortization_flow()
    elif option == "2":
        comparison_flow()
    else:
        print("Invalid option. Run the program again and choose 1 or 2.")


if __name__ == "__main__":
    main()