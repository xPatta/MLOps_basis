
    # Customer Churn Model Card"

    ## Purpose
    Predict whether a customer is at risk of churn.

    ## Features
    tenure_months, monthly_charges, support_calls, contract_type, payment_method

    ## Algorithm
    RandomForestClassifier inside a scikit-learn Pipeline.

    ## Metrics
    {
  "accuracy": 0.636,
  "precision": 0.4375,
  "recall": 0.7467,
  "f1_score": 0.5517,
  "training_rows": 750,
  "test_rows": 250
}

    ## Limitations
    This is a synthetic training dataset for learning Devops for ML.
    It should not be used for real customer decisions.

    ## Operational notes
    The model should be retrained when data drift is detected or when
    performance drops below the accepted threshold.
    