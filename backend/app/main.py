from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
from datetime import datetime
from typing import Optional
import openai
from decouple import config

# Initialize FastAPI app
app = FastAPI(title="Healthcare Chatbot API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure OpenAI
openai.api_key = config("OPENAI_API_KEY", default=None)

# Data models
class SymptomRequest(BaseModel):
    symptoms: str

class DiagnosisResponse(BaseModel):
    advice: str
    severity: str
    timestamp: str

# Database file path
DB_FILE = "conversations.json"

def load_conversations():
    """Load conversations from JSON file"""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_conversation(user_input: str, response: str, severity: str):
    """Save conversation to JSON file"""
    conversations = load_conversations()
    
    conversation = {
        "user": user_input,
        "response": response,
        "severity": severity,
        "timestamp": datetime.now().isoformat()
    }
    
    conversations.append(conversation)
    
    with open(DB_FILE, 'w') as f:
        json.dump(conversations, f, indent=2)

def get_healthcare_advice(symptoms: str) -> tuple[str, str]:
    """Get healthcare advice using OpenAI GPT-4"""
    if not openai.api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    
    system_prompt = """You are a healthcare assistant. Your role is to provide helpful guidance for common health concerns while maintaining safety.

For common mild symptoms (cold, cough, mild fever, minor headaches, etc.), suggest simple home remedies like:
- Rest and hydration
- Over-the-counter medications (general guidance only)
- Home care practices

For serious symptoms (chest pain, severe breathing difficulties, high fever >102°F, severe pain, etc.), strongly advise consulting a doctor immediately.

Always classify your response severity as either "mild" or "serious".
Do not prescribe specific medications or provide definitive diagnoses.
Keep responses concise and practical.
End with appropriate disclaimer about consulting healthcare professionals."""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"I have the following symptoms: {symptoms}"}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        advice = response.choices[0].message.content.strip()
        
        # Determine severity based on keywords in the response
        severity_keywords = [
            "doctor", "medical attention", "emergency", "serious", 
            "immediately", "urgent", "hospital", "professional"
        ]
        
        severity = "serious" if any(keyword in advice.lower() for keyword in severity_keywords) else "mild"
        
        return advice, severity
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting AI response: {str(e)}")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Healthcare Chatbot API is running"}

@app.post("/diagnose", response_model=DiagnosisResponse)
async def diagnose_symptoms(request: SymptomRequest):
    """Diagnose symptoms and provide healthcare advice"""
    if not request.symptoms.strip():
        raise HTTPException(status_code=400, detail="Symptoms cannot be empty")
    
    try:
        advice, severity = get_healthcare_advice(request.symptoms)
        
        # Save conversation to database
        save_conversation(request.symptoms, advice, severity)
        
        return DiagnosisResponse(
            advice=advice,
            severity=severity,
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/history")
async def get_conversation_history():
    """Get conversation history"""
    try:
        conversations = load_conversations()
        return {"conversations": conversations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading history: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)