import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from openai import OpenAI
from backend.src.core.config import settings

print("Testing simple OpenRouter API call...")

# Initialize the client
client = OpenAI(
    api_key=settings.openrouter_api_key,
    base_url=settings.openrouter_base_url
)

# Test a simple API call without tools
try:
    response = client.chat.completions.create(
        model=settings.openrouter_model,
        messages=[{"role": "user", "content": "Say hello in a friendly way."}],
        temperature=0.7,
        max_tokens=100,
    )
    
    print(f"Response type: {type(response)}")
    print(f"Has choices: {hasattr(response, 'choices')}")
    
    if hasattr(response, 'choices') and len(response.choices) > 0:
        content = response.choices[0].message.content
        safe_content = content.encode('ascii', errors='replace').decode('ascii')
        print(f"Response content: {safe_content}")
        print("SUCCESS: Simple OpenRouter API call works!")
    else:
        print("ERROR: Response doesn't contain expected choices")
        
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()