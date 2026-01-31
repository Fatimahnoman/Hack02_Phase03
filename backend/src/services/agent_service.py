import openai
import json
from typing import Dict, Any, List
from sqlmodel import Session
from ..core.config import settings
from .mcp_tool_registry import MCPTaskToolRegistry


class AgentService:
    """Service for managing OpenAI agent interactions with MCP tools."""

    def __init__(self, session: Session):
        self.session = session
        self.mcp_tool_registry = MCPTaskToolRegistry(session)

        # Initialize OpenAI client with potential custom base URL
        client_params = {"api_key": settings.openai_api_key}
        if settings.openai_api_base_url:
            client_params["base_url"] = settings.openai_api_base_url

        self.client = openai.OpenAI(**client_params)

        # Register tools with the agent
        self.tools = self._register_tools()

    def _register_tools(self) -> List[Dict[str, Any]]:
        """Register MCP tools with the OpenAI agent."""
        available_tools = self.mcp_tool_registry.register_tools()
        tool_definitions = []

        # Define tool schemas for OpenAI
        tool_definitions.append({
            "type": "function",
            "function": {
                "name": "create_task",
                "description": "Create a new task with a title and optional description and priority",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "The title of the task"
                        },
                        "description": {
                            "type": "string",
                            "description": "The description of the task"
                        },
                        "priority": {
                            "type": "string",
                            "enum": ["low", "medium", "high", "urgent"],
                            "description": "The priority of the task",
                            "default": "medium"
                        }
                    },
                    "required": ["title"]
                }
            }
        })

        tool_definitions.append({
            "type": "function",
            "function": {
                "name": "list_tasks",
                "description": "List all tasks with optional filtering by status and priority",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["pending", "in-progress", "completed", "cancelled"],
                            "description": "Filter tasks by status"
                        },
                        "priority": {
                            "type": "string",
                            "enum": ["low", "medium", "high", "urgent"],
                            "description": "Filter tasks by priority"
                        }
                    }
                }
            }
        })

        tool_definitions.append({
            "type": "function",
            "function": {
                "name": "update_task",
                "description": "Update an existing task with new information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "The ID of the task to update"
                        },
                        "title": {
                            "type": "string",
                            "description": "The new title of the task"
                        },
                        "description": {
                            "type": "string",
                            "description": "The new description of the task"
                        },
                        "status": {
                            "type": "string",
                            "enum": ["pending", "in-progress", "completed", "cancelled"],
                            "description": "The new status of the task"
                        },
                        "priority": {
                            "type": "string",
                            "enum": ["low", "medium", "high", "urgent"],
                            "description": "The new priority of the task"
                        }
                    },
                    "required": ["task_id"]
                }
            }
        })

        tool_definitions.append({
            "type": "function",
            "function": {
                "name": "complete_task",
                "description": "Mark a task as completed",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "The ID of the task to complete"
                        }
                    },
                    "required": ["task_id"]
                }
            }
        })

        tool_definitions.append({
            "type": "function",
            "function": {
                "name": "delete_task",
                "description": "Delete a task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "The ID of the task to delete"
                        }
                    },
                    "required": ["task_id"]
                }
            }
        })

        return tool_definitions

    def process_request(self, user_input: str, conversation_history: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Process a user request through the OpenAI agent with MCP tools.

        Args:
            user_input: The user's natural language request
            conversation_history: The history of the conversation for context

        Returns:
            Dictionary containing the agent response and tool call metadata
        """
        # Prepare the messages for the agent, including conversation history
        messages = []

        # Add system message to set the agent's behavior
        messages.append({
            "role": "system",
            "content": f"""You are a helpful assistant that manages tasks for users.
            Use the provided tools to create, list, update, complete, or delete tasks.
            Always respond in a friendly and informative way.
            The current model is {settings.openai_model}. Respond within {settings.max_response_tokens} tokens."""
        })

        # Add conversation history
        for msg in conversation_history:
            messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })

        # Add the current user input
        messages.append({
            "role": "user",
            "content": user_input
        })

        try:
            # Call the OpenAI API with tools
            response = self.client.chat.completions.create(
                model=settings.openai_model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto",  # Auto-select the appropriate tool
            )

            # Get the response message
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            # If the agent decided to use tools, execute them
            if tool_calls:
                # Create a temporary message list that includes the assistant's tool calls
                # This follows the correct protocol: assistant message with tool_calls comes first
                temp_messages = messages.copy()

                # Add the assistant message that contains the tool_calls (this was the original response)
                temp_messages.append({
                    "role": "assistant",
                    "content": response_message.content,
                    "tool_calls": response_message.tool_calls
                })

                # Execute each tool call and add the tool responses
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    # Get the function from the registry
                    available_functions = self.mcp_tool_registry.register_tools()
                    if function_name in available_functions:
                        function_to_call = available_functions[function_name]

                        # Execute the function
                        try:
                            function_response = function_to_call(**function_args)

                            # Add the tool response to the messages for the agent
                            # This follows the protocol: tool response comes after assistant with tool_calls
                            temp_messages.append({
                                "role": "tool",
                                "content": str(function_response),
                                "tool_call_id": tool_call.id
                            })
                        except Exception as e:
                            # Handle error and add to messages
                            error_msg = f"Error executing {function_name}: {str(e)}"
                            temp_messages.append({
                                "role": "tool",
                                "content": error_msg,
                                "tool_call_id": tool_call.id
                            })
                    else:
                        # Unknown function
                        temp_messages.append({
                            "role": "tool",
                            "content": f"Unknown function: {function_name}",
                            "tool_call_id": tool_call.id
                        })

                # Get the final response from the agent after tool execution
                # This request includes the complete sequence: user → assistant(with tool_calls) → tool → assistant
                second_response = self.client.chat.completions.create(
                    model=settings.openai_model,
                    messages=temp_messages,
                )

                final_response = second_response.choices[0].message.content

                # Collect tool call information for metadata
                tool_call_metadata = []
                for tc in tool_calls:
                    tool_call_metadata.append({
                        "function_name": tc.function.name,
                        "parameters": json.loads(tc.function.arguments),
                        "id": tc.id
                    })

                return {
                    "response": final_response,
                    "tool_calls": tool_call_metadata,
                    "status": "success"
                }
            else:
                # No tools were called, return the agent's response
                return {
                    "response": response_message.content,
                    "tool_calls": [],
                    "status": "success"
                }

        except Exception as e:
            # Handle any errors in the agent processing
            return {
                "response": f"I'm sorry, I encountered an error processing your request: {str(e)}",
                "tool_calls": [],
                "status": "error"
            }