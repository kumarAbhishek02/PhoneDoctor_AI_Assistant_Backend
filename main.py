import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@app.post("/chat")
async def chat(message: dict):
    prompt = message.get("message", "")

    # Healthcare filter
    if not any(word in prompt.lower() for word in 
        ["health", "pain", "fever", "medicine", "disease", "injury", "symptom", "cough", "doctor"]):
        return {"reply": "I can only help with healthcare related topics."}

    # NEW Gemini 2.5 Flash endpoint
    url = (
        "https://generativelanguage.googleapis.com/v1/models/"
        "gemini-2.5-flash:generateContent?key=" + GEMINI_API_KEY
    )

    # NEW request format for Gemini 2.5
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": f"You are a healthcare assistant. {prompt}"}
                ]
            }
        ]
    }

    response = requests.post(url, json=payload)
    
    print("Status:", response.status_code)
    print("Response:", response.text)

    # Catch invalid API response → avoid "null" error
    if not response.ok:
        return {"reply": "Server error: Unable to process request."}

    data = response.json()

    try:
        reply = data["candidates"][0]["content"]["parts"][0]["text"]
    except:
        reply = "I couldn't understand the response."

    return {"reply": reply}


@app.get("/")
def root():
    return {"message": "Server is running"}
