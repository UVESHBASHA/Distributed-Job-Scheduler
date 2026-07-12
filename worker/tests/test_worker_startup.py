import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

from worker import register_worker


@patch("worker.SessionLocal")
def test_register_worker_handles_database_error(mock_session_local):
    mock_session = mock_session_local.return_value
    mock_session.execute.side_effect = Exception("database unavailable")

    try:
        register_worker()
    except Exception as exc:
        assert "database unavailable" in str(exc)
    else:
        assert False, "register_worker should raise when the database is unavailable"
