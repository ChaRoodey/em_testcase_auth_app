from pydantic import BaseModel, EmailStr, ConfigDict


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserRegisterSchema(UserLoginSchema):
    first_name: str
    last_name: str | None = None
    patronymic: str | None = None


class UserResponseSchema(UserLoginSchema):
    id: int | None = None
    is_active: bool | None = None
