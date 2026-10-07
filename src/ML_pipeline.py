import sys, subprocess, os
from config import LAB_ROOT, VERBOSE, MODELS, REPORTS

env = os.environ.copy()
env["PYTHONPATH"] = str((LAB_ROOT / "src").resolve())

# Generate data
subprocess.run([sys.executable, "-m", "data_generation"], cwd=LAB_ROOT, env=env, check=True)

# Test data validation pipeline
result = subprocess.run([sys.executable, "-m", "pytest", "-v", "-p no:cacheprovider"], cwd=LAB_ROOT, env=env, text=True, capture_output=True)
if VERBOSE:
    print(result.stdout)
if result.returncode != 0:
    print(result.stdout)
    print(result.stderr)
    raise SystemExit(result.returncode)
print("Validation Test passed.")
# Validate generated data
subprocess.run([sys.executable, "-m", "data_validation"], cwd=LAB_ROOT, env=env, check=True)          

# Train model
subprocess.run([sys.executable, "-m", "train"], cwd=LAB_ROOT, env=env, check=True)

if VERBOSE:
    print("Model training completed. Artifacts:")
    print(" -", MODELS / "churn_model.joblib" if (MODELS / "churn_model.joblib").exists() else "no model found")
    print(" -", REPORTS / "metrics.json" if (REPORTS / "metrics.json").exists() else "no metrics found")
    print(" -", REPORTS / "model_card.md" if (REPORTS / "model_card.md").exists() else "no model card found")