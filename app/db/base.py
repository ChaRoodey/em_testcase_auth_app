from typing import Annotated

from sqlalchemy.orm import DeclarativeBase, mapped_column

intpk = Annotated[int, mapped_column(primary_key=True)]


class Base(DeclarativeBase):
    ...
