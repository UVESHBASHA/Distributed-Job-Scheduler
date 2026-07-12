import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

from poller import claim_next_job


@patch("poller.SessionLocal")
def test_claim_next_job_claims_next_queued_job(mock_session_local):
    mock_session = mock_session_local.return_value
    mock_result = MagicMock()
    mock_result.mappings.return_value.first.return_value = {
        "id": 7,
        "name": "demo-job",
        "status": "QUEUED",
    }
    mock_session.execute.return_value = mock_result

    claimed_job = claim_next_job(1)

    assert claimed_job is not None
    assert claimed_job["id"] == 7
    assert claimed_job["status"] == "QUEUED"


@patch("poller.SessionLocal")
def test_claim_next_job_returns_none_when_no_job_is_available(mock_session_local):
    mock_session = mock_session_local.return_value
    mock_result = MagicMock()
    mock_result.mappings.return_value.first.return_value = None
    mock_session.execute.return_value = mock_result

    claimed_job = claim_next_job(1)

    assert claimed_job is None
