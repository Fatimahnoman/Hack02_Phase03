import os
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine, text

# Get the database URL
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///test.db')
print(f'DATABASE_URL: {DATABASE_URL}')

# Create engine and session
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    # Check if tasks table exists
    result = conn.execute(text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'task');"))
    table_exists = result.scalar()
    print(f'Tasks table exists: {table_exists}')
    
    if table_exists:
        # Count total tasks
        count_result = conn.execute(text('SELECT COUNT(*) FROM task;'))
        total_tasks = count_result.scalar()
        print(f'Total tasks in database: {total_tasks}')
        
        # Get most recent tasks
        recent_result = conn.execute(text('SELECT id, title, status, user_id, created_at FROM task ORDER BY created_at DESC LIMIT 5;'))
        recent_tasks = recent_result.fetchall()
        print('Most recent tasks:')
        for i, task in enumerate(recent_tasks):
            print(f'  {i+1}. ID: {task[0]}, Title: {task[1]}, Status: {task[2]}, User ID: {task[3]}, Created: {task[4]}')