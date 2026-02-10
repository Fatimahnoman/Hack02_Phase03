import cohere
from backend.src.core.config import settings

print("Testing Cohere configuration...")
print(f"API Key configured: {bool(settings.cohere_api_key)}")
print(f"Model: {settings.cohere_model}")

client = cohere.Client(api_key=settings.cohere_api_key)

try:
    resp = client.chat(message="hi", model=settings.cohere_model)
    print("SUCCESS: Cohere connection works!")
    print(f"Response: {resp.text}")
except Exception as e:
    print(f"ERROR: {e}")