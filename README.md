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

## 🏗️ Architecture

```
Healthcare Chatbot/
├── backend/                 # FastAPI Python backend
│   ├── app/
│   │   └── main.py         # Main FastAPI application
│   ├── requirements.txt    # Python dependencies
│   └── start.sh           # Backend startup script
├── frontend/               # React TypeScript frontend
│   ├── src/
│   │   ├── App.tsx        # Main chat interface
│   │   └── App.css        # ChatGPT-style styling
│   └── package.json       # Node.js dependencies
├── docs/                   # Documentation
└── conversations.json      # JSON database (auto-generated)
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **OpenAI API Key** ([Get it here](https://platform.openai.com/api-keys))

### 1. Clone & Setup

```bash
git clone <repository-url>
cd \"HealthCare ChatBot\"
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 3. Start Backend

```bash
cd backend
./start.sh
```

The backend will be available at `http://localhost:8000`

### 4. Start Frontend

```bash
# In a new terminal
cd frontend
npm install
npm start
```

The frontend will be available at `http://localhost:3000`

## 🎯 Usage

1. **Open your browser** to `http://localhost:3000`
2. **Describe your symptoms** in the chat input (e.g., \"I have a fever and cough\")
3. **Get AI-powered advice** with automatic severity assessment
4. **Follow recommendations** for home remedies or medical consultation

### Example Interactions

**Mild Symptoms:**
- Input: \"I have a slight headache\"
- Output: Home remedies like rest, hydration, and over-the-counter pain relievers

**Serious Symptoms:**
- Input: \"I have chest pain and difficulty breathing\"  
- Output: Immediate recommendation to consult a doctor or visit emergency room

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python, OpenAI GPT-4, Pydantic
- **Frontend**: React, TypeScript, Axios
- **Database**: JSON file-based storage
- **Styling**: Custom CSS with ChatGPT-inspired design
- **Deployment**: Local development (Docker/cloud ready)

## 📁 API Reference

### POST `/diagnose`
Analyze symptoms and provide healthcare advice.

**Request:**
```json
{
  \"symptoms\": \"fever and cough\"
}
```

**Response:**
```json
{
  \"advice\": \"Drink warm fluids and rest. If fever >102°F persists, see a doctor.\",
  \"severity\": \"mild\",
  \"timestamp\": \"2024-01-15T10:30:00Z\"
}
```

### GET `/history`
Retrieve conversation history.

**Response:**
```json
{
  \"conversations\": [
    {
      \"user\": \"I have a cold\",
      \"response\": \"Try steam inhalation and warm fluids\",
      \"severity\": \"mild\",
      \"timestamp\": \"2024-01-15T10:15:00Z\"
    }
  ]
}
```

## 📚 Documentation

Detailed documentation is available in the `docs/` folder:

- [📋 Project Overview](docs/PROJECT_OVERVIEW.md)
- [⚙️ Setup Guide](docs/SETUP_GUIDE.md) 
- [📖 API Reference](docs/API_REFERENCE.md)
- [📝 Task Log](docs/TASK_LOG.md)

## ⚠️ Medical Disclaimer

**This chatbot provides general health information only and is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for serious or persistent medical conditions.**

## 🔒 Privacy & Security

- All conversations are stored locally in `conversations.json`
- No data is shared with third parties (except OpenAI for AI processing)
- OpenAI API key is stored securely in environment variables
- No personal health information is logged or transmitted unnecessarily

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues:

1. Check the [Setup Guide](docs/SETUP_GUIDE.md)
2. Ensure your OpenAI API key is valid and has credits
3. Verify both backend (port 8000) and frontend (port 3000) are running
4. Check browser console for any JavaScript errors

---

**Built with ❤️ for better healthcare accessibility**