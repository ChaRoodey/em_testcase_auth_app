from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from app.db.base import Base


class ResourcesModel(Base):
    __tablename__ = 'resources'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), unique=True)
