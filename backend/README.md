# Agent-Orchestrated Task Management API

This is the backend API for an agent-orchestrated task management system that leverages MCP (Model Context Protocol) tools for intelligent task handling.

## Overview

This API provides endpoints for:
- Chat interactions with AI agents
- Authentication and user management
- Task and to-do management
- Health checks

## Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /api/v1/chat` - Chat with the AI agent
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET/POST/PUT/DELETE /api/todos` - To-do management
- `GET/POST/PUT/DELETE /api/tasks` - Task management

## Technologies Used

- FastAPI
- SQLModel
- PostgreSQL (or SQLite for development)
- Cohere API for AI interactions
- JWT for authentication

## Deployment

This application is deployed on Hugging Face Spaces using Docker.