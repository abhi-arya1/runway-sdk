from pydantic import BaseModel
from typing import Literal
from enum import Enum


class StatusCode(Enum):
    SUCCESS = 200
    ERROR = 500
    NOT_FOUND = 404
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504
    BAD_GATEWAY = 502
    REQUEST_TIMEOUT = 408
    CONFLICT = 409
    GONE = 410