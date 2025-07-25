from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Album(Base):
    __tablename__ = "album"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(125))
    artist: Mapped[str] = mapped_column(String(80))
    cover_url: Mapped[str] = mapped_column(String(255))

    def __repr__(self) -> str:
        return f"Album(name={self.name!r}, artist={self.artist!r}, cover_url={self.cover_url!r})"
