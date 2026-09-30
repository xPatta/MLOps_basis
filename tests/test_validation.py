import pandas as pd
from data_validation import validate_dataframe

def valid_df():
    return pd.DataFrame({
        "tenure_months": [12, 24, 36] * 40,
        "monthly_charges": [50.0, 75.5, 91.2] * 40,
        "support_calls": [0, 1, 2] * 40,
        "contract_type": ["month-to-month", "one-year", "two-year"] * 40,
        "payment_method": ["credit-card", "electronic-check", "bank-transfer"] * 40,
        "churn": [0, 1, 0] * 40
    })

def test_valid_dataframe_passes():
    ok, errors = validate_dataframe(valid_df())
    assert ok is True
    assert errors == []

def test_missing_column_fails():
    df = valid_df().drop(columns=["churn"])
    ok, errors = validate_dataframe(df)
    assert ok is False
    assert any("Missing columns" in error for error in errors)

def test_invalid_target_fails():
    df = valid_df()
    df.loc[0, "churn"] = 7  # Invalid value (must be in {0, 1})
    ok, errors = validate_dataframe(df)
    assert ok is False
    assert any("Column 'churn' must only contain 0 or 1." in error for error in errors)