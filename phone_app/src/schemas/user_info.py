from pydantic import Field, constr

from schemas.base import Base


class PhoneDataSchema(Base):
    phone: constr(
        pattern=r"8^\d{10}$")  # = Field(description="Номер телефона")  # накинуть валидацию и убрать - TODO: добавить коммент про либу phonenumber


class AddressDataSchema(Base):
    # Может ли адрес быть пустым?
    address: str = Field(max_length=255, description="Адрес")


class UserInfoSchema(AddressDataSchema, PhoneDataSchema):
    ...
