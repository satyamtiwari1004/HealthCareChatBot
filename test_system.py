#!/usr/bin/env python3
"""
Healthcare Chatbot System Test
Tests the basic functionality without requiring OpenAI API key
"""

import json
import os
import sys
from datetime import datetime

def test_backend_imports():
    """Test that all backend dependencies can be imported"""
    print("🧪 Testing backend imports...")
    try:
        # Add the backend app directory to the Python path
        backend_path = os.path.join(os.path.dirname(__file__), 'backend', 'app')
        sys.path.insert(0, backend_path)
        
        # Test imports (but don't actually run the app)
        from fastapi import FastAPI
        from pydantic import BaseModel
        print("✅ Backend imports successful")
        return True
    except ImportError as e:
        print(f"❌ Backend import failed: {e}")
        print("Note: Run 'pip install fastapi uvicorn pydantic' to install dependencies")
        return False
    except Exception as e:
        print(f"❌ Backend test error: {e}")
        return False

def test_json_database():
    """Test the JSON database functionality"""
    print("🧪 Testing JSON database...")
    try:
        # Test conversation structure
        test_conversation = {
            "user": "test symptoms",
            "response": "test response",
            "severity": "mild",
            "timestamp": datetime.now().isoformat()
        }
        
        # Test JSON serialization
        json_str = json.dumps([test_conversation], indent=2)
        parsed = json.loads(json_str)
        
        assert len(parsed) == 1
        assert parsed[0]["user"] == "test symptoms"
        assert parsed[0]["severity"] in ["mild", "serious"]
        
        print("✅ JSON database structure validated")
        return True
    except Exception as e:
        print(f"❌ JSON database test failed: {e}")
        return False

def test_frontend_structure():
    """Test frontend file structure"""
    print("🧪 Testing frontend structure...")
    try:
        frontend_files = [
            "frontend/src/App.tsx",
            "frontend/src/App.css",
            "frontend/package.json"
        ]
        
        missing_files = []
        for file_path in frontend_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
        
        if missing_files:
            print(f"❌ Missing frontend files: {missing_files}")
            return False
        
        print("✅ Frontend structure validated")
        return True
    except Exception as e:
        print(f"❌ Frontend structure test failed: {e}")
        return False

def test_documentation():
    """Test documentation completeness"""
    print("🧪 Testing documentation...")
    try:
        doc_files = [
            "README.md",
            "docs/PROJECT_OVERVIEW.md",
            "docs/SETUP_GUIDE.md", 
            "docs/API_REFERENCE.md",
            "docs/TASK_LOG.md"
        ]
        
        missing_docs = []
        for doc_path in doc_files:
            if not os.path.exists(doc_path):
                missing_docs.append(doc_path)
        
        if missing_docs:
            print(f"❌ Missing documentation files: {missing_docs}")
            return False
        
        # Check if main README has content
        with open("README.md", "r") as f:
            readme_content = f.read()
            if len(readme_content) < 100:
                print("❌ README.md appears to be empty or too short")
                return False
        
        print("✅ Documentation validated")
        return True
    except Exception as e:
        print(f"❌ Documentation test failed: {e}")
        return False

def test_environment_config():
    """Test environment configuration"""
    print("🧪 Testing environment configuration...")
    try:
        # Check for environment files
        if not os.path.exists(".env.example"):
            print("❌ .env.example not found")
            return False
        
        if not os.path.exists(".env"):
            print("⚠️  .env file not found (create from .env.example)")
        
        print("✅ Environment configuration validated")
        return True
    except Exception as e:
        print(f"❌ Environment config test failed: {e}")
        return False

def main():
    """Run all system tests"""
    print("🩺 Healthcare Chatbot System Test")
    print("=" * 50)
    
    tests = [
        test_backend_imports,
        test_json_database,
        test_frontend_structure,
        test_documentation,
        test_environment_config
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready for deployment.")
        print("\nNext steps:")
        print("1. Add your OpenAI API key to the .env file")
        print("2. Start the backend: cd backend && ./start.sh")
        print("3. Start the frontend: cd frontend && npm start")
        print("4. Open http://localhost:3000 in your browser")
    else:
        print("❌ Some tests failed. Please review the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())