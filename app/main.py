from typing import Optional, List
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas, database
from .database import get_db

from .models import Chat


app = FastAPI()


models.Base.metadata.create_all(bind=database.engine)

@app.get("/drop_chat_table/")
def drop_chat_table():
    Chat.__table__.drop(database.engine)
    return {"message": "Chat table dropped!"}

@app.get("/get_feedback_list/", response_model=List[schemas.FeedbackOut])
def read_feedbacks(db: Session = Depends(get_db)):
    feedbacks = crud.get_feedback_list(db=db)
    return feedbacks


@app.post("/add_chat_feedback/")
def add_chat_feedback(chat_feedback: schemas.ChatFeedback, db: Session = Depends(database.get_db)):
    # Create a chat
    chat = crud.create_chat(db, chat_data=schemas.ChatCreate(
        chat_id=chat_feedback.chat_id,
        chat_title=chat_feedback.chat_title,
        chat_array=chat_feedback.chat_array
    ))

    # Create feedback for the chat
    feedback = crud.create_feedback(db, feedback_data=schemas.FeedbackCreate(
        chat_id=chat_feedback.chat_id,
        user_id=chat_feedback.user_id,
        marked_index=chat_feedback.marked_index,
        created_at=chat_feedback.created_at,
        user_feedback_like=chat_feedback.user_feedback_like,
        user_feedback_string=chat_feedback.user_feedback_string
    ))

    return {"chat": chat, "feedback": feedback}


@app.get("/")  # decorator
def root():
    return {"message": "Hello World"}
