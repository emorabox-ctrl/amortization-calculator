import os
from loan_amortization import calculate_payment, generate_amortization_schedule, generate_variable_rate_schedule, compare_scenarios, export_to_excel


def test_calculate_payment_basic():
    result = calculate_payment(100000, 12, 36)
    assert round(result, 2) == 3321.43


def test_schedule_final_balance_close_to_zero():
    schedule = generate_amortization_schedule(100000, 12, 36)
    last_balance = schedule[-1]["balance"]
    assert abs(last_balance) < 1  # rounding tolerance


def test_schedule_has_correct_number_of_months():
    schedule = generate_amortization_schedule(50000, 10, 24)
    assert len(schedule) == 24


def test_calculate_payment_zero_rate():
    result = calculate_payment(120000, 0, 12)
    assert round(result, 2) == 10000.00


def test_schedule_zero_rate():
    schedule = generate_amortization_schedule(120000, 0, 12)
    
    for row in schedule:
        assert round(row["payment"], 2) == 10000.00
        assert round(row["interest"], 2) == 0.00
        assert round(row["principal"], 2) == 10000.00
    
    assert schedule[-1]["balance"] == 0


def test_schedule_with_extra_payment_reduces_term():
    schedule_without_extra = generate_amortization_schedule(100000, 12, 36)
    schedule_with_extra = generate_amortization_schedule(100000, 12, 36, {6: 20000})
    
    assert len(schedule_with_extra) < len(schedule_without_extra)
    assert schedule_with_extra[5]["extra_payment"] == 20000
    assert abs(schedule_with_extra[-1]["balance"]) < 1


def test_variable_rate_schedule_changes_payment_correctly():
    schedule = generate_variable_rate_schedule(100000, {1: 10, 13: 14}, 24)
    
    for row in schedule[:12]:
        assert row["annual_rate"] == 10
    
    for row in schedule[12:]:
        assert row["annual_rate"] == 14
    
    assert schedule[11]["payment"] != schedule[12]["payment"]
    assert abs(schedule[-1]["balance"]) < 1


def test_compare_scenarios_correct_structure():
    result = compare_scenarios(100000, 12, {1: 10, 13: 14}, 24)
    
    expected_keys = {"total_interest_fixed", "total_interest_variable",
                      "total_paid_fixed", "total_paid_variable", "difference"}
    assert set(result.keys()) == expected_keys
    
    calculated_difference = result["total_paid_variable"] - result["total_paid_fixed"]
    assert round(result["difference"], 2) == round(calculated_difference, 2)


def test_export_to_excel_creates_file():
    schedule = generate_amortization_schedule(100000, 12, 12)
    file_name = "test_export_temp.xlsx"
    
    result = export_to_excel(schedule, file_name)
    
    assert result == file_name
    assert os.path.exists(file_name)
    
    os.remove(file_name)