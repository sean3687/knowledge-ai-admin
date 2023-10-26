from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import relationship

from sqlalchemy import DateTime, func
from .database import Base



class Chat(Base):
    __tablename__ = "chats"

    chat_id = Column(Integer, primary_key=True, index=True)
    chat_title = Column(String)
    chat_array = Column(JSON)
    feedbacks = relationship("Feedback", back_populates="chat")

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)  # New primary key for feedback
    chat_id = Column(Integer, ForeignKey('chats.chat_id'))  # ForeignKey to chats table
    user_id = Column(String)
    marked_index = Column(Integer)
    created_at = Column(DateTime(timezone=True), default=func.now())
    user_feedback_like = Column(String)  # like or dislike
    user_feedback_string = Column(String)  # user feedback string

    # Relationship
    chat = relationship("Chat", back_populates="feedbacks")