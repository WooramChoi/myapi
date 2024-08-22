from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from .common import Base, TimestampMixin

class Board(TimestampMixin, Base):
    __tablename__ = "board_info"

    seq_board: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[Optional[str]] = mapped_column(String(9000))
    plain_text: Mapped[Optional[str]] = mapped_column(String(3000))
    yn_use: Mapped[bool] = mapped_column(default=True)
    name: Mapped[Optional[str]] = mapped_column(String(100))
    pwd: Mapped[Optional[str]] = mapped_column(String(255))