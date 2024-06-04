from fastapi import status
from fastapi import HTTPException


class NumberIsAlreadyExist(HTTPException):
    def __init__(
            self, detail: str = "This number is already exist", status_code=status.HTTP_409_CONFLICT
    ):
        self.detail = detail
        self.status_code = status_code


class NumberDoesNotExist(HTTPException):
    def __init__(
            self, detail: str = "This number does not exist", status_code=status.HTTP_204_NO_CONTENT
    ):
        self.detail = detail
        self.status_code = status_code
