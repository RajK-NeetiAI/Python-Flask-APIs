from sqlalchemy import select

from src.models.bookmark_model import Bookmark
from src.database.connect import Session


def create_bookmark(bookmark: Bookmark) -> bool:
    with Session() as session:
        session.begin()
        try:
            session.add(bookmark)
        except:
            session.rollback()
            return False
        else:
            session.commit()
            return True


def get_bookmark_by_url(url: str) -> Bookmark:
    with Session() as session:
        statement = select(Bookmark).filter_by(url=url, is_deleted=False)
        bookmark = session.scalars(statement).one_or_none()
        return bookmark


def get_bookmarks(user_id: int) -> list[Bookmark]:
    with Session() as session:
        statement = select(Bookmark).filter_by(
            user_id=user_id, is_deleted=False)
        bookmarks = session.scalars(statement).all()
        formated_bookmarks = []
        for bm in bookmarks:
            formated_bookmarks.append(bm._asdict())
        return formated_bookmarks


def get_bookmark_by_id(id: int, user_id: int) -> Bookmark | None:
    with Session() as session:
        statement = select(Bookmark).filter_by(
            id=id, user_id=user_id, is_deleted=False)
        bookmark = session.scalars(statement).one_or_none()
        if bookmark:
            return bookmark._asdict()
        else:
            return None


def update_bookmark_by_id(id: int, update: dict) -> bool:
    with Session() as session:
        session.begin()
        try:
            session.query(Bookmark).filter(Bookmark.id == id).update(update)
        except:
            session.rollback()
            return False
        else:
            session.commit()
            return True


def get_bookmark_by_shorten_url(shorten_url: str, user_id: int) -> dict | None:
    with Session() as session:
        statement = select(Bookmark).filter_by(
            shorten_url=shorten_url, is_deleted=False, user_id=user_id)
        bookmark = session.scalars(statement).one_or_none()
        if bookmark:
            return bookmark._asdict()
        else:
            return None
