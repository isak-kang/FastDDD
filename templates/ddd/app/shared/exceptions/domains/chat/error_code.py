from enum import Enum


class ChatErrorCode(Enum):
    CHAT_ERROR = (400, "CHAT_001", "Chat request failed.")
    CHAT_MESSAGE_NOT_FOUND = (404, "CHAT_002", "Chat message not found.")
    CHAT_PROVIDER_FAILED = (500, "CHAT_003", "Chat provider request failed.")
