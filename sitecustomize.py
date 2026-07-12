import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
for candidate in (ROOT / 'backend', ROOT / 'worker'):
    if candidate.exists() and str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

# Ensure the backend app package is importable from the repository root.
backend_app = ROOT / 'backend' / 'app'
if backend_app.exists() and str(backend_app) not in sys.path:
    sys.path.insert(0, str(backend_app))

worker_app = ROOT / 'worker' / 'app'
if worker_app.exists() and str(worker_app) not in sys.path:
    sys.path.insert(0, str(worker_app))
