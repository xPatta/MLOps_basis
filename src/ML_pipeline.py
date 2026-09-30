import sys, subprocess, os
from config import LAB_ROOT, VERBOSE

env = os.environ.copy()
env["PYTHONPATH"] = str((LAB_ROOT / "src").resolve())

# Generate data
subprocess.run([sys.executable, "-m", "data_generation"], cwd=LAB_ROOT, env=env, check=True)

# Test data validation pipeline
result = subprocess.run([sys.executable, "-m", "pytest", "-v"], cwd=LAB_ROOT, env=env, text=True, capture_output=True)
if VERBOSE:
    print(result.stdout)
if result.returncode != 0:
    print(result.stdout)
    print(result.stderr)
    raise SystemExit(result.returncode)
print("Validation Test passed.")
# Validate generated data
subprocess.run([sys.executable, "-m", "data_validation"], cwd=LAB_ROOT, env=env, check=True)          