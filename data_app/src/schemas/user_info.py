from pydantic import Field, field_validator, ValidationInfo
from pydantic_extra_types.phone_numbers import PhoneNumber

from schemas.base import Base

PhoneNumber.phone_format = 'E164'
PhoneNumber.min_length = 11
PhoneNumber.default_region_code = "RU"


class PhoneDataSchema(Base):
    phone: PhoneNumber = Field(description="Номер телефона", example="89090000000")


class AddressDataSchema(Base):
    address: str = Field(max_length=255, description="Адрес")


class UserInfoSchema(AddressDataSchema, PhoneDataSchema):
    ...
