import httpx
import base64
import json
import os
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
from dotenv import load_dotenv



load_dotenv()
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

client_id = os.getenv("QUICKBOOKS_CLIENT_ID")
client_secret = os.getenv("QUICKBOOKS_CLIENT_SECRET")
base_url = os.getenv("QUICKBOOKS_BASE_URL")
base_auth_url = os.getenv("QUICKBOOKS_OAUTH_URL")


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
    
class RefreshToken(BaseModel):
    refresh_token: str

@app.get("/login_quickbooks/")
async def login_quickbooks():
    auth_url = auth_client.get_authorization_url(scopes)
    print("Please visit the following URL to authorize your app:")
    print(auth_url)
    return {"auth_url": auth_url}  # Redirect to this URL

@app.post("/get_token")
async def get_token(auth_code: AuthCode):
    token_endpoint = base_auth_url+ "/v1/tokens/bearer"
    redirect_uri = "https://klib-accounting.vercel.app/profile/autorize_quickbook/" 
    auth_header = 'Basic ' + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': auth_header
    }
    data = {
        'code': auth_code.code,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(token_endpoint, data=data, headers=headers)
        if r.status_code != 200:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        bearer_raw = r.json()

        return bearer_raw  
    
@app.post("/get_bearer_token_from_refresh")
async def get_bearer_token_from_refresh(refresh_token: RefreshToken):
    token_endpoint = base_auth_url +"/v1/tokens/bearer"
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {encoded_credentials}'
    }
    data = {
    'grant_type': 'refresh_token',
    'refresh_token': refresh_token.refresh_token
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(token_endpoint, data=data, headers=headers)

        if response.status_code == 200:
            # Successfully refreshed the token
            return (response.json())
        else:
            # Failed to refresh the token
            return (f"Failed to refresh tokens: {response.text}")

@app.post("/get_company_info/")
async def get_company_info(auth_code: AuthCode):
    # Construct the query
    query = "SELECT * FROM CompanyInfo"

    # Construct the full endpoint URL
    token_endpoint = f"{base_url}/v3/company/{auth_code.realm_id}/query?query={query}"

    # Implement the logic to obtain the access token using auth_code
    # This is an example and needs to be replaced with actual token acquisition logic
    access_token = auth_code.code

    # Set up the headers
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(token_endpoint, headers=headers)

        if response.status_code == 200:
            # Successfully refreshed the token
            return (response.json())
        else:
            # Failed to refresh the token
            return (f"Failed to refresh tokens: {response.text}")

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
