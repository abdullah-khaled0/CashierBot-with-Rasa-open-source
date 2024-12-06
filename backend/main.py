from fastapi import FastAPI
import requests
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for the frontend
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str

@app.post("/chat")
async def chat_with_rasa(user_message: Message):
    rasa_url = "http://localhost:5005/webhooks/rest/webhook"
    response = requests.post(rasa_url, json={"sender": "user", "message": user_message.message})
    bot_response = response.json()
    return {"response": bot_response}

