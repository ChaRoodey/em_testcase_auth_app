from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from app.db.base import Base, intpk


class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str | None] = mapped_column(String(30))
    patronymic: Mapped[str | None] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
