import re
from fastapi import Header, Request, Depends


class ContentType:
    def __init__(self, request: Request):
        self.content_type = request.headers.get("content-type")


def generate_slug(text: str) -> str:
    """Generate slug from a string

    Args:
        text (str): _description_

    Returns:
        str: _description_
    """

    # Change to lowercas
    slug: str = text.lower()
    # Replace no desired chars by dash
    slug = re.sub(r"[\s_]+", "-", slug)
    # Delete no alfanumerical chars
    slug = re.sub(r"[^\w-]", "", slug)
    # Delete dashes at the beginning or end
    slug = slug.strip("-")
    return slug


def get_content_type(ct: ContentType = Depends()) -> str | None:
    """Get content type from header parameters
        Utility function to use as Depends on api controllers
    Args:
        content_type (str, optional): _description_. Defaults to Header(None).

    Returns:
        _type_: _description_
    """
    return ct.content_type
