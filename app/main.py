import httpx
import base64
import json
from typing import Optional, List
from fastapi import FastAPI, Depends, Request, APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas, database
from .database import get_db
from .models import Chat
from authlib.integrations.starlette_client import OAuth
from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from starlette.datastructures import URL
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")
router = APIRouter()
app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

auth_client = AuthClient(
    "AB5NRJWFzxcviA6iUeJ62G7wpT1NdJYFlg3rGXogomoICL6aaD",
    "PS5nk7fSrTm63eAVtzx17cOeNUYeg5Pgpp2BGd50",
    "https://klib-accounting.vercel.app/profile/autorize_quickbook/",
    "sandbox" 
)
scopes = [Scopes.ACCOUNTING]


models.Base.metadata.create_all(bind=database.engine)

class AuthCode(BaseModel):
    code: str
    realm_id: str

@app.get("/login_quickbooks/")
async def login_quickbooks():
    auth_url = auth_client.get_authorization_url(scopes)
    print("Please visit the following URL to authorize your app:")
    print(auth_url)
    return {"auth_url": auth_url}  # Redirect to this URL

@app.post("/autorize_quickbook/")
async def auth(auth_code: AuthCode ):
    response = auth_client.get_bearer_token(auth_code = auth_code.code, realm_id=auth_code.realm_id)
    print(response)
    return {"access_token": response}

@app.post("/get_token")
async def get_token(auth_code: AuthCode):
    token_endpoint = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
    client_id = "AB5NRJWFzxcviA6iUeJ62G7wpT1NdJYFlg3rGXogomoICL6aaD"  # Replace with your client ID
    client_secret = "PS5nk7fSrTm63eAVtzx17cOeNUYeg5Pgpp2BGd50"  # Replace with your client secret
    redirect_uri = "https://klib-accounting.vercel.app/profile/autorize_quickbook/"  # Replace with your redirect URI

    auth_header = 'Basic ' + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': auth_header
    }
    payload = {
        'code': auth_code.code,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(token_endpoint, data=payload, headers=headers)
        if r.status_code != 200:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        bearer_raw = r.json()

        # Extract the fields you need from bearer_raw and return
        return bearer_raw  # Or a subset of this data
    
@app.get("/update_access_token/")
async def update_access_token(refresh_token: str):
    
    return
    

@app.get("/get_company_info/")
async def get_company_info(request: Request):
    access_token = request.headers.get('Authorization')
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token is missing")

    # Assuming auth_client is already configured elsewhere in your code
    return auth_client.client.get_company_info(access_token)

@app.get("/drop_chat_table/")
def drop_chat_table():
    Chat.__table__.drop(database.engine)
    return {"message": "Chat table dropped!"}

@app.get("/get_feedback_list/", response_model=List[schemas.FeedbackOut])
def read_feedbacks(db: Session = Depends(get_db)):
    feedbacks = crud.get_feedback_list(db=db)
    return feedbacks

app.get("/get_conversation/{chat_id}", response_model=schemas.Chat)
def get_conversation(db : Session = Depends(get_db)):
    chat = crud.get_conversation(db=db)
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat


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
