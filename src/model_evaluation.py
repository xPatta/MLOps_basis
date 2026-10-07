import json, os
from config import LAB_ROOT, VERBOSE, ACCURACY_THRESHOLD, F1_SCORE_THRESHOLD

os.chdir(LAB_ROOT)

# Metrics gate: checks accuracy and f1_score against thresholds
metrics = json.loads((LAB_ROOT /"reports" /"metrics.json").read_text())
thresholds = {"accuracy": ACCURACY_THRESHOLD, "f1_score": F1_SCORE_THRESHOLD}

for metric, minimum in thresholds.items():
    actual = metrics.get(metric)
    status = "✓" if actual >= minimum else "✗"
    if VERBOSE:
        print(f"{status} {metric}: actual={actual} required={minimum}")
    if actual < minimum:
        raise SystemExit(f"Model promotion gate failed: {metric} below threshold")

print("\n Model promotion gate passed - ready for serving")
print(json.dumps(metrics, indent=2))