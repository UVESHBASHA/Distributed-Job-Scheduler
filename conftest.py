import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BACKEND = ROOT / "backend"
BACKEND_APP = ROOT / "backend" / "app"
WORKER = ROOT / "worker"
WORKER_APP = ROOT / "worker" / "app"

for path in (BACKEND_APP, WORKER_APP, BACKEND, WORKER):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)
