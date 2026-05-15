from sqlalchemy.orm import mapped_column, Mapped

from app.db.base import Base, intpk


class RoleModel(Base):
    __tablename__ = 'roles'

    id: Mapped[intpk] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
