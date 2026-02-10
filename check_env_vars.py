import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('backend/.env')

print("Environment variables from .env file:")
print(f"OPENAI_API_KEY: {'*' * 20}{os.getenv('OPENAI_API_KEY', '')[-5:] if os.getenv('OPENAI_API_KEY') else 'NOT SET'}")
print(f"OPENAI_API_BASE_URL: {os.getenv('OPENAI_API_BASE_URL')}")
print(f"OPENAI_MODEL: {os.getenv('OPENAI_MODEL')}")

# Also load .env.local if present
load_dotenv("backend/.env.local", override=True)

print("\nAfter loading .env.local:")
print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")