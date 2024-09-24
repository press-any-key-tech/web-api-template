from fastapi import HTTPException


class PersonAlreadyExistsException(HTTPException):
    """Domain exception for person already exists

    Args:
        HTTPException (HTTPException): inherits from base http exception
    """

    def __init__(self, id: str):
        super().__init__(
            status_code=409,
            detail=f"Person with the identification number {id} already exists",
            headers={"X-Error": "PersonAlreadyExists"},
        )
