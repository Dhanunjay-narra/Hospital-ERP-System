from fastapi import HTTPException, status
from typing import Any, Optional, Dict

class AppException(HTTPException):
    def __init__(self, status_code: int, detail: str, error_code: Optional[str] = None, data: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code or "APP_ERROR"
        self.data = data or {}

class NotFoundError(AppException):
    def __init__(self, detail: str = "Resource not found", data: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail, error_code="NOT_FOUND", data=data)

class UnauthorizedError(AppException):
    def __init__(self, detail: str = "Could not validate credentials", data: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, error_code="UNAUTHORIZED", data=data)

class ForbiddenError(AppException):
    def __init__(self, detail: str = "Access forbidden: insufficient permissions", data: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail, error_code="FORBIDDEN", data=data)

class ConflictError(AppException):
    def __init__(self, detail: str = "Resource already exists", data: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail, error_code="CONFLICT", data=data)

class ValidationError(AppException):
    def __init__(self, detail: str = "Validation failed", data: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail, error_code="VALIDATION_ERROR", data=data)
