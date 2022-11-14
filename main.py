from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session

from models import User
from db import create_db_and_tables, get_session

description = """
Fastapi-sqlmodel API is the base for a CRUD mixing the properties of Pydantic and SQLAlchemist. 🚀

## Users

You can 
* **Read users**.
* **Create a user**
* **Delete a user**
"""

app = FastAPI(
    title="fastapi-sqlmodel",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.verisure.com/terms/",
    contact={
        "name": "Adrian Sacristan",
        "url": "http://example.verisure.com",
        "email": "adrian@verisure.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def users_get(session: Session = Depends(get_session)):
    return User.get_users(session)


@app.delete("/<user_email>")
def users_delete(user_email: str, session: Session = Depends(get_session)):
    user = User.get_one_user(session, user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.delete_user(session)
    return {'message': 'Ok'}


@app.post("/", response_model=User)
def users_create(user: User, session: Session = Depends(get_session)):
    user = User.create_user(session, user)
    return user
