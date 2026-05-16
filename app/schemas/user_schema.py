from pydantic import BaseModel, EmailStr


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserRegisterSchema(UserLoginSchema):
    first_name: str
    last_name: str | None = None
    patronymic: str | None = None


class UserWithIdSchema(UserLoginSchema):
    id: int | None = None


class UserResponseSchema(UserRegisterSchema):
    id: int | None = None
    role_id: str | None = None
    is_active: bool | None = None
