# File: backend/utils/error_handling/db/errors.py

from backend.utils.error_handling.utils.errors import GeneralError

# Base Database Error
class DatabaseError(GeneralError):
    """Base exception for all database-related errors."""
    pass

# Specific Database Errors
class DatabaseConnectionError(DatabaseError):
    """Raised for database connection issues."""
    pass

class SchemaCreationError(DatabaseError):
    """Raised for database schema creation errors."""
    pass

class SessionCommitError(DatabaseError):
    """Raised for errors during database session commits."""
    pass

class UserError(DatabaseError):
    """Raised for user-related database errors."""
    pass

class SecurityError(DatabaseError):
    """Raised for security-related database errors."""
    pass

class LogNotFoundError(DatabaseError):
    """Raised when a log entry is not found."""
    pass

class LogError(DatabaseError):
    """Raised for log-related database errors."""
    pass

class AnalyticsError(DatabaseError):
    """Raised for analytics-related database errors."""
    pass

class ImageError(DatabaseError):
    """Raised for image-related database errors."""
    pass
