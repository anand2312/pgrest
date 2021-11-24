from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class PostgrestError(Exception):
    """
    Base Postgrest exception.

    Raised mainly for HTTP status codes: 400, 500
    """

    message: str
    """The error message raised"""
    hint: Optional[str]
    """Hint about the error"""
    code: str
    """The PostgreSQL error code that was raised"""
    details: Optional[str]
    """Details about the error"""
    http_status: int
    """The HTTP status code recieved"""


class UndefinedResourceError(PostgrestError):
    """
    Raised for HTTP status codes: 404

    - undefined function, table
    """


class AuthenticationError(PostgrestError):
    """
    Raised for HTTP status codes: 403

    - invalid grantor
    - invalid role specification
    - insufficient privileges (while authenticated)
    - invalid auth specification
    """


class DatabaseError(PostgrestError):
    """
    Raised for HTTP status codes: 503

    - pg connection error
    - insufficient resources
    """


class ConstraintViolation(PostgrestError):
    """
    Raised for HTTP status codes: 409

    - foreign key violation
    - uniqueness violation
    """
