from enum import Enum

class StatusCode(Enum):
    OK = 200
    CREATED = 201
    SUCCESS = 200
    NOT_FOUND = 404
    SERVER_ERROR = 500
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    BAD_REQUEST = 400
    NO_RESPONSE = 0
    TOO_MANY_REQUESTS = 429
    CONFLICT = 409