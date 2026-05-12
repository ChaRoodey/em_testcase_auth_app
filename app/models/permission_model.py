from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from app.db.base import Base


class PermissionModel(Base):
    __tablename__ = 'permissions'

    id: Mapped[int] = mapped_column(primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    resource_id: Mapped[int] = mapped_column(ForeignKey("resources.id"))
    can_read: Mapped[bool] = mapped_column(Boolean, default=True)
    can_create: Mapped[bool] = mapped_column(Boolean, default=False)
    can_update: Mapped[bool] = mapped_column(Boolean, default=False)
    can_delete: Mapped[bool] = mapped_column(Boolean, default=False)
