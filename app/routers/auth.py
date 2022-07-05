from fastapi import APIRouter
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models
from .. import schemas
from ..utils import verify
from ..oauth2 import create_access_token,get_current_user

router=APIRouter(
    prefix="/login",
    tags=["Login"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def user_login(params: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_db)):
    """Function to perform login"""

    user=db.query(models.User).filter(models.User.email_id == params.username).first()
    if user:
        if verify(params.password, user.password):
            access_token=create_access_token({"data": params.username})
            return {"access_token": access_token, "token_type": "bearer"}
        else:
            msg={"message": "Failure", "payload": "Incorrect password"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)


    else:
        msg={"message": "Failure", "payload": "User does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
