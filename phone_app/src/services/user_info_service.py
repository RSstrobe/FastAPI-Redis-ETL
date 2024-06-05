from fastapi import Depends

from helpers.exceptions import NumberDoesNotExist, NumberIsAlreadyExist
from repositories.redis_repository import get_redis_repo, RedisRepository
from repositories.base import BaseRepository
from schemas.user_info import UserInfoSchema, AddressDataSchema


class UserinfoService:
    def __init__(self, ui_repo: BaseRepository):
        self.ui_repo = ui_repo

    async def check_data(self, phone_number: str) -> UserInfoSchema:
        response = await self.ui_repo.get(phone_number)

        if not response:
            raise NumberDoesNotExist

        return UserInfoSchema(phone=phone_number, address=response["address"])

    async def change_data(self, dto: UserInfoSchema) -> UserInfoSchema:
        await self.check_data(dto.phone)

        await self.ui_repo.set(dto.phone, AddressDataSchema(address=dto.address).json())

        return dto

    async def write_data(self, dto: UserInfoSchema) -> None:
        user_info = await self.ui_repo.get(dto.phone)

        if user_info:
            raise NumberIsAlreadyExist

        await self.ui_repo.set(dto.phone, AddressDataSchema(address=dto.address).json())


async def get_user_info_srvice(ui_repo: RedisRepository = Depends(get_redis_repo)) -> UserinfoService:
    return UserinfoService(ui_repo=ui_repo)
