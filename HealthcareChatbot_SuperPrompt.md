# 🧩 Super Prompt — Healthcare Chatbot Project

I want to build a **Healthcare Chatbot** using **OpenAI GPT-4**. The chatbot should:
- Accept symptoms (e.g., cold, fever, cough) as input.
- Suggest simple home remedies for mild cases.
- Recommend consulting a doctor in serious cases.
- Display chat in a **ReactJS frontend** with **ChatGPT/Gemini-style UI** (chat bubbles, sticky input, scrollable history).
- Backend in **FastAPI (Python)**.
- Store interactions in a **file-based database** (JSON/SQLite).
- Provide **documentation** (README + setup guides + task log).

---

## ✅ Tech Stack
- **Backend**: FastAPI + Python + OpenAI GPT-4
- **Frontend**: ReactJS + HTML + CSS
- **Database**: JSON or SQLite
- **Deployment**: Local (extendable later)

---

## 🛠️ Step-by-Step Build Instructions

### 1. Obtain OpenAI API Key
1. Sign in at [https://platform.openai.com](https://platform.openai.com).
2. Go to **View API Keys** → Create new key.
3. Copy the key and save in `.env`:
   ```env
   OPENAI_API_KEY=sk-xxxxxxx
   ```

### 2. Backend (FastAPI)
- Create FastAPI project `backend/app/main.py`.
- Install:
  ```bash
  pip install fastapi uvicorn openai pydantic python-decouple
  ```
- Endpoint `/diagnose` accepts:
  ```json
  { "symptoms": "fever and cough" }
  ```
- Use GPT-4 with system prompt:
  > “You are a healthcare assistant. For common mild diseases (cold, cough, mild fever), suggest simple home remedies. For severe symptoms (chest pain, prolonged fever), advise consulting a doctor immediately. Do not prescribe medications.”
- Response:
  ```json
  {
    "advice": "Drink warm fluids and rest. If fever >102F persists, see a doctor.",
    "severity": "serious"
  }
  ```
- Save interaction in `conversations.json`.

### 3. Database
- Use JSON file or SQLite.
- Schema:
  ```json
  {
    "user": "I have a cold",
    "response": "Try steam inhalation and warm fluids",
    "severity": "mild",
    "timestamp": "2025-09-26T10:15:00"
  }
  ```

### 4. Frontend (React)
- Scaffold:
  ```bash
  npx create-react-app healthcare-chatbot
  ```
- Components:
  - `ChatWindow` (scrollable history)
  - `ChatBubble` (user vs bot styles)
  - `InputBar` (fixed bottom, send button)
- Features:
  - Auto-scroll on new message
  - Typing dots animation while waiting
  - Mobile responsive

### 5. Styling (ChatGPT/Gemini-like)
- Background: light gray
- User bubble: teal/blue
- Bot bubble: light gray
- Rounded corners + shadows
- Sticky input at bottom

### 6. Documentation
Generate inside `docs/`:
- `PROJECT_OVERVIEW.md` → Purpose, architecture, roadmap
- `SETUP_GUIDE.md` → Install steps (Python + Node.js + API key setup)
- `API_REFERENCE.md` → Docs for `/diagnose` endpoint
- `TASK_LOG.md` → AI/developer contributions log (Cursor, Warp, ChatGPT entries)

Root `README.md` should include:
- Overview
- Tech stack
- Features
- Setup instructions (backend + frontend + OpenAI key)
- Links to docs/
- Disclaimer:
  > ⚠️ This chatbot provides general advice only. Always consult a qualified doctor for serious or persistent conditions.

---

## 📦 Deliverables
1. **Backend code** (FastAPI + JSON DB + `/diagnose`)
2. **Frontend code** (React chat UI)
3. **File-based DB** (`conversations.json`)
4. **Documentation** (`README.md`, `docs/*.md`)
5. **Setup instructions** for backend, frontend, OpenAI key

---

⚡ Use this prompt to scaffold the **entire project repo** in Cursor, Warp, or other AI IDEs.
