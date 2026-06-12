from enum import Enum


class AuthErrorCode(Enum):
    AUTH_ERROR = (401, "AUTH_001", "Authentication failed.")
    INVALID_TOKEN = (401, "AUTH_002", "Invalid token.")
    PERMISSION_DENIED = (403, "AUTH_003", "Permission denied.")
    AUTH_USER_NOT_FOUND = (400, "AUTH_018", "Auth User not found")
