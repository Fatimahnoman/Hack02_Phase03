import os
from dotenv import load_dotenv

# Load the environment files like the application does
print("Loading environment variables...")
load_dotenv()  # This loads from the current directory (root)
print(f"After loading root .env - OPENAI_API_BASE_URL: {os.getenv('OPENAI_API_BASE_URL')}")
print(f"After loading root .env - OPENAI_MODEL: {os.getenv('OPENAI_MODEL')}")

load_dotenv('.env.local', override=True)  # This would load from root .env.local if it exists
print(f"After loading root .env.local - OPENAI_API_BASE_URL: {os.getenv('OPENAI_API_BASE_URL')}")
print(f"After loading root .env.local - OPENAI_MODEL: {os.getenv('OPENAI_MODEL')}")

# Also load from backend directory
if os.path.exists('backend/.env'):
    print("Loading backend/.env...")
    load_dotenv('backend/.env')
    print(f"After loading backend .env - OPENAI_API_BASE_URL: {os.getenv('OPENAI_API_BASE_URL')}")
    print(f"After loading backend .env - OPENAI_MODEL: {os.getenv('OPENAI_MODEL')}")

if os.path.exists('backend/.env.local'):
    print("Loading backend/.env.local...")
    load_dotenv('backend/.env.local', override=True)
    print(f"After loading backend .env.local - OPENAI_API_BASE_URL: {os.getenv('OPENAI_API_BASE_URL')}")
    print(f"After loading backend .env.local - OPENAI_MODEL: {os.getenv('OPENAI_MODEL')}")

print('\nFinal values:')
print(f'OPENAI_API_BASE_URL: {os.getenv("OPENAI_API_BASE_URL")}')
print(f'OPENAI_MODEL: {os.getenv("OPENAI_MODEL")}')
print(f'OPENAI_API_KEY preview: {os.getenv("OPENAI_API_KEY", "")[:20]}...')