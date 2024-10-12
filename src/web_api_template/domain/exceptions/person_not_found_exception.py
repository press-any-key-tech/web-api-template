from fastapi import HTTPException


class PersonNotFoundException(HTTPException):
    """Domain exception for person not found

    Args:
        HTTPException (HTTPException): inherits from base http exception
    """

    def __init__(self, id: str):
        super().__init__(
            status_code=404,
            detail=f"Person with ID {id} not found",
            headers={"X-Error": "PersonNotFound"},
        )
