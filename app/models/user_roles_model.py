from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from app.db.base import Base


class UserRolesModel(Base):
    __tablename__ = 'users-roles'

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
