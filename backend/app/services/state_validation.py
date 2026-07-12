from app.constants import JobStatus


def validate_job_status_transition(from_status, to_status):
    if not isinstance(from_status, JobStatus):
        from_status = JobStatus(from_status)
    if not isinstance(to_status, JobStatus):
        to_status = JobStatus(to_status)
    return JobStatus.can_transition(from_status, to_status)
