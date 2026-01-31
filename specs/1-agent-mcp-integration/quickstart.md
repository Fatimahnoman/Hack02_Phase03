# Quickstart Guide: Agent-Orchestrated Task Management via MCP Tools

**Feature**: 1-agent-mcp-integration
**Date**: 2026-01-28

## Overview

This guide provides quick setup instructions for the Agent-Orchestrated Task Management system that connects OpenAI Agents SDK with MCP task tools for natural language task management.

## Prerequisites

- Python 3.11+
- OpenAI API key
- MCP SDK
- PostgreSQL database (Neon Serverless recommended)
- SQLModel
- FastAPI

## Setup Instructions

### 1. Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd <repository-directory>

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=postgresql+asyncpg://username:password@host:port/database_name
MCP_SERVER_URL=your_mcp_server_url
SECRET_KEY=your_secret_key_for_authentication
```

### 3. Database Setup

```bash
# Run database migrations
alembic upgrade head

# Initialize database with required data
python -c "from src.core.database import init_db; init_db()"
```

### 4. Running the Service

```bash
# Start the backend server
uvicorn src.api.main:app --reload --port 8000

# Or with gunicorn for production
gunicorn src.api.main:app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## API Usage

### Chat Endpoint

Send a POST request to `/chat` with the following payload:

```json
{
  "message": "Create a new task called 'Update documentation'"
}
```

The response will include:
- The agent's response
- Tool call metadata
- Any relevant task information

## Key Components

### Agent Service
Located in `src/services/agent_service.py`, this component manages the OpenAI Agent and its interaction with MCP tools.

### MCP Tool Registry
Located in `src/services/mcp_tool_registry.py`, this component registers and manages MCP tools available to the agent.

### Conversation Service
Located in `src/services/conversation_service.py`, this component handles conversation history retrieval and storage.

## Testing

```bash
# Run all tests
pytest

# Run specific test module
pytest tests/unit/test_agent_service.py

# Run integration tests
pytest tests/integration/
```

## Development

### Adding New MCP Tools

1. Create a new tool function in the appropriate service
2. Register the tool with the MCP tool registry
3. Add the tool to the agent's available tools list
4. Write tests for the new functionality

### Modifying Agent Behavior

1. Update the system prompt in `src/core/config.py`
2. Adjust the agent configuration in `src/services/agent_service.py`
3. Test the changes with various natural language inputs

## Troubleshooting

### Common Issues

1. **OpenAI API Connection**: Verify your API key is correct and has sufficient quota
2. **Database Connection**: Ensure the DATABASE_URL is properly configured
3. **MCP Tool Registration**: Confirm all required tools are registered with the agent
4. **Conversation History**: Verify the database contains conversation history

### Debugging Tips

- Enable debug logging by setting `LOG_LEVEL=debug` in your environment
- Check the tool call logs in the database for execution details
- Monitor the agent's response to identify interpretation issues