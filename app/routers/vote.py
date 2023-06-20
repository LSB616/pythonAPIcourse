from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2, database
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(
    prefix="/vote",
    tags=['Votes']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    #checks if post exists
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post With ID: {vote.post_id} Does Not Exist")

    #checks if vote alreadyt exists
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} Has Already Voted On Post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfuly Added Vote"}  
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote Does Not Exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully Deleted Vote"}