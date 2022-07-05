from typing import List
from fastapi import FastAPI, Response,status,HTTPException,Depends
from sqlalchemy.orm import Session
from app.database import engine,get_db
from ..schemas import User,Vote
from .. import models
from .. import oauth2
from fastapi import APIRouter

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def do_vote(payload:Vote,db:Session=Depends(get_db),current_user:User=Depends(oauth2.get_current_user)):
    "Help user to vote a post"
    
    post_id = payload.dict()['post_id']
    direction = payload.dict()['direction']
    user_id = current_user.id

    check_vote = db.query(models.Post).filter(models.Post.id==post_id).first()
    if not check_vote:
        msg={"message":"Failure","payload":"Post not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=msg)
        
    existing_vote = db.query(models.Vote).filter(models.Vote.post_id==post_id,models.Vote.user_id==user_id).first()

    if existing_vote:
        if direction:
            msg={"message":"Failure","payload":"Vote already exists"}
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=msg)

        elif not direction:
            db.delete(existing_vote)
            db.commit();         
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        if direction:
            vote=models.Vote(post_id=post_id,user_id=user_id)           
            db.add(vote)
            db.commit()
            db.refresh(vote)
            if vote:
                return {"message":"Success","payload":vote}
            else:
                return {"message":"Failure","payload":None}

        elif not direction:
            msg={"message":"Failure","payload":"Vote doesnt exist"}
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=msg)