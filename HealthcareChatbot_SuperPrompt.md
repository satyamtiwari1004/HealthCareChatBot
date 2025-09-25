# 🧩 Super Prompt — Healthcare Chatbot Project

I want to build a **Healthcare Chatbot** using **OpenAI GPT-4**. The chatbot should:
- Accept symptoms (e.g., cold, fever, cough) as input from users
- Provide intelligent health guidance with severity assessment (mild/serious)
- Suggest simple home remedies for mild cases
- Recommend consulting a doctor for serious conditions
- Display chat in a **React TypeScript frontend** with **ChatGPT/Gemini-style UI** 
- Backend in **FastAPI (Python)** with OpenAI integration
- Store interactions in a **JSON file database**
- Include comprehensive **documentation** and **troubleshooting guides**
- **CRITICAL**: Ensure all code is syntactically correct and tested before delivery

---

## ✅ Tech Stack & Requirements
- **Backend**: FastAPI 0.104.1 + Python 3.8+ + OpenAI GPT-4 (API v0.28.1)
- **Frontend**: React 19 + TypeScript + Create React App + Axios
- **Database**: JSON file-based storage (`conversations.json`)
- **Styling**: Custom CSS with healthcare-focused design
- **Dependencies**: Node.js 16+, Python 3.8+, Valid OpenAI API Key
- **Development**: Local development setup (production-ready architecture)

---

## 🛠️ Step-by-Step Build Instructions

### 1. Project Structure Setup
**Create this exact folder structure:**
```
HealthCare ChatBot/
├── .env                     # Environment variables
├── .env.example            # Environment template
├── README.md               # Main project documentation
├── backend/
│   ├── app/
│   │   └── main.py          # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── start.sh            # Backend startup script
├── frontend/               # React TypeScript app
├── docs/                   # Documentation folder
└── conversations.json      # JSON database (auto-generated)
```

### 2. Environment Configuration
**Create `.env` file in project root:**
```env
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
```

**Create `.env.example` template:**
```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**Get OpenAI API Key:**
1. Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Create new secret key
3. Copy and paste into `.env` file
4. Ensure you have credits in your OpenAI account

### 3. Backend Implementation (FastAPI)

**File: `backend/requirements.txt`**
```txt
fastapi==0.104.1
uvicorn==0.24.0
openai==0.28.1
pydantic==2.5.0
python-decouple==3.8
python-multipart==0.0.6
```

**File: `backend/start.sh` (executable script)**
```bash
#!/bin/bash
# Healthcare Chatbot Backend Startup Script
echo "🏥 Starting Healthcare Chatbot Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check for environment file
if [ ! -f "../.env" ]; then
    echo "⚠️  No .env file found. Please copy .env.example to .env and add your OpenAI API key."
    exit 1
fi

# Start the server
echo "🚀 Starting FastAPI server..."
cd app && python main.py
```

**File: `backend/app/main.py` (Complete FastAPI implementation)**
```python
import json
import os
from datetime import datetime
from typing import Dict, Any

import openai
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from decouple import config

# Initialize FastAPI app
app = FastAPI(
    title="Healthcare Chatbot API",
    description="AI-powered healthcare assistance with OpenAI GPT-4",
    version="1.0.0"
)

# CORS configuration for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI configuration
openai.api_key = config('OPENAI_API_KEY')

# Pydantic models
class SymptomRequest(BaseModel):
    symptoms: str

class DiagnosisResponse(BaseModel):
    advice: str
    severity: str
    timestamp: str

# Healthcare system prompt
SYSTEM_PROMPT = """
You are a helpful healthcare assistant. Analyze the user's symptoms and provide appropriate guidance.

For MILD symptoms (common cold, mild headache, minor cuts):
- Provide home remedies and self-care advice
- Suggest over-the-counter treatments if appropriate
- Mark severity as "mild"

For SERIOUS symptoms (chest pain, severe fever >102°F, difficulty breathing, severe injuries):
- Recommend immediate medical attention
- Advise contacting a doctor or emergency services
- Mark severity as "serious"

Always include appropriate disclaimers about consulting healthcare professionals.
Be concise but helpful. Do not diagnose specific medical conditions.
"""

# Conversations storage
CONVERSATIONS_FILE = "../../conversations.json"

def load_conversations():
    if os.path.exists(CONVERSATIONS_FILE):
        with open(CONVERSATIONS_FILE, 'r') as f:
            return json.load(f)
    return {"conversations": []}

