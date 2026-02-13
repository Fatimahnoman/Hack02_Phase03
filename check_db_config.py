import os
from dotenv import load_dotenv

# Load the main .env file
load_dotenv()

# Check the DATABASE_URL from the main .env file
db_url = os.getenv('DATABASE_URL', 'sqlite:///test.db')
print('DATABASE_URL from main .env:', db_url)

# Change to backend directory and check its .env
backend_env_path = os.path.join('backend', '.env')
if os.path.exists(backend_env_path):
    # Load the backend .env file
    load_dotenv(backend_env_path, override=True)
    
backend_db_url = os.getenv('DATABASE_URL', 'sqlite:///test.db')
print('DATABASE_URL from backend .env (after loading):', backend_db_url)