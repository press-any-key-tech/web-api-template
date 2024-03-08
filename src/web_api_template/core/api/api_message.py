from pydantic import BaseModel


class ApiMessage(BaseModel):
    """Api response object

    Args:
        BaseModel (_type_): pydantic base model
    """

    message: str
    error_code: int
