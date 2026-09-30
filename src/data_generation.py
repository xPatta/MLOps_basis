from pathlib import Path
import pandas as pd
import numpy as np


def generate_customer_churn_data(path = "data/raw/customer_churn.csv", n_rows = 1000, seed = 42):
    """
    Generate synthetic customer churn data and save it to a CSV file.

    Parameters:
    path (str): The file path to save the generated CSV file.
    n_rows (int): The number of rows of data to generate.
    seed (int): The random seed for reproducibility.

    Returns:
    None
    """
    rng = np.random.default_rng(seed)
    
    tenure_months = rng.integers(1, 72, n_rows)
    monthly_charges = rng.normal(70, 20, n_rows).clip(20, 120).round(2)
    support_calls = rng.poisson(2, n_rows)
    contract_type = rng.choice(["month-to-month", "one-year", "two-year"], size=n_rows, p=[0.55, 0.30, 0.15])
    payment_method = rng.choice(["electronic-check", "credit-card", "bank-transfer"], size=n_rows)

    # Create realistic churn probabilities based on user features
    churn_probability = (
        0.20
        + (contract_type == "month-to-month") * 0.25
        + (support_calls > 3) * 0.20
        + (monthly_charges > 90) * 0.10
        - (tenure_months > 36) * 0.15
    )
    
    churn = rng.binomial(1, churn_probability)
    
    df = pd.DataFrame({
        "tenure_months": tenure_months,
        "monthly_charges": monthly_charges,
        "support_calls": support_calls,
        "contract_type": contract_type,
        "payment_method": payment_method,
        "churn": churn
    })
    
    path = Path(path)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)

    print(f"Customer churn data generated and saved to {path}")

    return path


if __name__ == "__main__":
    generate_customer_churn_data()
