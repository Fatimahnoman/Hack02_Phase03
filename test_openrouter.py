import openai
from backend.src.core.config import settings

print("Testing OpenRouter configuration...")
print(f"API Key: {settings.openai_api_key[:10]}... (truncated)")
print(f"Base URL: {settings.openai_api_base_url}")
print(f"Model: {settings.openai_model}")

# Initialize OpenAI client with OpenRouter settings
client_params = {"api_key": settings.openai_api_key}
if settings.openai_api_base_url:
    client_params["base_url"] = settings.openai_api_base_url

print(f"Client params: {client_params}")

client = openai.OpenAI(**client_params)

# Try a simple test call
try:
    completion = client.chat.completions.create(
        model=settings.openai_model,
        messages=[{"role": "user", "content": "hi"}],
        max_tokens=10
    )
    print("SUCCESS: OpenRouter connection works!")
    print(f"Response: {completion.choices[0].message.content}")
except Exception as e:
    print(f"ERROR: {e}")