from datetime import datetime

from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase


from src.models.user_model import User


class BookmarkBase(DeclarativeBase):
    pass


class Bookmark(BookmarkBase):
    __tablename__ = 'bookmarks'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    url: Mapped[str] = mapped_column(String(128))
    remarks: Mapped[str] = mapped_column(String(256))
    visits: Mapped[int] = mapped_column(Integer)
    shorten_url: Mapped[str] = mapped_column(String(128))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(User.id), nullable=False, index=True)

    def __repr__(self) -> str:
        return f'{self.id} -> {self.shorten_url}.'
