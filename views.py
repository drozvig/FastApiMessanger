from fastapi import APIRouter, status, Depends, HTTPException
from schemas import Message_ALL
import models
from database import get_session
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="",
    tags=["Message router"],
)


@router.post(("/"))
def messege(message: Message_ALL, db: Session = Depends(get_session)):
    with db as db:
        message_model = models.Message()
        message_model.text_message = message.text_message
        message_model.author = message.author

        db.add(message_model)
        db.commit()


@router.get(("/"))
def messege_all(db: Session = Depends(get_session)):
    return db.query(models.Message).all()

@router.put(("/{messege_id}"))
def update_messege(messege_id: int,message: Message_ALL,db: Session = Depends(get_session)):
    with db as db:
        message_model = db.query(models.Message).filter(models.Message.id == messege_id).first()

        if message_model is None:
            raise HTTPException(
                status_code=404,
                detail=f"ID {messege_id} : Does not exist"
            )

        message_model.text_message = message.text_message
        message_model.author = message.author
        db.add(message_model)
        db.commit()

        return message

@router.delete(("/{messege_id}"))
def delete_messege(messege_id: int,db: Session = Depends(get_session)):
    message_model = db.query(models.Message).filter(models.Message.id == messege_id).first()
    if message_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {messege_id} : Does not exist"
        )
    db.query(models.Message).filter(models.Message.id == messege_id).delete()
    db.commit()

@router.get(("/{author}"))
def messege_author(author: str, db: Session = Depends(get_session)):
    with db as db:
        return db.query(models.Message).filter(models.Message.author == author).all()
