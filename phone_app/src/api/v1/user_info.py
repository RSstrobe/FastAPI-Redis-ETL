from fastapi import APIRouter, status, Query, Depends

from services.user_info_service import get_user_info_srvice, UserinfoService
from schemas.user_info import UserInfoSchema, PhoneDataSchema

router = APIRouter(tags=["User info"])


@router.post(
    "/write_data",
    status_code=status.HTTP_201_CREATED,
    description="Записать информацию и номере и адресе",
    summary="Записать информацию и номере и адресе",
    response_model=PhoneDataSchema,
)
async def write_data(
        request: UserInfoSchema = UserInfoSchema,
        service: UserinfoService = Depends(get_user_info_srvice)
):
    ...
    await service.write_data(request)
    return PhoneDataSchema(phone=request.phone)


@router.patch(
    "/write_data",
    status_code=status.HTTP_200_OK,
    description="Записать информацию и номере и адресе",
    summary="Записать информацию и номере и адресе",
    response_model=UserInfoSchema,
)
async def change_data(
        request: UserInfoSchema = UserInfoSchema,
        service: UserinfoService = Depends(get_user_info_srvice)
):
    response = await service.change_data(request)
    return response


@router.get(
    "/check_data",
    status_code=status.HTTP_200_OK,
    description="Получить сведения о наличии подписки",
    summary="Получить сведения о наличии подписки",
    response_model=UserInfoSchema,
)
async def check_data(
        phone: str = Query(description="Номер телефона"),
        service: UserinfoService = Depends(get_user_info_srvice)
):
    response = await service.check_data(phone)
    return response
