from .base import AppException

class RepositoryError(AppException):
    pass

class NotFoundError(RepositoryError):
    pass

class DuplicateError(RepositoryError):
    pass

class LimitExceededError(RepositoryError):
    pass