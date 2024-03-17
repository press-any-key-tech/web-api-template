import re


def slug_validator(v):
    if v is not None and not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", v):
        raise ValueError("Invalid slug format")
    return v
