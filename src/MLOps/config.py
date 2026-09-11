from pathlib import Path
import sys

LAB_ROOT = Path("")
SRC = LAB_ROOT / "src"/"MLOps"
TEST = LAB_ROOT / "tests"
DATA = LAB_ROOT / "data"/ "raw"
MODELS = LAB_ROOT / "models"
REPORTS = LAB_ROOT / "reports"
WORKFLOWS = LAB_ROOT / ".github"/ "workflows"


if __name__ == "__main__":
    for p in [SRC, TEST, DATA, MODELS, REPORTS, WORKFLOWS]:
        p.mkdir(parents=True, exist_ok=True)
    (SRC / "__init__.py").touch() 
    if str(SRC) not in sys.path:
	    sys.path.insert(0, str(SRC))
    print(f"Project structure created at {LAB_ROOT.resolve()}")