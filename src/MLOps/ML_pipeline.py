import sys, subprocess, os
from MLOps.config import LAB_ROOT

env = os.environ.copy()
env["PYTHONPATH"] = str((LAB_ROOT / "src").resolve())

# Generate data
subprocess.run([sys.executable, "-m", "MLOps.data_generation"], cwd=LAB_ROOT, env=env, check=True)

# Test data validation pipeline
result = subprocess.run([sys.executable, "-m", "pytest", "-v"], cwd=LAB_ROOT, env=env, text=True, capture_output=True)
if result.returncode != 0:
    print(result.stdout)
    print(result.stderr)
raise SystemExit(f"Validation Test failed. Returncode: {result.returncode}"if result.returncode != 0 else "Validation Test passed.")

# Validate generated data
subprocess.run([sys.executable, "-m", "MLOps.data_validation"], cwd=LAB_ROOT, env=env, check=True)          