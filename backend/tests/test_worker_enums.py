import pytest

from app.constants import JobStatus, RetryStrategy
from app.models.job import Job


def test_job_status_enum_values_are_supported():
    assert JobStatus.QUEUED.value == "QUEUED"
    assert JobStatus.RUNNING.value == "RUNNING"
    assert JobStatus.SUCCEEDED.value == "SUCCEEDED"
    assert JobStatus.FAILED.value == "FAILED"


def test_retry_strategy_enum_values_are_supported():
    assert RetryStrategy.NONE.value == "NONE"
    assert RetryStrategy.EXPONENTIAL.value == "EXPONENTIAL"
    assert RetryStrategy.LINEAR.value == "LINEAR"


def test_job_status_transition_validation():
    job = Job(status=JobStatus.QUEUED.value)

    assert JobStatus.can_transition(JobStatus.QUEUED, JobStatus.RUNNING) is True
    assert JobStatus.can_transition(JobStatus.RUNNING, JobStatus.SUCCEEDED) is True
    assert JobStatus.can_transition(JobStatus.RUNNING, JobStatus.FAILED) is True
    assert JobStatus.can_transition(JobStatus.QUEUED, JobStatus.FAILED) is False
