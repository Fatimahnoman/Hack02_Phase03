# Quickstart Guide: Stateless Conversation Cycle

## Overview
This guide provides the essential information needed to implement and deploy the stateless conversation cycle feature. This feature enables the chatbot to operate without relying on conversation memory, ensuring each request is processed independently using only user input, database state, and tool results.

## Prerequisites
- Python 3.9+ installed
- Node.js 18+ installed (for frontend)
- PostgreSQL database (Neon Serverless recommended)
- Git version control

## Setup Steps

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

### 3. Environment Configuration
Create `.env` file in the backend directory:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/chatbot_db
SECRET_KEY=your-secret-key-here
DEBUG=False
```

### 4. Database Initialization
```bash
cd backend
python -m src.main init-db
```

This will create all necessary tables based on the data model:
- users table
- tasks table
- conversation_contexts table
- intent_logs table
- tool_executions table

## Key Implementation Components

### 1. Intent Parser Service (`intent_parser.py`)
Located in `backend/src/services/`
- Parses user input to determine intent
- Does not rely on conversation history
- Returns structured intent with parameters

### 2. Database Service (`database_service.py`)
Located in `backend/src/services/`
- Handles all database operations
- Ensures "fetch-first" approach before actions
- Manages transactions for consistency

### 3. Conversation Service (`conversation_service.py`)
Located in `backend/src/services/`
- Orchestrates the stateless conversation flow
- Coordinates intent parsing, database queries, and tool execution
- Generates responses based on reality (database state + tool results)

### 4. API Endpoints (`routes/chat.py`)
Located in `backend/src/api/routes/`
- `/chat` - Main endpoint for chat interactions
- Processes each request independently
- Returns deterministic responses based on current state

## Running the Application

### Backend
```bash
cd backend
python -m src.main dev
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Testing the Stateless Behavior

### 1. Deterministic Output Test
Send the same input multiple times:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_input": "What are my pending tasks?", "user_id": "test-user"}'
```

Verify that the output is identical for identical inputs under the same database conditions.

### 2. Server Restart Test
- Start the server and send a few requests
- Restart the server
- Send the same requests
- Verify that behavior is consistent across restarts

### 3. Database State Verification
- Manually modify database records
- Send requests that would access those records
- Verify that responses reflect the actual database state, not cached information

## Key Code Patterns

### Stateless Request Handler
```python
async def handle_request(user_input: str, user_id: str):
    # 1. Parse intent from current input only
    intent = await intent_parser.parse(user_input)

    # 2. Fetch required data from DB before action
    user_data = await db_service.get_user_tasks(user_id)

    # 3. Execute exactly one tool per intent
    if intent.type == "create_task":
        result = await tool_executor.create_task(intent.params)

    # 4. Validate tool result
    if not result.success:
        return {"error": result.message}

    # 5. Generate response from reality (DB + tool result)
    updated_tasks = await db_service.get_user_tasks(user_id)
    return {"response": f"Task created. You now have {len(updated_tasks)} tasks."}
```

### Database Transaction Wrapper
```python
async def execute_with_consistency_check(operation, user_id):
    # Verify state before operation
    initial_state = await db_service.get_user_state(user_id)

    # Execute operation in transaction
    async with db_service.transaction():
        result = await operation()

    # Verify state after operation
    final_state = await db_service.get_user_state(user_id)

    return {
        "result": result,
        "state_changed": initial_state != final_state
    }
```

## Common Pitfalls to Avoid

1. **Caching Conversation State**: Never store conversation history in memory or session
2. **Assuming Context**: Always verify database state before making decisions
3. **Simulating Tool Success**: Always execute and validate actual tool results
4. **Skipping Validation**: Validate all inputs and outputs independently
5. **Persistent Sessions**: Avoid creating persistent session objects that retain state

## Monitoring and Validation

### Built-in Validation Checks
- Intent consistency logging
- Database state verification
- Response determinism testing
- Error handling validation

### Key Metrics to Monitor
- Request processing time
- Database query efficiency
- Tool execution success rates
- Response consistency scores
- Memory usage (should remain stable regardless of conversation length)

## Troubleshooting

### If Responses Are Not Deterministic
1. Check if any conversation state is being cached
2. Verify all database queries are executed for each request
3. Ensure tool execution is actually happening (not mocked)

### If Database State Isn't Reflected
1. Verify database connections are fresh for each request
2. Check transaction isolation levels
3. Ensure cache invalidation is working properly

### Performance Issues
1. Optimize database queries with proper indexing
2. Use connection pooling effectively
3. Consider read replicas for frequent queries