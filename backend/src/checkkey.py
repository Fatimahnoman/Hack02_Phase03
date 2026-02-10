import os
from dotenv import load_dotenv

# Load .env from backend root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

key = os.getenv("OPENROUTER_API_KEY")
if key:
    print("✅ OpenRouter key loaded:", key[:6] + "...")
else:
    print("❌ OpenRouter key NOT found")
