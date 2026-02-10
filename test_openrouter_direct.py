import openai
from backend.src.core.config import settings

# Test the OpenRouter API configuration
print("Testing OpenRouter API configuration...")

# Print the settings
print(f"API Key: {settings.openrouter_api_key[:10] if settings.openrouter_api_key else 'None'}...")
print(f"Base URL: {settings.openrouter_base_url}")
print(f"Model: {settings.openrouter_model}")

# Initialize the client
client = openai.OpenAI(
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
    # Safely print the response, handling potential Unicode characters
    try:
        print(f"Response: {response}")
    except UnicodeEncodeError:
        print(f"Response (with Unicode handling): {response.model_dump_json()}")
    print(f"Choices: {hasattr(response, 'choices')}")
    
    if hasattr(response, 'choices'):
        print(f"First choice content: {response.choices[0].message.content}")
    else:
        print("No choices attribute found")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()