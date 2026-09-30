from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = {
    "tenure_months",
    "monthly_charges",
    "support_calls",
    "contract_type",
    "churn"
}

VALID_CONTRACT_TYPES = {"month-to-month", "one-year", "two-year"}
VALID_PAYMENT_METHODS = {"electronic-check", "credit-card", "bank-transfer"}

def validate_dataframe(df: pd.DataFrame) -> tuple[bool, list[str]]:
    """
    This function validates a DataFrame against the required schema and constraints.

    Args:
        df (pd.DataFrame): The DataFrame to validate.
    
    Returns:
        Bool: True if the DataFrame is valid, False otherwise.
        List[str]: A list of error messages if the DataFrame is invalid.
    """

    errors = []
    missing_columns = REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        errors.append(f"Missing columns: {sorted(missing_columns)}")
    if len(df) < 100:
        errors.append("DataFrame must contain at least 100 rows.")
    if df.isnull().any().any():
        errors.append("DataFrame contains missing values." )
    if "churn" in df.columns and not df["churn"].isin([0, 1]).all():
        errors.append("Column 'churn' must only contain 0 or 1.")
    if "contract_type" in df.columns and not df["contract_type"].isin(VALID_CONTRACT_TYPES).all():
        errors.append("Invalid contract type detected.")
    if "payment_method" in df.columns and not df["payment_method"].isin(VALID_PAYMENT_METHODS).all():
        errors.append("Invalid payment method detected.")

    return (len(errors) == 0, errors)

def validate_csv(path: str) -> bool:
    """
    This function validates a CSV file against the required schema and constraints.

    Args:
        path (str): The path to the CSV file.

    Returns:
        bool: True if the CSV file is valid, False otherwise.
    """

    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    df = pd.read_csv(path)
    ok, errors = validate_dataframe(df)
    if not ok:
        raise ValueError("\n".join(errors))
    print(f"Validation passed for {path} with {len(df)} rows.")
    return True

if __name__ == "__main__":
    validate_csv("data/raw/customer_churn.csv")