import sys
import os
sys.path.append('.')

# Import and check the config directly
from src.core.config import settings
print('Direct import from backend:')
print(f'COHERE_MODEL: {settings.cohere_model}')