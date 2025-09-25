# 📖 API Reference

## Healthcare Chatbot REST API

### Base URL
```
http://localhost:8000
```

---

## 🔍 Overview

The Healthcare Chatbot API provides endpoints for symptom analysis and conversation management. Built with FastAPI, it offers automatic documentation, request validation, and OpenAPI schema generation.

### Authentication
Currently, no authentication is required for local development. For production deployments, implement appropriate authentication mechanisms.

### Rate Limiting
No rate limiting is implemented in the current version. Consider adding rate limiting for production use.

---

## 📋 Endpoints

### 1. Health Check

#### `GET /`

Simple health check endpoint to verify API availability.

**Request:**
```bash
curl -X GET http://localhost:8000/
```

**Response:**
```json
{
  \"message\": \"Healthcare Chatbot API is running\"
}
```

**Status Codes:**
- `200 OK`: API is running successfully

---

### 2. Diagnose Symptoms

#### `POST /diagnose`

Analyze user symptoms and provide healthcare guidance using OpenAI GPT-4.

**Request:**
```bash
curl -X POST http://localhost:8000/diagnose \\
  -H \"Content-Type: application/json\" \\
  -d '{
    \"symptoms\": \"I have a fever and cough\"
  }'
```

**Request Body:**
```json
{
  \"symptoms\": \"string\"
}
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| symptoms | string | Yes | Description of the user's symptoms |

**Response:**
```json
{
  \"advice\": \"For fever and cough, try getting plenty of rest, staying hydrated, and taking over-the-counter fever reducers. If your fever exceeds 102°F (38.9°C) or persists for more than 3 days, please consult a healthcare provider.\",
  \"severity\": \"mild\",
  \"timestamp\": \"2024-01-15T14:30:45.123456\"
}
```

**Response Fields:**
| Field | Type | Description |
|-------|------|-------------|
| advice | string | AI-generated healthcare advice |
| severity | string | Severity level: \"mild\" or \"serious\" |
| timestamp | string | ISO 8601 formatted timestamp |

**Status Codes:**
- `200 OK`: Successful diagnosis
- `400 Bad Request`: Invalid input (empty symptoms)
- `500 Internal Server Error`: AI service error or server issue

**Error Response:**
```json
{
  \"detail\": \"Symptoms cannot be empty\"
}
```

---

### 3. Conversation History

#### `GET /history`

Retrieve all stored conversation history.

**Request:**
```bash
curl -X GET http://localhost:8000/history
```

**Response:**
```json
{
  \"conversations\": [
    {
      \"user\": \"I have a headache\",
      \"response\": \"For a headache, try resting in a quiet, dark room and staying hydrated. Over-the-counter pain relievers like acetaminophen or ibuprofen may help.\",
      \"severity\": \"mild\",
      \"timestamp\": \"2024-01-15T14:25:30.123456\"
    },
    {
      \"user\": \"I have chest pain\",
      \"response\": \"Chest pain can be serious and requires immediate medical attention. Please seek emergency medical care right away or call emergency services.\",
      \"severity\": \"serious\",
      \"timestamp\": \"2024-01-15T14:30:45.123456\"
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Successfully retrieved history
- `500 Internal Server Error`: Database read error

---

## 🏗️ Data Models

### SymptomRequest

```json
{
  \"symptoms\": \"string\"
}
```

**Validation Rules:**
- `symptoms` must be a non-empty string
- Maximum length: 1000 characters (recommended)
- Whitespace-only strings are rejected

### DiagnosisResponse

```json
{
  \"advice\": \"string\",
  \"severity\": \"string\",
  \"timestamp\": \"string\"
}
```

**Field Details:**
- `advice`: Comprehensive health guidance (1-500 words typical)
- `severity`: Either \"mild\" or \"serious\"
- `timestamp`: ISO 8601 format with microsecond precision

### Conversation

```json
{
  \"user\": \"string\",
  \"response\": \"string\",
  \"severity\": \"string\",
  \"timestamp\": \"string\"
}
```

---

## 🧪 Testing Examples

### Basic Symptom Analysis
```bash
curl -X POST http://localhost:8000/diagnose \\
  -H \"Content-Type: application/json\" \\
  -d '{\"symptoms\": \"runny nose and sneezing\"}'
```

### Serious Symptom Test
```bash
curl -X POST http://localhost:8000/diagnose \\
  -H \"Content-Type: application/json\" \\
  -d '{\"symptoms\": \"severe chest pain and difficulty breathing\"}'
```

### Invalid Request Test
```bash
curl -X POST http://localhost:8000/diagnose \\
  -H \"Content-Type: application/json\" \\
  -d '{\"symptoms\": \"\"}'
```

Expected Response: `400 Bad Request`

---

## 🔧 Error Handling

### Error Response Format
```json
{
  \"detail\": \"Error description\"
}
```

### Common Error Scenarios

#### OpenAI API Issues
- **Status**: `500 Internal Server Error`
- **Cause**: Invalid API key, insufficient credits, or service downtime
- **Solution**: Check OpenAI account status and API key configuration

#### Validation Errors
- **Status**: `400 Bad Request`
- **Cause**: Empty or invalid symptoms parameter
- **Solution**: Provide valid symptom description

#### Database Errors
- **Status**: `500 Internal Server Error`
- **Cause**: Unable to read/write conversation history
- **Solution**: Check file permissions and disk space

---

## 🔬 Advanced Usage

### Batch Processing
For multiple symptom analyses, make separate requests:

```python
import asyncio
import aiohttp

async def analyze_symptoms(session, symptoms_list):
    tasks = []
    for symptoms in symptoms_list:
        task = session.post('/diagnose', json={'symptoms': symptoms})
        tasks.append(task)
    
    responses = await asyncio.gather(*tasks)
    return responses
```

### Custom Headers
Add custom headers for tracking or debugging:

```bash
curl -X POST http://localhost:8000/diagnose \\
  -H \"Content-Type: application/json\" \\
  -H \"X-Request-ID: unique-request-id\" \\
  -d '{\"symptoms\": \"symptoms description\"}'
```

---

## 📊 Response Time Expectations

| Endpoint | Expected Response Time | Notes |
|----------|----------------------|-------|
| `GET /` | < 10ms | Simple health check |
| `POST /diagnose` | 1-5 seconds | Depends on OpenAI API response |
| `GET /history` | < 100ms | File I/O dependent |

---

## 🚀 Interactive API Documentation

FastAPI automatically generates interactive documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

### Features:
- Try endpoints directly from browser
- View request/response schemas
- Download OpenAPI specification
- Generate client SDKs

---

## 🔮 Future API Enhancements

### Planned Endpoints
- `POST /auth/login` - User authentication
- `GET /users/profile` - User profile management
- `POST /symptoms/analyze-image` - Image-based symptom analysis
- `GET /history/export` - Export conversation data

### Planned Features
- WebSocket support for real-time chat
- Webhook integration for external systems
- API versioning (/v1/, /v2/)
- GraphQL endpoint support

---

## 📝 API Changelog

### Version 1.0.0 (Current)
- Initial release with basic symptom analysis
- JSON file-based storage
- OpenAI GPT-4 integration
- CORS support for web frontend

### Planned Version 1.1.0
- Rate limiting implementation
- Enhanced error responses
- Request logging and analytics
- Performance optimizations

---

*This API reference is automatically updated with each release. For the most current information, always refer to the interactive documentation at `/docs`.*