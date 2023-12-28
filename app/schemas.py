from pydantic import BaseModel
from typing import Any
from datetime import datetime

class ChatCreate(BaseModel):
    chat_id: int
    chat_title: str
    chat_array: Any

class FeedbackCreate(BaseModel):
    chat_id: int
    user_id: str
    marked_index: int
    created_at: datetime = None
    user_feedback_like: str
    user_feedback_string: str

class ChatFeedback(BaseModel):
    chat_id: int
    user_id: str
    marked_index: int
    created_at: datetime = None
    user_feedback_like: str
    user_feedback_string: str
    chat_title: str
    chat_array: Any

class FeedbackOut(BaseModel):
    id: int
    chat_id: int
    user_id: str
    user_feedback_like: str
    user_feedback_string: str
    created_at: datetime = None

class Chat(BaseModel):
    id: int
    chat_id: int
    chat_title: str
    chat_array: Any
    marked_index: int
    user_feedback_like: str
    user_feedback_string: str