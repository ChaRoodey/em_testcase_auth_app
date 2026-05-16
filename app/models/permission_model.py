from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from app.db.base import Base, intpk


class PermissionsModel(Base):
    __tablename__ = 'permissions'

    id: Mapped[intpk]
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    resource_id: Mapped[int] = mapped_column(ForeignKey("resources.id"))
    can_read: Mapped[bool] = mapped_column(default=True)
    can_all_read: Mapped[bool] = mapped_column(default=False)
    can_create: Mapped[bool] = mapped_column(default=False)
    can_all_create: Mapped[bool] = mapped_column(default=False)
    can_update: Mapped[bool] = mapped_column(default=False)
    can_all_update: Mapped[bool] = mapped_column(default=False)
    can_delete: Mapped[bool] = mapped_column(default=False)
    can_all_delete: Mapped[bool] = mapped_column(default=False)
