from typing import Optional
from sqlmodel import SQLModel, Field, select


class User(SQLModel, table=True):
    email: str = Field(primary_key=True)
    first_name: str
    last_name: str
    age: Optional[int] = Field(default=None, index=True)

    @staticmethod
    def get_users(session):
        users = session.exec(select(User)).all()
        return users

    @staticmethod
    def get_one_user(session, email: str):
        user = session.get(User, email)
        return user

    @staticmethod
    def create_user(session, user):
        db_user = User.from_orm(user)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

    def delete_user(self, session):
        session.delete(self)
        session.commit()
