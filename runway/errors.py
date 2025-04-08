from typing import Optional, Any
import traceback

class RunwayError(Exception):
    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[Any] = None):
        self.message = message
        self.error_code = error_code
        self.details = details
        self.traceback = traceback.format_exc()

    def __str__(self):
        error_str = f"RunwayError: {self.message}"
        if self.error_code:
            error_str += f" (Error Code: {self.error_code})"
        if self.details:
            error_str += f"\nDetails: {self.details}"
        return error_str

class APIKeyError(RunwayError):
    def __init__(self, message: str = "API key is missing or invalid"):
        super().__init__(message, error_code="API_KEY_ERROR")

class ConfigurationError(RunwayError):
    def __init__(self, message: str = "Configuration error occurred"):
        super().__init__(message, error_code="CONFIG_ERROR")

class RouteError(RunwayError):
    def __init__(self, message: str = "Route handling error occurred"):
        super().__init__(message, error_code="ROUTE_ERROR")

class ServerError(RunwayError):
    def __init__(self, message: str = "Server error occurred"):
        super().__init__(message, error_code="SERVER_ERROR")

