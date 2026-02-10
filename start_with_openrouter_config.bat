@echo off
REM Set the correct OpenRouter configuration explicitly
set OPENAI_API_KEY=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
set OPENAI_API_BASE_URL=https://openrouter.ai/api/v1
set OPENAI_MODEL=openai/gpt-3.5-turbo

echo Starting backend server with correct OpenRouter configuration...
cd backend
uvicorn src.main:app --host 127.0.0.1 --port 8000
pause