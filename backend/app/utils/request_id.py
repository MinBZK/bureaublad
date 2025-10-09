import re

# Maximum length for X-Request-ID to prevent abuse
MAX_REQUEST_ID_LENGTH = 255

# Pattern for valid request IDs (alphanumeric, hyphens, underscores)
# This covers ULIDs, UUIDs, and most common correlation ID formats
REQUEST_ID_PATTERN = re.compile(r"^[a-zA-Z0-9_-]+$")


def validate_request_id(request_id: str | None) -> str | None:
    """
    Validate an incoming X-Request-ID header value.

    Returns the validated request ID if valid, None otherwise.

    Validation rules:
    - Must not be empty
    - Must not exceed MAX_REQUEST_ID_LENGTH characters
    - Must only contain alphanumeric characters, hyphens, and underscores
    - This prevents header injection and malicious values
    """
    if not request_id:
        return None

    request_id = request_id.strip()

    if len(request_id) > MAX_REQUEST_ID_LENGTH:
        return None

    if not REQUEST_ID_PATTERN.match(request_id):
        return None

    return request_id
