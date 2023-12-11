from werkzeug.security import check_password_hash
from sqlalchemy import select

from src.models.user_model import User
from src.database.connect import Session


def create_user(user: User) -> bool:
    with Session() as session:
        session.begin()
        try:
            session.add(user)
        except:
            session.rollback()
            return False
        else:
            session.commit()
            return True


def get_user_by_email(email: str) -> User | None:
    with Session() as session:
        statement = select(User).filter_by(email=email)
        user = session.scalars(statement).one_or_none()
        return user


def verify_user(email: str, password: str) -> User | None:
    user = get_user_by_email(email)
    if user:
        _ = check_password_hash(user.hashed_password, password)
        return user
    else:
        return None
