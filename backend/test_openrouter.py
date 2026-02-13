import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if the OpenRouter API key is loaded
api_key = os.getenv("OPENROUTER_API_KEY")
print(f"OPENROUTER_API_KEY: {'Loaded' if api_key else 'NOT FOUND'}")

if api_key:
    print(f"API Key starts with: {api_key[:10]}...")
    print(f"API Key length: {len(api_key)}")

# Check other related environment variables
base_url = os.getenv("OPENROUTER_BASE_URL")
model = os.getenv("OPENROUTER_MODEL")

print(f"OPENROUTER_BASE_URL: {base_url}")
print(f"OPENROUTER_MODEL: {model}")