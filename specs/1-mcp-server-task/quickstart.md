# Quickstart Guide: MCP Server and Stateless Task Tooling Layer

**Feature**: MCP Server and Stateless Task Tooling Layer
**Date**: 2026-01-28

## Prerequisites

### System Requirements
- Python 3.11 or higher
- pip package manager
- Access to Neon Serverless PostgreSQL database
- Network connectivity for AI agent access

### Environment Setup
```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Database Configuration
1. Obtain Neon Serverless PostgreSQL connection credentials
2. Set environment variables:
```bash
export DATABASE_URL="postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require"
```

## Installation

### 1. Install Core Dependencies
```bash
pip install python-mcp sqlmodel psycopg2-binary python-dotenv
```

### 2. Set Up Environment Variables
Create `.env` file with:
```
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
SERVER_HOST=localhost
SERVER_PORT=3000
LOG_LEVEL=INFO
```

### 3. Initialize Database Tables
```bash
# Run this command to create required tables
python -m src.mcp_server.models.database init
```

## Running the Server

### Start the MCP Server
```bash
python -m src.mcp_server.server
```

The server will start and register the following tools:
- `add_task`
- `list_tasks`
- `update_task`
- `complete_task`
- `delete_task`

## Using the Tools

### Example Tool Invocations

#### Add a New Task
```json
{
  "tool": "add_task",
  "arguments": {
    "title": "Sample Task",
    "description": "Description of the sample task"
  }
}
```

#### List All Tasks
```json
{
  "tool": "list_tasks",
  "arguments": {}
}
```

#### Update a Task
```json
{
  "tool": "update_task",
  "arguments": {
    "task_id": "uuid-string",
    "title": "Updated Title",
    "status": "in-progress"
  }
}
```

#### Complete a Task
```json
{
  "tool": "complete_task",
  "arguments": {
    "task_id": "uuid-string"
  }
}
```

#### Delete a Task
```json
{
  "tool": "delete_task",
  "arguments": {
    "task_id": "uuid-string"
  }
}
```

## Testing the Server

### Run Unit Tests
```bash
pytest tests/unit/
```

### Run Integration Tests
```bash
pytest tests/integration/
```

### Manual Testing
Use an MCP-compatible client to connect to the server and invoke the tools.

## Configuration Options

### Server Settings
- `SERVER_HOST`: Host address for the server (default: localhost)
- `SERVER_PORT`: Port for the server (default: 3000)
- `LOG_LEVEL`: Logging level (default: INFO)

### Database Settings
- `DATABASE_URL`: Connection string for Neon PostgreSQL
- `DB_POOL_SIZE`: Size of the connection pool (default: 5)
- `DB_POOL_TIMEOUT`: Timeout for getting connections (default: 30)

## Troubleshooting

### Common Issues

#### Database Connection Errors
- Verify `DATABASE_URL` is correctly set
- Check network connectivity to Neon database
- Ensure database credentials are valid

#### Tool Registration Failures
- Verify MCP SDK is properly installed
- Check server startup logs for errors
- Ensure no port conflicts exist

#### State Persistence Issues
- Confirm database tables are created
- Verify write permissions to the database
- Check for connection timeouts during operations

### Log Locations
Server logs are written to stdout by default. For production, consider redirecting to a log file.

## Production Deployment

### Environment Variables for Production
```
DATABASE_URL=postgresql://prod-credentials...
SERVER_HOST=0.0.0.0
SERVER_PORT=3000
LOG_LEVEL=WARNING
```

### Health Checks
The server exposes health check endpoints for monitoring:
- `/health` - Basic server health
- `/ready` - Server readiness for traffic

### Scaling Considerations
- Increase database connection pool size for higher concurrency
- Use load balancer for multiple server instances
- Monitor database connection limits