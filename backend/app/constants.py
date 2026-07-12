from enum import Enum


class JobStatus(str, Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"

    @classmethod
    def can_transition(cls, from_status, to_status):
        allowed = {
            cls.QUEUED: {cls.RUNNING},
            cls.RUNNING: {cls.SUCCEEDED, cls.FAILED},
            cls.SUCCEEDED: set(),
            cls.FAILED: set(),
        }
        return to_status in allowed.get(from_status, set())


class RetryStrategy(str, Enum):
    NONE = "NONE"
    EXPONENTIAL = "EXPONENTIAL"
    LINEAR = "LINEAR"


class WorkerStatus(str, Enum):
    ACTIVE = "ACTIVE"
    IDLE = "IDLE"
    STOPPED = "STOPPED"
