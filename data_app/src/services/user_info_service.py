from api.v1.exceptions import NumberDoesNotExist, NumberIsAlreadyExist
from repositories.base import BaseRepository

from schemas.user_info import UserInfoSchema


class UserinfoService:
    def __init__(self, ui_repo: BaseRepository):
        self.ui_repo = ui_repo

    async def get_address(self, phone_number: str, *, raise_if_not_exists: bool = True) -> str:
        address = await self.ui_repo.get(phone_number)

        if address is None and raise_if_not_exists:
            raise NumberDoesNotExist(phone_number)

        if address is not None:
            address = address.decode()

        return address

    async def get_data(self, phone_number: str) -> str:
        address = await self.get_address(phone_number)
        return address

    async def change_data(self, dto: UserInfoSchema):
        await self.get_address(dto.phone)
        await self.ui_repo.set(dto.phone, dto.address)

    async def write_data(self, dto: UserInfoSchema) -> None:
        address = await self.get_address(dto.phone, raise_if_not_exists=False)

        if address is not None:
            raise NumberIsAlreadyExist(dto.phone)

        await self.ui_repo.set(dto.phone, dto.address)
