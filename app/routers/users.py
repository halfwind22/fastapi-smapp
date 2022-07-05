from typing import List
from fastapi import FastAPI, Response,status,HTTPException,Depends
from sqlalchemy.orm import Session
from app.database import engine,get_db
from ..utils import hash_string
from ..schemas import CreateResponseUser,ReadUserInput
from .. import models
from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=CreateResponseUser)
async def create_user(payload:ReadUserInput,db: Session = Depends(get_db)):
    """Function to insert posts"""

    #convert pydantic model to a dictionary
    params = payload.dict()
    params['password'] = hash_string(params['password'])
    user = models.User(first_name=params['first_name'],last_name=params['last_name'],email_id=params['email_id'],password=params['password'])
    db.add(user)
    db.commit()
    #A combination of expire and refresh will flush and retrieve the object attributes modified on the database end in the current session
    db.refresh(user)
    if user:
        return {"message":"Success","payload":user}
    else:
        return {"message":"Failure","payload":None}

@router.get("/{userid}/",response_model=CreateResponseUser,status_code=status.HTTP_200_OK)
async def get_user(userid:int, db: Session = Depends(get_db)):
    """Function to retrieve user based on userid"""

    users = db.query(models.User).filter(models.User.id==userid).all()

    if len(users)>0:
        return {"message":"Success","payload":users[0]}
    else:
        msg = {"message":"Failure","payload":users}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=msg)
