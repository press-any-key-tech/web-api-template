from fastapi import HTTPException


class PersonAlreadyModifiedException(HTTPException):
    """Domain exception for person already modified

    Args:
        HTTPException (HTTPException): inherits from base http exception
    """

    def __init__(self, id: str):
        super().__init__(
            status_code=409,
            detail=f"Person with the id {id} already modified by another process",
            headers={"X-Error": "PersonAlreadyModified"},
        )
