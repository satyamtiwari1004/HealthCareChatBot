# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is the **React TypeScript frontend** for a Healthcare Chatbot application. The project is part of a full-stack healthcare assistant that provides AI-powered guidance for health concerns while maintaining safety standards. The backend uses FastAPI with OpenAI GPT-4.

## Key Commands

### Development
```bash
npm start                    # Start development server on http://localhost:3000
npm run build               # Build production bundle
npm test                    # Run tests in watch mode
npm test -- --coverage     # Run tests with coverage report
```

### Package Management
```bash
npm install                 # Install all dependencies
npm install <package>       # Add new dependency
npm install -D <package>    # Add development dependency
```

### Testing
```bash
npm test -- --watchAll=false    # Run tests once (non-interactive)
npm test -- --testPathPattern=App    # Run specific test file
```

## Architecture

### Frontend Structure
- **Single Page Application**: Built with Create React App and React 19
- **Main Component**: `App.tsx` - Contains the entire chat interface as a single component
- **State Management**: Uses React hooks (useState, useEffect) for local state
- **API Communication**: Axios for HTTP requests to backend at `http://localhost:8000`
- **Styling**: Custom CSS with ChatGPT-inspired design in `App.css`

### Key Interfaces
```typescript
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
```

### Component Architecture
The application uses a monolithic component approach where `App.tsx` handles:
- **Message State**: Array of Message objects with user/bot messages
- **API Integration**: POST requests to `/diagnose` endpoint
- **UI States**: Loading indicators, input validation, error handling
- **Auto-scrolling**: Smooth scrolling to latest messages
- **Responsive Design**: Mobile-friendly chat interface

### Backend Integration
- **API Base URL**: `http://localhost:8000` (configurable in `App.tsx` line 19)
- **Primary Endpoint**: `POST /diagnose` with payload `{ symptoms: string }`
- **Response Format**: `{ advice: string, severity: string, timestamp: string }`
- **Error Handling**: Graceful fallback when backend is unavailable

### Styling Approach
- **CSS Architecture**: Single `App.css` file with component-scoped classes
- **Design System**: Healthcare-focused with medical color scheme (blues, gradients)
- **Responsive**: Mobile-first with breakpoint at 768px
- **Animations**: Fade-in messages, typing indicators, hover effects
- **Severity Indicators**: Color-coded messages based on symptom severity

### Development Considerations

#### Backend Dependency
The frontend expects a FastAPI backend running on port 8000. The backend must be started first:
```bash
cd ../backend && ./start.sh
```

#### API Key Requirement
Backend requires OpenAI API key in `../.env` file. Frontend will show connection errors if backend is not configured.

#### State Management
- No external state management (Redux, Context) - uses local component state
- Message history is maintained only during session (no persistence)
- Real-time updates through API calls, no WebSocket connection

#### Testing
- Basic test setup with Jest and React Testing Library
- Current test suite minimal - needs expansion for full coverage
- Tests focus on component rendering and user interactions

### Common Development Tasks

#### Adding New Message Types
1. Update `Message` interface in `App.tsx`
2. Modify message rendering logic in the JSX return
3. Add corresponding CSS classes in `App.css`

#### Customizing API Integration
1. Update `API_BASE_URL` constant in `App.tsx`
2. Modify request/response interfaces as needed
3. Update error handling in `sendMessage` function

#### Styling Updates
1. All styles in single `App.css` file
2. CSS custom properties used for theming
3. Mobile styles in media queries at bottom of file

#### Adding Features
- Consider breaking down the monolithic `App.tsx` if adding complex features
- State management should be evaluated if adding user authentication or persistence
- API calls should be abstracted to service layer if adding multiple endpoints

## Project Context

This frontend is part of a larger Healthcare Chatbot system:
- **Backend**: FastAPI with OpenAI GPT-4 integration (`../backend/`)
- **Documentation**: Project docs available in `../docs/`
- **Environment**: Requires `.env` file with OpenAI API key in parent directory
- **Database**: JSON file-based conversation storage in backend

The application prioritizes user safety with medical disclaimers and appropriate severity assessment of symptoms.