from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func

from datetime import datetime

class Base(DeclarativeBase):
    pass

class TimestampMixin:
    dt_create: Mapped[datetime] = mapped_column(default=func.now())
    dt_update: Mapped[datetime] = mapped_column(default=func.now())