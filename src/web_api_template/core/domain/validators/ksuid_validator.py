import re


def ksuid_validator(ksuid: str) -> str:
    """Validates ksuid format."""

    if not re.match(r"^[a-zA-Z0-9]{27}$", ksuid):
        raise ValueError("Invalid KSUID format")
    return ksuid
