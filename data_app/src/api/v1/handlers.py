from fastapi import APIRouter, status, Query

from deps import UserDataService
from schemas.user_info import UserInfoSchema, PhoneDataSchema

data_router = APIRouter(prefix='/data', tags=['user_info'])


@data_router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    description="Записать информацию и номере и адресе",
    summary="Записать информацию и номере и адресе",
    response_model=PhoneDataSchema,
)
async def write_data(
        service: UserDataService,
        request: UserInfoSchema = UserInfoSchema
):
    await service.write_data(request)
    return PhoneDataSchema(phone=request.phone)


@data_router.patch(
    path="",
    status_code=status.HTTP_200_OK,
    description="Записать информацию и номере и адресе",
    summary="Записать информацию и номере и адресе",
    response_model=UserInfoSchema,
)
async def change_data(
        service: UserDataService,
        request: UserInfoSchema = UserInfoSchema
):
    await service.change_data(request)
    return request


@data_router.get(
    path="",
    status_code=status.HTTP_200_OK,
    description="Получить сведения о наличии подписки",
    summary="Получить сведения о наличии подписки",
    response_model=UserInfoSchema,
)
async def get_data(
        service: UserDataService,
        phone: str = Query(description="Номер телефона")
):
    address = await service.get_data(phone)
    return UserInfoSchema(phone=phone, address=address)
