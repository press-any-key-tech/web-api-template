from fastapi import HTTPException


class AddressNotFoundException(HTTPException):
    """Domain exception for address not found

    Args:
        HTTPException (HTTPException): inherits from base http exception
    """

    def __init__(self, id: int):
        super().__init__(
            status_code=404,
            detail=f"Address with ID {id} not found",
            headers={"X-Error": "AddressNotFound"},
        )
