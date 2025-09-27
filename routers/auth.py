from datetime import timedelta, timezone
import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from database.db_manager import SessionLocal
from models import Users
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = 'bd0ee123f75849d9ceb810ec9e8e8b45f51a301c5379b79e678376c06b2a83e4'
ALGORITHM = 'HS256'  #makes sure the jwt token is secure

#hash password
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')#url that the client with sent to the api application 

#user will use to login
class CreateUserRequest(BaseModel):
    username:str = Field(..., min_length=3, max_length=50)
    email:str = Field(..., min_length=5, max_length=100)
    first_name:str = Field(..., min_length=2, max_length=50)
    last_name:str = Field(..., min_length=2, max_length=50)
    password:str = Field(..., min_length=6, max_length=100)
    role:str = Field(..., min_length=2, max_length=50)
 

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

#authenticate user function
def authenticate_user(username:str, password:str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user

def create_access_token(username: str, user_id: str, expires_delta: timedelta):
    #create encoding
    encode = {'sub': username, 'id': user_id}
    expires = datetime.datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username:str = payload.get('sub')
        user_id:str = payload.get('id') #get user id from payload
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, 
                      create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        password=bcrypt_context.hash(create_user_request.password), #hashing password using bcrypt
        is_active=True
    )

    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency):

    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')

    token = create_access_token(user.username, user.id, timedelta(minutes=20))
   
    return {'access_token': token, 'token_type': 'bearer'}