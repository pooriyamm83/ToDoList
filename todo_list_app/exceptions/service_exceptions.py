from .base import AppException

class ServiceError(AppException):
    pass

class ValidationError(ServiceError):
    pass