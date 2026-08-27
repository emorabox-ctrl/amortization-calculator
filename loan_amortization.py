from openpyxl import Workbook


def calculate_payment(amount, annual_rate, term_months):
    """
    Calculates the fixed monthly payment for a loan.
    
    amount: loan principal (e.g. 100000)
    annual_rate: annual interest rate as a percentage (e.g. 12 for 12%)
    term_months: number of monthly payments (e.g. 36)
    """
    monthly_rate = (annual_rate / 100) / 12
    
    if monthly_rate == 0:
        return amount / term_months
    
    payment = amount * (monthly_rate * (1 + monthly_rate) ** term_months) / ((1 + monthly_rate) ** term_months - 1)
    
    return payment


def generate_amortization_schedule(amount, annual_rate, term_months, extra_payments=None):
    """
    Generates the full amortization schedule, month by month.
    
    extra_payments: optional dictionary {month: extra_amount}, e.g. {6: 5000}
                     means an extra payment of 5000 in month 6.
    Returns a list of dictionaries with the detail of each installment.
    """
    if extra_payments is None:
        extra_payments = {}
    
    monthly_rate = (annual_rate / 100) / 12
    payment = calculate_payment(amount, annual_rate, term_months)
    
    balance = amount
    schedule = []
    month = 1
    
    while balance > 0.01 and month <= term_months:
        if monthly_rate == 0:
            interest = 0
        else:
            interest = balance * monthly_rate
        
        principal = payment - interest
        extra = extra_payments.get(month, 0)
        
        # If the remaining balance is less than payment + extra, adjust to avoid overpaying
        if principal + extra > balance:
            principal = balance - extra if balance - extra > 0 else balance
            extra = balance - principal if principal == balance else extra
        
        balance = balance - principal - extra
        if balance < 0:
            balance = 0
        
        schedule.append({
            "month": month,
            "payment": payment,
            "interest": interest,
            "principal": principal,
            "extra_payment": extra,
            "balance": balance
        })
        
        month += 1
    
    return schedule


def generate_variable_rate_schedule(amount, rate_tiers, term_months, extra_payments=None):
    """
    Generates the amortization schedule when the interest rate changes over time.
    
    rate_tiers: dictionary {month_from: annual_rate}, e.g. {1: 10, 13: 14, 25: 8}
                 means the rate is 10% from month 1, changes to 14% from month 13, etc.
    Each time the rate changes, the payment is recalculated using the current
    balance as the new principal and the remaining months as the new term.
    """
    if extra_payments is None:
        extra_payments = {}
    
    balance = amount
    schedule = []
    month = 1
    current_rate = rate_tiers[1]  # a rate for month 1 must always exist
    remaining_months = term_months
    payment = calculate_payment(balance, current_rate, remaining_months)
    
    while balance > 0.01 and month <= term_months:
        # Does the rate change this month?
        if month in rate_tiers:
            current_rate = rate_tiers[month]
            remaining_months = term_months - month + 1
            payment = calculate_payment(balance, current_rate, remaining_months)
        
        monthly_rate = (current_rate / 100) / 12
        
        if monthly_rate == 0:
            interest = 0
        else:
            interest = balance * monthly_rate
        
        principal = payment - interest
        extra = extra_payments.get(month, 0)
        
        if principal + extra > balance:
            principal = balance - extra if balance - extra > 0 else balance
            extra = balance - principal if principal == balance else extra
        
        balance = balance - principal - extra
        if balance < 0:
            balance = 0
        
        schedule.append({
            "month": month,
            "annual_rate": current_rate,
            "payment": payment,
            "interest": interest,
            "principal": principal,
            "extra_payment": extra,
            "balance": balance
        })
        
        month += 1
    
    return schedule


def compare_scenarios(amount, fixed_rate, variable_rate_tiers, term_months):
    """
    Compares the total paid under a fixed-rate scenario vs a variable-rate scenario.
    
    Returns a dictionary summarizing both scenarios.
    """
    fixed_schedule = generate_amortization_schedule(amount, fixed_rate, term_months)
    variable_schedule = generate_variable_rate_schedule(amount, variable_rate_tiers, term_months)
    
    total_interest_fixed = sum(row["interest"] for row in fixed_schedule)
    total_interest_variable = sum(row["interest"] for row in variable_schedule)
    
    total_paid_fixed = sum(row["payment"] for row in fixed_schedule)
    total_paid_variable = sum(row["payment"] for row in variable_schedule)
    
    return {
        "total_interest_fixed": total_interest_fixed,
        "total_interest_variable": total_interest_variable,
        "total_paid_fixed": total_paid_fixed,
        "total_paid_variable": total_paid_variable,
        "difference": total_paid_variable - total_paid_fixed
    }


def export_to_excel(schedule, file_name="amortization_schedule.xlsx"):
    """
    Exports an amortization schedule to an Excel file.
    
    schedule: list of dictionaries generated by generate_amortization_schedule,
              generate_variable_rate_schedule, etc.
    file_name: name of the .xlsx file to create
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "Amortization"
    
    has_rate = "annual_rate" in schedule[0]
    
    if has_rate:
        headers = ["Month", "Rate %", "Payment", "Interest", "Principal", "Extra Payment", "Balance"]
    else:
        headers = ["Month", "Payment", "Interest", "Principal", "Extra Payment", "Balance"]
    
    ws.append(headers)
    
    for row in schedule:
        if has_rate:
            ws.append([
                row["month"], row["annual_rate"], round(row["payment"], 2),
                round(row["interest"], 2), round(row["principal"], 2),
                round(row["extra_payment"], 2), round(row["balance"], 2)
            ])
        else:
            ws.append([
                row["month"], round(row["payment"], 2), round(row["interest"], 2),
                round(row["principal"], 2), round(row["extra_payment"], 2), round(row["balance"], 2)
            ])
    
    wb.save(file_name)
    return file_name