def save_conversation(user_input: str, ai_response: str, severity: str):
    data = load_conversations()
    conversation = {
        "user": user_input,
        "response": ai_response,
        "severity": severity,
        "timestamp": datetime.now().isoformat()
    }
    data["conversations"].append(conversation)
    
    with open(CONVERSATIONS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.get("/")
async def root():
    return {"message": "Healthcare Chatbot API is running"}

@app.post("/diagnose", response_model=DiagnosisResponse)
async def diagnose_symptoms(request: SymptomRequest):
    try:
        # Call OpenAI GPT-4
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Symptoms: {request.symptoms}"}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content.strip()
        
        # Determine severity based on keywords
        serious_keywords = [
            "doctor", "emergency", "hospital", "serious", "severe", 
            "immediate", "urgent", "medical attention", "911"
        ]
        
        severity = "serious" if any(keyword in ai_response.lower() for keyword in serious_keywords) else "mild"
        
        # Save conversation
        save_conversation(request.symptoms, ai_response, severity)
        
        return DiagnosisResponse(
            advice=ai_response,
            severity=severity,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/history")
async def get_conversation_history():
    return load_conversations()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

### 4. Frontend Implementation (React + TypeScript)

**Create React app:**
```bash
npx create-react-app frontend --template typescript
cd frontend
npm install axios
```

**File: `frontend/src/App.tsx` (Complete React implementation)**
```typescript
import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
  severity?: string;
}

interface ApiResponse {
  advice: string;
  severity: string;
  timestamp: string;
}

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Add welcome message
    const welcomeMessage: Message = {
      id: 'welcome',
      text: 'Hello! I\'m your healthcare assistant. Please describe your symptoms, and I\'ll provide some guidance. Remember, this is for informational purposes only and doesn\'t replace professional medical advice.',
      isUser: false,
      timestamp: new Date(),
      severity: 'mild'
    };
    setMessages([welcomeMessage]);
  }, []);

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputValue,
      isUser: true,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await axios.post<ApiResponse>(`${API_BASE_URL}/diagnose`, {
        symptoms: inputValue
      });

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: response.data.advice,
        isUser: false,
        timestamp: new Date(),
        severity: response.data.severity
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: 'Sorry, I encountered an error. Please make sure the backend server is running and try again.',
        isUser: false,
        timestamp: new Date(),
        severity: 'serious'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="App">
      <div className="chat-container">
        <div className="chat-header">
          <h1>🩺 Healthcare Assistant</h1>
          <p>Get guidance for your health concerns</p>
        </div>
        
        <div className="chat-messages">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`message ${message.isUser ? 'user-message' : 'bot-message'} ${
                message.severity === 'serious' ? 'serious-message' : ''
              }`}
            >
              <div className="message-content">
                <div className="message-text">{message.text}</div>
                <div className="message-timestamp">
                  {message.timestamp.toLocaleTimeString()}
                </div>
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="message bot-message">
              <div className="message-content">
                <div className="typing-indicator">
                  <div className="typing-dot"></div>
                  <div className="typing-dot"></div>
                  <div className="typing-dot"></div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
        
        <div className="chat-input">
          <div className="input-container">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Describe your symptoms (e.g., 'I have a fever and cough')..."
              disabled={isLoading}
              rows={1}
            />
            <button 
              onClick={sendMessage}
              disabled={!inputValue.trim() || isLoading}
              className="send-button"
            >
              Send
            </button>
          </div>
        </div>
        
        <div className="disclaimer">
          ⚠️ This chatbot provides general advice only. Always consult a qualified doctor for serious or persistent conditions.
        </div>
      </div>
    </div>
  );
}

export default App;
```

### 5. 🎨 Frontend Styling (CRITICAL - VALIDATE CSS SYNTAX)

**File: `frontend/src/App.css` (Healthcare-focused design)**

**🚨 IMPORTANT: This CSS must be syntactically perfect. Validate before implementing.**

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f7f7f8;
}

.App {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.chat-container {
  width: 90%;
  max-width: 800px;
  height: 90vh;
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-header {
  background: linear-gradient(135deg, #2196F3, #21CBF3);
  color: white;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.chat-header h1 {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 5px;
}

.chat-header p {
  font-size: 14px;
  opacity: 0.9;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background-color: #f7f7f8;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message {
  display: flex;
  max-width: 80%;
  animation: fadeIn 0.3s ease-in;
}

.user-message {
  align-self: flex-end;
}

.bot-message {
  align-self: flex-start;
}

.message-content {
  background: white;
  border-radius: 18px;
  padding: 12px 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: relative;
}

.user-message .message-content {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  margin-left: 40px;
}

.bot-message .message-content {
  background: white;
  color: #333;
  margin-right: 40px;
  border: 1px solid #e0e0e0;
}

.serious-message .message-content {
  border-left: 4px solid #f44336;
  background: #ffebee;
}

.message-text {
  font-size: 15px;
  line-height: 1.5;
  margin-bottom: 4px;
  word-wrap: break-word;
}

.message-timestamp {
  font-size: 11px;
  opacity: 0.7;
  text-align: right;
}

.user-message .message-timestamp {
  color: rgba(255, 255, 255, 0.8);
}

.typing-indicator {
  display: flex;
  gap: 4px;
  align-items: center;
  padding: 8px 0;
}

.typing-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #999;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-dot:nth-child(1) { animation-delay: -0.32s; }
.typing-dot:nth-child(2) { animation-delay: -0.16s; }
.typing-dot:nth-child(3) { animation-delay: 0s; }

@keyframes typing {
  0%, 80%, 100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

.chat-input {
  padding: 16px 20px;
  background: white;
  border-top: 1px solid #e0e0e0;
}

.input-container {
  display: flex;
  gap: 12px;
  align-items: flex-end;
}

.input-container textarea {
  flex: 1;
  min-height: 44px;
  max-height: 120px;
  border: 2px solid #e0e0e0;
  border-radius: 22px;
  padding: 12px 16px;
  font-size: 15px;
  font-family: inherit;
  resize: none;
  outline: none;
  transition: border-color 0.2s;
}

.input-container textarea:focus {
  border-color: #667eea;
}

.input-container textarea:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.send-button {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 50%;
  width: 44px;
  height: 44px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.send-button:hover:not(:disabled) {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.send-button:disabled {
  background: #ccc;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.disclaimer {
  background: #fff3cd;
  color: #856404;
  padding: 12px 20px;
  font-size: 12px;
  text-align: center;
  border-top: 1px solid #ffeaa7;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  .chat-container {
    width: 100%;
    height: 100vh;
    border-radius: 0;
  }
  
  .message {
    max-width: 90%;
  }
  
  .user-message .message-content {
    margin-left: 20px;
  }
  
  .bot-message .message-content {
    margin-right: 20px;
  }
  
  .chat-header h1 {
    font-size: 20px;
  }
  
  .input-container textarea {
    font-size: 16px; /* Prevent zoom on iOS */
  }
}

/* Scrollbar styling */
.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}
```

**🚨 CSS VALIDATION CHECKLIST:**
- All opening braces `{` have matching closing braces `}`
- All CSS properties end with semicolons `;`
- No orphaned keyframe rules (all have matching `@keyframes`)
- No incomplete media queries
- Test compilation with `npm start` immediately after adding CSS

### 6. 📚 Complete Documentation Suite

**Create `README.md` in project root with:**
```markdown
# 🩺 Healthcare Chatbot

A modern healthcare assistant chatbot powered by OpenAI GPT-4 that provides guidance for common health concerns while maintaining safety standards.

![Healthcare Chatbot](https://img.shields.io/badge/Python-FastAPI-blue)
![React](https://img.shields.io/badge/Frontend-React%20TypeScript-61dafb)
![OpenAI](https://img.shields.io/badge/AI-OpenAI%20GPT--4-green)

## ✨ Features

- **Intelligent Health Guidance**: Uses OpenAI GPT-4 to provide healthcare advice
- **Severity Assessment**: Automatically categorizes symptoms as mild or serious
- **Modern Chat Interface**: ChatGPT/Gemini-style UI with smooth animations
- **Conversation History**: Stores all interactions in JSON database
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Safety First**: Includes appropriate medical disclaimers and recommendations

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **OpenAI API Key** ([Get it here](https://platform.openai.com/api-keys))

### 1. Clone & Setup
```bash
git clone <repository-url>
cd "HealthCare ChatBot"
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 3. Start Backend
```bash
cd backend
./start.sh
```

### 4. Start Frontend
```bash
cd frontend
npm install
npm start
```

⚠️ **Medical Disclaimer**: This chatbot provides general health information only and is not a substitute for professional medical advice, diagnosis, or treatment.
```

**Create `frontend/WARP.md` with:**
```markdown
# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## 🚨 Critical Issues Prevention

### CSS Syntax Validation
**ALWAYS validate CSS before committing:**
- Check all opening braces `{` have matching closing braces `}`
- Ensure all CSS properties end with semicolons `;`
- Verify no orphaned keyframe rules without parent `@keyframes`
- Test compilation with `npm start` immediately after CSS changes

### Common Issues & Solutions
1. **CSS Compilation Error**: Check `App.css` for syntax errors
2. **Backend Connection**: Ensure backend is running on port 8000
3. **TypeScript Errors**: Address all TS warnings before committing
4. **Dependencies**: Run `npm install` if modules are missing

## Quick Commands
```bash
npm install     # Install dependencies
npm start       # Start development server
npm test        # Run tests
npm run build   # Production build
```
```

**Documentation files to create in `docs/` folder:**
- `PROJECT_OVERVIEW.md` - Architecture and purpose
- `SETUP_GUIDE.md` - Detailed installation steps
- `API_REFERENCE.md` - Backend API documentation
- `TASK_LOG.md` - Development history and AI contributions

---

### 7. 🧪 Testing & Validation (CRITICAL)

**Before delivering, MUST complete ALL these tests:**

#### ✅ Pre-Development Checklist
1. **Validate all code syntax** before writing files
2. **Check CSS for matching braces and semicolons**
3. **Ensure TypeScript interfaces are complete**
4. **Verify all imports and exports are correct**

#### 🚨 Critical Testing Steps

**Step 1: Backend Testing**
```bash
cd backend
./start.sh
# Verify server starts without errors
# Test endpoint: curl http://localhost:8000/
```

**Step 2: Frontend Testing**
```bash
cd frontend
npm install
npm start
# MUST compile without errors
# Browser should open to http://localhost:3000
```

**Step 3: Integration Testing**
1. Start both backend and frontend
2. Test chat interface loads
3. Send test message: "I have a headache"
4. Verify bot responds with appropriate advice
5. Check severity classification works
6. Verify conversations saved to JSON file

**Step 4: Error Handling Testing**
1. Stop backend while frontend running
2. Send message - should show connection error
3. Restart backend - functionality should resume

#### 📝 Validation Checklist
- [ ] All files compile without syntax errors
- [ ] CSS validates without extra braces or incomplete rules
- [ ] TypeScript compiles without warnings
- [ ] Backend starts and responds to requests
- [ ] Frontend loads without console errors
- [ ] Chat functionality works end-to-end
- [ ] Conversation history saves correctly
- [ ] Mobile responsive design works
- [ ] Medical disclaimers are present

### 8. 📦 Final Deliverables

**Complete Project Structure:**
```
HealthCare ChatBot/
├── README.md              ✓ Main documentation
├── .env.example           ✓ Environment template
├── backend/
│   ├── app/main.py        ✓ FastAPI application (tested)
│   ├── requirements.txt   ✓ Python dependencies
│   └── start.sh           ✓ Startup script (executable)
├── frontend/
│   ├── src/App.tsx        ✓ React app (syntax validated)
│   ├── src/App.css        ✓ Styles (CSS validated)
│   ├── package.json       ✓ Dependencies
│   └── WARP.md            ✓ Warp guidance
├── docs/
│   ├── PROJECT_OVERVIEW.md
│   ├── SETUP_GUIDE.md
│   ├── API_REFERENCE.md
│   └── TASK_LOG.md
└── conversations.json     ✓ Auto-generated on first use
```

**Quality Assurance Requirements:**
1. **All code must compile and run successfully**
2. **CSS must be syntactically perfect (no extra braces)**
3. **Backend must respond to API calls**
4. **Frontend must load without console errors**
5. **End-to-end chat functionality must work**
6. **Documentation must be complete and accurate**

---

## 🚀 Quick Start Instructions (For End User)

**Copy these exact commands to get started:**

```bash
# 1. Get OpenAI API Key from https://platform.openai.com/api-keys

# 2. Setup environment
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=sk-your-key-here

# 3. Start Backend (Terminal 1)
cd backend
./start.sh

# 4. Start Frontend (Terminal 2)
cd frontend
npm install
npm start

# 5. Open browser to http://localhost:3000
```

**Expected Result:** Fully functional healthcare chatbot with ChatGPT-style interface, OpenAI integration, and conversation storage.

---

⚡ **Use this optimized prompt to create a complete, tested, and validated Healthcare Chatbot project that works immediately without syntax errors or configuration issues.**
