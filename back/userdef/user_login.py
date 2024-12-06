from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from zenitdb.app import app
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import select, Column, String, text

from sqlalchemy.orm import Session
from zenitdb.database import engine, get_db

from zenitdb.models import User


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 600


class Token(BaseModel):
    access_token: str
    token_type: str

class UserInDB(User):
    pass


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    # print(pwd_context.hash(password))
    return pwd_context.hash(password)


def get_user(user_login: str):
    db = Session(engine)
    stmt = select(UserInDB).where(UserInDB.user_login == user_login)
    user = db.scalars(stmt).first()
    return user



def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        if username == "admin":
            print("Admin not found. please run SQL against your DB.")
            print(f"Insert into user (user_login, user_pass) Values \n     ('admin', '{get_password_hash(password)}');")
        return False
    if not verify_password(password, user.user_pass):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user


@app.post("/login", tags=['Auth'])
async def user_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
) -> Token:
    # get_password_hash(form_data.password)
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.user_login,
            "project_id": 17,
            "accessLevel":"admin"
        }, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get('/whoami', tags=["Auth"])
def WhoAmI(user: dict = Depends(get_current_user)
          ,db: Session = Depends(get_db)):
    
    user.user_pass = None
    return user

from zenitdb.schemas import User
from .usercontrol import raiseError

@app.post('/auth/register', tags=["Auth"])
def user_register(user_login: str, 
                  new_pass: str, 
                  the_User: User, 
                  user: dict = Depends(get_current_user),
                  db: Session = Depends(get_db)
                  ) -> User:
    if user.id != 1:
        raiseError(403, "NO_ACCESS", msg="Only user id 1 Can add users")

    userd = get_user(user_login)
    if userd != None:
        raiseError(403, "USER_LOGIN_REPEAT", msg="this user_login used before", 
                   ctx=userd.user_name)

    udb = UserInDB(user_login=user_login, 
                   user_pass=get_password_hash(new_pass), 
                   **the_User.model_dump())
    db.add(udb)
    db.commit()
    db.refresh(udb)
    return udb

@app.post('/auth/reset', tags=["Auth"])
def user_register(user_login: str, 
                  new_pass: str, 
                  user: dict = Depends(get_current_user),
                  db: Session = Depends(get_db)
                  ):
    stmt = select(UserInDB).where(UserInDB.user_login == user_login)
    userd = db.scalars(stmt).first()
    if userd == None:
        raiseError(404, 'NOT_FOUND', msg="Can't Find user")
    
    if user.id != 1 or user.id != userd.id:
        raiseError(403, "NO_ACCESS", msg="Only user id 1 Can reset passwords")

    userd.user_pass = get_password_hash(new_pass)
    db.commit()
    
    return True

