from datetime import datetime,timedelta
import os
from fastapi import HTTPException,status,Depends
from jose import JWTError,jwt
from fastapi.security import OAuth2PasswordBearer
from .database import get_db
from . import models
from .schemas import User
from sqlalchemy.orm import Session

SECRET_KEY = os.getenv("APP_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data:dict):
    #Create a copy of the param(username,pwd) dictionary
    to_encode=data.copy()
    #calculate the expiry time of the token and add it to the payload
    token_expires = datetime.utcnow()+timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"token_expires": token_expires.isoformat()})
    #Encode
    return jwt.encode(claims=to_encode,key=SECRET_KEY,algorithm=ALGORITHM)


def verify_access_token(token:str,InvalidCredentialsException,TokenExpiredException):
    try:
        payload=jwt.decode(token=token,key=SECRET_KEY,algorithms=[ALGORITHM])
        username:str=payload['data']
        token_valid_until = datetime.fromisoformat(payload['token_expires'])
        expired:False=token_valid_until<datetime.utcnow()

        if not username:
            raise InvalidCredentialsException
        elif expired:
            raise TokenExpiredException

        return username
    except JWTError as e:
        raise InvalidCredentialsException


def get_user(username:str,db:Session):
    user=db.query(models.User).filter(models.User.email_id == username).first()
    if user:
        return User(id=user.id,first_name=user.first_name, last_name=user.last_name,
        email_id=user.email_id)

#Determines whether or not the an access token is received from the url that was passed
#  in the oauth2schema.
def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):

    InvalidCredentialsException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    TokenExpiredException = HTTPException(
        status_code=status.HTTP_408_REQUEST_TIMEOUT,
        detail="Token has expired",
        headers={"WWW-Authenticate": "Bearer"},
    )

    username = verify_access_token(token,InvalidCredentialsException,TokenExpiredException)
    user = get_user(username=username,db=db)
    print(user.dict())
    return user
