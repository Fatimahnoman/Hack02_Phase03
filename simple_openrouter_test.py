import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from openai import OpenAI
from backend.src.core.config import settings

print("Testing OpenRouter API configuration...")

# Print the settings
print(f"API Key: {settings.openrouter_api_key[:10] if settings.openrouter_api_key else 'None'}...")
print(f"Base URL: {settings.openrouter_base_url}")
print(f"Model: {settings.openrouter_model}")

# Initialize the client
client = OpenAI(
    api_key=settings.openrouter_api_key,
    base_url=settings.openrouter_base_url
)

# Test a simple API call
try:
    response = client.chat.completions.create(
        model=settings.openrouter_model,
        messages=[{"role": "user", "content": "Hello, how are you?"}],
        temperature=0.7,
        max_tokens=100,
    )
    
    print(f"Response type: {type(response)}")
    print(f"Has choices: {hasattr(response, 'choices')}")
    
    if hasattr(response, 'choices') and len(response.choices) > 0:
        content = response.choices[0].message.content
        print(f"Response content length: {len(content)}")
        # Print a safe version of the content without problematic Unicode characters
        safe_content = content.encode('ascii', errors='replace').decode('ascii')
        print(f"Response content preview: {safe_content[:100]}...")
        print("SUCCESS: OpenRouter API is working correctly!")
    else:
        print("ERROR: Response doesn't contain expected choices")
        
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()