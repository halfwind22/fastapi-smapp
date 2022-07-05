from fastapi import Response,status,HTTPException,Depends
from fastapi import APIRouter
from fastapi import Response, status, HTTPException, Depends

from app.oauth2 import get_current_user
from ..schemas import Post, CreateResponseItem, ReadItemVotes, UpdateItem, GetResponseItem, UpdateResponseItem,User
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from .. import models
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

#method:path
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=CreateResponseItem)
async def create_post(payload:Post,db: Session = Depends(get_db),user_payload:User=Depends(get_current_user)):
    """Function to insert posts"""
    #convert pydantic model to a dictionary
    params = payload.dict()
    post = models.Post(title=params['title'],content=params['content'],published=params['published'],user_id=user_payload.dict()['id'])
    db.add(post)
    db.commit()
    #A combination of expire and refresh will flush and retrieve the object attributes modified on the database end in the current session
    db.refresh(post)
    if post:
        return {"message":"Success","payload":post}
    else:
        return {"message":"Failure","payload":None}

@router.get("/",response_model=GetResponseItem,status_code=status.HTTP_200_OK)
async def get_posts(response:Response, db: Session = Depends(get_db),limit:int=10,offset:int=0,q_search:str=None):
    """Function to retrieve posts"""   

    basequery = db.query(models.Post,func.count(models.Vote.post_id).label('votes')).join(models.Vote,models.Post.id==models.Vote.post_id).group_by(models.Vote.post_id)
        
    if q_search:
        posts = basequery.filter(models.Post.content.contains(q_search)).limit(limit=limit).offset(offset=offset).all()
    else:
        posts = basequery.limit(limit=limit).offset(offset=offset).all()
    return {"message":"Success","payload":posts}


@router.get("/{postid}/",response_model=GetResponseItem,status_code=status.HTTP_200_OK)
async def get_post(postid:int, db: Session = Depends(get_db)):
    """Function to retrieve posts based on postid"""

    basequery = db.query(models.Post,func.count(models.Vote.post_id).label('votes')).join(models.Vote,models.Post.id==models.Vote.post_id).group_by(models.Vote.post_id)
    posts = basequery.filter(models.Post.id==postid).all()

    if len(posts)>0:
        return {"message":"Success","payload":posts}
    else:
        msg = {"message":"Failure","payload":posts}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=msg)


@router.delete("/{postid}/",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(postid:int,db: Session = Depends(get_db),user_payload:User=Depends(get_current_user)):
    """Function to delete posts"""

    post = db.query(models.Post).filter(models.Post.id==postid).first()
    if not post:
        msg = {"message":"Post was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=msg)

    if post.user_id==user_payload.dict()['id']:

        db.delete(post)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        msg = {"message":"Post doesnt belong to logged in user"}
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=msg)


@router.put("/{postid}/",status_code=status.HTTP_200_OK,response_model=UpdateResponseItem)
async def update_post(postid:int,payload:UpdateItem,db: Session = Depends(get_db),user_payload:User=Depends(get_current_user)):
    """Function to update posts"""

    posts = db.query(models.Post).filter(models.Post.id==postid)
    post = posts.first()
    if post:
        if post.user_id==user_payload.dict()['id']:
                
            paramdict = payload.dict()
            rows_modified = posts.update(values=paramdict,synchronize_session=False)
            db.commit()
            if rows_modified>0:
                return {"message":"Success","payload":payload.dict()}
        
            else:
                msg = {"message":"Failure","payload":"Updation failed"}
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=msg)
        else:

            msg = {"message":"Post doesnt belong to logged in user"}
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=msg)

    else:
        msg = {"message":"Failure","payload":"Post was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=msg)
