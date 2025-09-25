# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is the **React TypeScript frontend** for a Healthcare Chatbot application. The project is part of a full-stack healthcare assistant that provides AI-powered guidance for health concerns while maintaining safety standards. The backend uses FastAPI with OpenAI GPT-4.

## Key Commands

### Development
```bash
npm install                 # ALWAYS run first - install dependencies
npm start                   # Start development server on http://localhost:3000
npm run build              # Build production bundle
npm test                   # Run tests in watch mode
npm test -- --coverage     # Run tests with coverage report
```

### Quick Setup (First Time)
```bash
# Run these commands in order:
npm install
npm start
# App should open at http://localhost:3000
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

## 🚨 Troubleshooting & Known Issues

### CSS Compilation Errors
**Problem**: `Unexpected }` or CSS syntax errors during `npm start`

**Specific Issue Found**: Lines 282-286 in `App.css` had malformed CSS:
```css
/* WRONG - This caused compilation failure */
.chat-messages::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}
  }  /* <-- Extra brace */
  to {
    transform: rotate(360deg);
  }
}
```

**Solution**: Check `App.css` for:
- Unmatched opening/closing braces `{ }`
- Incomplete keyframe animations (missing `@keyframes` declaration)
- Missing semicolons in CSS properties
- Malformed media queries or selectors
- Orphaned animation keyframes without parent `@keyframes` rule

**Prevention**: Always validate CSS syntax before committing. Use VSCode CSS IntelliSense or online validators.

### Backend Connection Issues
**Problem**: Frontend shows "Sorry, I encountered an error" messages
**Solution**: 
1. Ensure backend is running: `cd ../backend && ./start.sh`
2. Check backend is accessible at `http://localhost:8000`
3. Verify `.env` file exists in parent directory with valid OpenAI API key

### Dependency Issues
**Problem**: `npm start` fails with module errors
**Solution**:
```bash
rm -rf node_modules package-lock.json
npm install
npm start
```

### Security Vulnerabilities (Development)
**Problem**: `npm audit` shows vulnerabilities
**Note**: Current vulnerabilities are in development dependencies (webpack-dev-server, postcss) and don't affect production. Avoid `npm audit fix --force` as it may break the build.

### Port Already in Use
**Problem**: "Port 3000 is already in use"
**Solution**: 
- Kill existing process: `lsof -ti:3000 | xargs kill -9`
- Or choose different port when prompted by React scripts

## 🛠️ Development Best Practices

### Before Making Changes
1. **Always test the app runs**: `npm start` before making changes
2. **Check git status**: Ensure you understand current state
3. **Create feature branches**: Don't work directly on main/develop

### CSS Editing Guidelines
- **Validate syntax**: Use VSCode CSS validation or online CSS validators
- **Test immediately**: Run `npm start` after CSS changes to catch syntax errors
- **Backup complex changes**: Comment out old code before replacing

### Code Quality
- **TypeScript**: Pay attention to type errors in VSCode
- **ESLint**: Address linting warnings shown in editor
- **Testing**: Run `npm test` before committing changes

### Git Workflow
```bash
git status                  # Check current state
git add .                   # Stage changes
git commit -m "message"     # Commit with clear message
git push origin branch-name # Push to remote
```

### Application Testing Checklist
**Before committing any changes, verify:**

1. **Frontend Compiles**: `npm start` runs without errors
2. **UI Loads**: App displays at `http://localhost:3000`
3. **Chat Interface**: Input field and send button are functional
4. **Error Handling**: App shows appropriate message when backend is down
5. **Responsive Design**: Test on mobile viewport (DevTools)
6. **TypeScript**: No TS errors in VSCode or terminal output

**Full System Test** (requires backend):
1. Start backend: `cd ../backend && ./start.sh`
2. Verify backend responds: `curl http://localhost:8000/health` (if health endpoint exists)
3. Test chat functionality: Send a test message like "I have a headache"
4. Verify response appears with appropriate styling

**Quick Smoke Test**:
```bash
npm install
npm start
# Wait for browser to open, verify no console errors
# Ctrl+C to stop
```
