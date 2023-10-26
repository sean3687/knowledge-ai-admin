from sqlalchemy.orm import Session
from . import models, schemas

def create_chat(db: Session, chat_data: schemas.ChatCreate):
    db_chat = models.Chat(
        chat_id=chat_data.chat_id, 
        chat_title=chat_data.chat_title, 
        chat_array=chat_data.chat_array
    )
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat


def create_feedback(db: Session, feedback_data: schemas.FeedbackCreate):
    db_feedback = models.Feedback(
        chat_id=feedback_data.chat_id, 
        user_id=feedback_data.user_id, 
        marked_index= feedback_data.marked_index,
        created_at=feedback_data.created_at,
        user_feedback_like=feedback_data.user_feedback_like, 
        user_feedback_string=feedback_data.user_feedback_string
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback


def get_feedback_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Feedback).offset(skip).limit(limit).all()