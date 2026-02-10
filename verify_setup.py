#!/usr/bin/env python3
"""
Quick verification script to ensure the system is properly set up
"""
import os
import sys
from pathlib import Path

def check_python_dependencies():
    """Check if required Python packages are installed"""
    print("[INFO] Checking Python dependencies...")

    required_packages = [
        "fastapi",
        "sqlmodel",
        "pydantic",
        "pydantic_settings",
        "uvicorn",
        "cohere",
        "passlib",
        "python_jose",
        "cryptography"
    ]

    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print(f"[ERROR] Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r backend/requirements.txt")
        return False
    else:
        print("[SUCCESS] All required Python packages are installed")
        return True

def check_files_exist():
    """Check if required files exist"""
    print("\n[INFO] Checking required files...")

    required_files = [
        "backend/requirements.txt",
        "backend/src/main.py",
        "backend/src/models/user.py",
        "backend/src/api/auth_router.py",
        "backend/src/services/auth_service.py",
        "backend/.env"
    ]

    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)

    if missing_files:
        print(f"[ERROR] Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("[SUCCESS] All required files exist")
        return True

def check_database_config():
    """Check if database configuration is correct"""
    print("\n[INFO] Checking database configuration...")

    env_path = Path("backend/.env")
    if not env_path.exists():
        print("[ERROR] .env file does not exist in backend/")
        return False

    with open(env_path, 'r') as f:
        content = f.read()

    if "sqlite://" in content:
        print("[SUCCESS] Database configured to use SQLite (local development)")
        return True
    elif "postgresql" in content.lower():
        print("[WARNING] Database configured to use PostgreSQL (ensure server is accessible)")
        return True
    else:
        print("[ERROR] Unknown database configuration")
        return False

def test_imports():
    """Test if main modules can be imported without errors"""
    print("\n[INFO] Testing module imports...")

    try:
        # Change to backend directory to make imports work
        original_dir = os.getcwd()
        os.chdir("backend")

        # Test main application import
        from src.main import app
        print("[SUCCESS] Main application imports successfully")

        # Test auth module
        from src.api.auth_router import router as auth_router
        print("[SUCCESS] Auth router imports successfully")

        # Test chat module
        from src.api.chat_router import router as chat_router
        print("[SUCCESS] Chat router imports successfully")

        # Test models
        from src.models.user import User, UserCreate, UserRead
        from src.models.conversation import Conversation
        from src.models.message import Message
        print("[SUCCESS] Models import successfully")

        # Test services
        from src.services.auth_service import create_user, authenticate_user
        from src.services.chat_service import ChatService
        from src.services.ai_agent_service import AIAgentService
        print("[SUCCESS] Services import successfully")

        os.chdir(original_dir)
        return True

    except Exception as e:
        print(f"[ERROR] Import error: {e}")
        os.chdir(original_dir)
        return False

def main():
    print("[INFO] Verifying Evolution of Todo - Phase III Setup")
    print("=" * 50)

    checks = [
        check_python_dependencies(),
        check_files_exist(),
        check_database_config(),
        test_imports()
    ]

    print("\n" + "=" * 50)
    if all(checks):
        print("[SUCCESS] All checks passed! The system is ready to run.")
        print("\\nTo start the application:")
        print("1. Backend: cd backend && uvicorn src.main:app --reload --port 8000")
        print("2. Frontend: cd frontend && npm run dev")
        print("\\nAPI endpoints will be available at:")
        print("- http://localhost:8000/docs (API documentation)")
        print("- http://localhost:8000/api/auth/register (Registration)")
        print("- http://localhost:8000/api/auth/login (Login)")
        print("- http://localhost:8000/api/{user_id}/chat (AI Chat)")
        return True
    else:
        print("[ERROR] Some checks failed. Please resolve the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)