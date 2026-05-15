from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from app.db.base import Base, intpk


class ResourcesModel(Base):
    __tablename__ = 'resources'

    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(String(50), unique=True)
