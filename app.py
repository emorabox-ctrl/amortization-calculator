import streamlit as st
from loan_amortization import generate_amortization_schedule, generate_variable_rate_schedule, compare_scenarios, export_to_excel

st.set_page_config(page_title="Loan Amortization Calculator", layout="centered")

st.title("Loan Amortization Calculator")

option = st.sidebar.radio(
    "Choose an option:",
    ["Amortization schedule", "Compare fixed vs variable rate"]
)

if option == "Amortization schedule":
    st.header("Calculate Amortization Schedule")
    
    amount = st.number_input("Loan amount", min_value=0.0, value=100000.0, step=1000.0)
    annual_rate = st.number_input("Annual interest rate (%)", min_value=0.0, value=12.0, step=0.5)
    term_months = st.number_input("Term (months)", min_value=1, value=36, step=1)
    
    st.subheader("Extra payments (optional)")
    st.write("Add extra payments to principal for specific months, if you want to simulate them.")
    
    num_extra = st.number_input("How many extra payments do you want to add?", min_value=0, value=0, step=1)
    
    extra_payments = {}
    for i in range(int(num_extra)):
        col1, col2 = st.columns(2)
        with col1:
            month = st.number_input(f"Month #{i+1}", min_value=1, max_value=int(term_months), key=f"month_{i}")
        with col2:
            extra_amount = st.number_input(f"Amount #{i+1}", min_value=0.0, key=f"amount_{i}")
        if extra_amount > 0:
            extra_payments[int(month)] = extra_amount
    
    if st.button("Calculate"):
        schedule = generate_amortization_schedule(amount, annual_rate, int(term_months), extra_payments)
        
        st.success(f"Total months paid: {len(schedule)}")
        
        st.dataframe(schedule, use_container_width=True)
        
        file_name = export_to_excel(schedule, "amortization_schedule.xlsx")
        with open(file_name, "rb") as f:
            st.download_button(
                label="Download as Excel",
                data=f,
                file_name=file_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

else:
    st.header("Compare Fixed Rate vs Variable Rate")
    
    amount = st.number_input("Loan amount", min_value=0.0, value=100000.0, step=1000.0)
    term_months = st.number_input("Term (months)", min_value=1, value=24, step=1)
    fixed_rate = st.number_input("Fixed annual rate (%)", min_value=0.0, value=12.0, step=0.5)
    
    st.subheader("Variable rate tiers")
    st.write("Define the rate for each period. The first tier must start at month 1.")
    
    num_tiers = st.number_input("How many rate tiers?", min_value=1, value=2, step=1)
    
    rate_tiers = {}
    for i in range(int(num_tiers)):
        col1, col2 = st.columns(2)
        with col1:
            month = st.number_input(f"Starts at month #{i+1}", min_value=1, max_value=int(term_months), key=f"tier_month_{i}")
        with col2:
            rate = st.number_input(f"Rate (%) #{i+1}", min_value=0.0, key=f"tier_rate_{i}")
        rate_tiers[int(month)] = rate
    
    if st.button("Compare"):
        if 1 not in rate_tiers:
            st.warning("Warning: no rate was defined for month 1. Please review your tiers.")
        else:
            result = compare_scenarios(amount, fixed_rate, rate_tiers, int(term_months))
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total paid (fixed)", f"{result['total_paid_fixed']:.2f}")
                st.metric("Total interest (fixed)", f"{result['total_interest_fixed']:.2f}")
            with col2:
                st.metric("Total paid (variable)", f"{result['total_paid_variable']:.2f}")
                st.metric("Total interest (variable)", f"{result['total_interest_variable']:.2f}")
            
            difference = result["difference"]
            if difference > 0:
                st.error(f"The variable rate is MORE EXPENSIVE by {difference:.2f}")
            elif difference < 0:
                st.success(f"The variable rate is CHEAPER by {abs(difference):.2f}")
            else:
                st.info("Both scenarios cost exactly the same.")