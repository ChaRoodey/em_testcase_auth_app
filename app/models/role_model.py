from sqlalchemy.orm import mapped_column, Mapped

from app.db.base import Base, intpk


class RolesModel(Base):
    __tablename__ = 'roles'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(unique=True)
