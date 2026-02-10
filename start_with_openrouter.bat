@echo off
REM Set the correct OpenAI configuration for OpenRouter
set OPENAI_API_BASE_URL=https://openrouter.ai/api/v1
set OPENAI_MODEL=openai/gpt-3.5-turbo

REM Start the backend server with correct configuration
echo Starting backend server with OpenRouter configuration...
cd backend
uvicorn src.main:app --host 127.0.0.1 --port 8000
pause