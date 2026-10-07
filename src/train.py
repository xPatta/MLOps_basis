from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

FEATURES = ["tenure_months", "monthly_charges", "support_calls", "contract_type", "payment_method"]
TARGET = "churn"

def build_pipeline():
    # Define Features
    categorical = ["contract_type", "payment_method"] # will need numerical encoder e.g. 1-hot
    numeric = ["tenure_months", "monthly_charges", "support_calls"]

    # Define Preprocessor
    preprocessor = ColumnTransformer(
        transformers=[("categorical", OneHotEncoder(handle_unknown=  "ignore"), categorical),
                ("numeric", "passthrough", numeric),
        ]
    )

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=6,
        random_state=42,
        class_weight="balanced",
    )

    return Pipeline([
        ("preprocessor", preprocessor),
        ("model", model),
    ])


def train_mode(data_path="data/raw/customer_churn.csv"):
    # Retrieve data
    df = pd.read_csv(data_path)
    X = df[FEATURES]
    y = df[TARGET]

    # Split dataset into train and test sets (75|25 random split, stratified)
    X_train, X_test, y_train, y_test = train_test_split( 
    X, y, test_size=0.25, random_state=42, stratify=y

    )

    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)
    predictions = pipeline.predict(X_test)

    metrics = {
        "accuracy": round(accuracy_score(y_test, predictions), 4),
        "precision": round(precision_score(y_test, predictions, zero_division=0), 4),
        "recall": round(recall_score(y_test, predictions, zero_division=0), 4),
        "f1_score": round(f1_score(y_test, predictions, zero_division=0), 4),
        "training_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
    }
    


    Path("models").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)

    # Save the trained model and metrics
    joblib.dump(pipeline, "models/churn_model.joblib")
    Path("reports/metrics.json").write_text(json.dumps(metrics, indent=2))

    # Build model card without backtick fences (avoids SyntaxError in triple-quoted string)
    metrics_json = json.dumps(metrics, indent=2)
    model_card = f"""
    # Customer Churn Model Card"

    ## Purpose
    Predict whether a customer is at risk of churn.

    ## Features
    {", ".join(FEATURES)}

    ## Algorithm
    RandomForestClassifier inside a scikit-learn Pipeline.

    ## Metrics
    {metrics_json}

    ## Limitations
    This is a synthetic training dataset for learning Devops for ML.
    It should not be used for real customer decisions.

    ## Operational notes
    The model should be retrained when data drift is detected or when
    performance drops below the accepted threshold.
    """

    Path("reports/model_card.md").write_text(model_card)
    return metrics

if __name__ == "__main__":
    metrics = train_mode()
    print("Training completed. Metrics:")
    print(json.dumps(metrics, indent=2))