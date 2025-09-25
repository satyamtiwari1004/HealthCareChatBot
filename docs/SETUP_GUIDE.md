# ⚙️ Setup Guide

## Complete Installation & Configuration Guide

### 📋 Prerequisites

#### System Requirements
- **Operating System**: macOS, Linux, or Windows 10+
- **Python**: Version 3.8 or higher
- **Node.js**: Version 16 or higher
- **Git**: Latest version for version control
- **Terminal/Command Prompt**: For running commands

#### Account Requirements
- **OpenAI Account**: Sign up at [platform.openai.com](https://platform.openai.com)
- **API Credits**: Ensure your OpenAI account has available credits
- **API Key**: Generate a new API key from your OpenAI dashboard

---

## 🚀 Installation Steps

### Step 1: Clone the Repository

```bash
# Option A: If you have the repository URL
git clone <your-repository-url>
cd \"HealthCare ChatBot\"

# Option B: If you're setting up locally
mkdir \"HealthCare ChatBot\"
cd \"HealthCare ChatBot\"
# Copy all project files to this directory
```

### Step 2: Environment Configuration

#### Create Environment File
```bash
# Copy the example environment file
cp .env.example .env
```

#### Edit Environment Variables
Open `.env` file in your preferred text editor and configure:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-your-actual-api-key-here

# Server Configuration (optional, uses defaults if not set)
BACKEND_PORT=8000
BACKEND_HOST=0.0.0.0

# Frontend Configuration (optional)
REACT_APP_API_URL=http://localhost:8000
```

**⚠️ Important:** Replace `sk-proj-your-actual-api-key-here` with your actual OpenAI API key.

### Step 3: Backend Setup (FastAPI)

#### Navigate to Backend Directory
```bash
cd backend
```

#### Option A: Using the Provided Script (Recommended)
```bash
# Make the script executable (macOS/Linux)
chmod +x start.sh

# Run the startup script
./start.sh
```

#### Option B: Manual Setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# .\\venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
cd app
python main.py
```

#### Verify Backend Installation
- Open your browser to `http://localhost:8000`
- You should see: `{\"message\": \"Healthcare Chatbot API is running\"}`
- Test the API documentation at `http://localhost:8000/docs`

### Step 4: Frontend Setup (React)

#### Navigate to Frontend Directory
```bash
# Open a new terminal window/tab
cd frontend
```

#### Install Dependencies
```bash
# Install Node.js dependencies
npm install

# If you encounter issues, try:
# npm install --legacy-peer-deps
```

#### Start Development Server
```bash
# Start React development server
npm start
```

#### Verify Frontend Installation
- Browser should automatically open to `http://localhost:3000`
- You should see the Healthcare Chatbot interface
- Try sending a test message to verify backend connectivity

---

## 🛠️ Troubleshooting

### Common Issues & Solutions

#### OpenAI API Key Issues
**Problem:** \"OpenAI API key not configured\" error
**Solution:**
1. Verify your `.env` file exists in the root directory
2. Check that your API key is correctly formatted
3. Ensure you have credits available in your OpenAI account
4. Restart the backend server after making changes

#### Port Already in Use
**Problem:** \"Port 8000 already in use\" error
**Solution:**
```bash
# Find and kill the process using port 8000
lsof -ti:8000 | xargs kill -9

# Or change the port in your .env file
BACKEND_PORT=8001
```

#### Module Not Found Errors
**Problem:** Python module import errors
**Solution:**
```bash
# Ensure virtual environment is activated
source backend/venv/bin/activate

# Reinstall dependencies
pip install -r backend/requirements.txt

# Check Python version
python --version  # Should be 3.8+
```

#### React Build Issues
**Problem:** npm install or start failures
**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Use older Node.js version if needed
# nvm use 16  # if using nvm
```

#### CORS Errors
**Problem:** Cross-origin request blocked
**Solution:**
1. Ensure backend is running on port 8000
2. Check that CORS middleware is configured in `backend/app/main.py`
3. Verify the API_BASE_URL in React app matches backend URL

---

## 🧪 Testing Your Installation

### Backend Tests
```bash
# Test health endpoint
curl http://localhost:8000/

# Test diagnose endpoint
curl -X POST http://localhost:8000/diagnose \\
  -H \"Content-Type: application/json\" \\
  -d '{\"symptoms\": \"test symptoms\"}'

# View API documentation
open http://localhost:8000/docs
```

### Frontend Tests
1. **Visual Test**: Interface loads without errors
2. **Interaction Test**: Send a message and receive a response
3. **Responsive Test**: Resize browser window to test mobile view
4. **Error Handling**: Try sending message with backend stopped

### Integration Test
1. Start both backend and frontend
2. Open browser to `http://localhost:3000`
3. Enter: \"I have a mild headache\"
4. Verify you receive an appropriate response
5. Check that conversation is saved in `conversations.json`

---

## 📦 Alternative Installation Methods

### Using Docker (Future Enhancement)
```bash
# Build and run with Docker Compose
docker-compose up --build

# Access application at http://localhost:3000
```

### Using Virtual Machines
If you're setting up on a VM:
1. Ensure VM has at least 2GB RAM
2. Install all prerequisites within the VM
3. Configure port forwarding for ports 3000 and 8000
4. Follow standard installation steps

---

## 🔧 Configuration Options

### Backend Configuration
Edit `backend/app/main.py` to customize:
- **CORS origins**: Add your domain for production
- **Rate limiting**: Implement request throttling
- **Logging**: Configure detailed logging
- **Database**: Switch from JSON to SQLite/PostgreSQL

### Frontend Configuration
Edit `frontend/src/App.tsx` to customize:
- **API endpoints**: Change backend URL
- **UI themes**: Modify color schemes
- **Features**: Enable/disable functionality
- **Branding**: Update titles and messages

### Environment Variables Reference
```env
# Required
OPENAI_API_KEY=sk-proj-...           # Your OpenAI API key

# Optional Backend
BACKEND_PORT=8000                    # Default: 8000
BACKEND_HOST=0.0.0.0                # Default: 0.0.0.0
DEBUG=true                          # Enable debug mode

# Optional Frontend  
REACT_APP_API_URL=http://localhost:8000  # Backend URL
REACT_APP_TITLE=Healthcare Chatbot      # App title
```

---

## 🚀 Production Deployment

### Preparation Checklist
- [ ] Environment variables configured for production
- [ ] CORS origins updated for your domain
- [ ] Database migrated to persistent storage (PostgreSQL)
- [ ] HTTPS configured with SSL certificates
- [ ] Rate limiting implemented
- [ ] Error monitoring setup (Sentry, etc.)
- [ ] Backup procedures established

### Deployment Options
1. **Cloud Platforms**: AWS, Google Cloud, Azure
2. **Container Orchestration**: Kubernetes, Docker Swarm
3. **Serverless**: Vercel (frontend), AWS Lambda (backend)
4. **Traditional**: VPS with nginx reverse proxy

---

## 📞 Support

If you encounter issues not covered in this guide:

1. **Check the logs**: Backend terminal and browser console
2. **Verify prerequisites**: Ensure all requirements are met
3. **Review documentation**: Read API reference and project overview
4. **Test components**: Isolate backend vs frontend issues
5. **Create an issue**: Document your problem with error messages and system info

---

*This setup guide is regularly updated to reflect the latest installation procedures and troubleshooting solutions.*