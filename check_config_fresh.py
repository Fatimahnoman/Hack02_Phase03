import sys
import os

# Clear any cached modules
modules_to_clear = [key for key in sys.modules.keys() if key.startswith('backend')]
for module in modules_to_clear:
    del sys.modules[module]

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Now import the settings
from backend.src.core.config import settings

print("Configuration Check:")
print(f"DATABASE_URL: {settings.database_url}")
print(f"COHERE_API_KEY: {'*' * 20}{settings.cohere_api_key[-5:] if settings.cohere_api_key else 'NOT SET'}")
print(f"COHERE_MODEL: {settings.cohere_model}")