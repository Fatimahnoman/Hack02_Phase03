import json
import logging
import os
import requests
from typing import Dict, Any, List
from sqlmodel import Session
from ..core.config import settings

logger = logging.getLogger(__name__)


class AgentService:
    """Service for managing chat interactions using OpenRouter API.

    This service handles natural language chat using OpenRouter's OpenAI-compatible API.
    """

    def __init__(self, session: Session, user_id: int = 1):
        self.session = session
        self.user_id = user_id
        self.settings = settings  # Store settings for later use

        # Store the API key and base URL for later use
        self.openrouter_api_key = settings.openrouter_api_key or ""
        if not self.openrouter_api_key:
            logger.warning("OPENROUTER_API_KEY not configured. Chat functionality will be limited.")

    def _register_tools(self) -> List[Dict[str, Any]]:
        """Register tools with the OpenAI agent."""
        # Define tool schemas for OpenAI function calling
        tool_definitions = []

        # Define tool schemas for OpenAI
        tool_definitions.append({
            "type": "function",
            "function": {
                "name": "create_task",
                "description": "Create a new task with a title and optional description, priority, and due date",
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
                        },
                        "due_date": {
                            "type": "string",
                            "description": "The due date for the task in ISO format (YYYY-MM-DDTHH:MM:SS) or natural language (e.g., '2026-02-23', 'Feb 23, 2026')"
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
                "description": "List all tasks with optional filtering by status, priority, and due date",
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
                        },
                        "due_date": {
                            "type": "string",
                            "description": "Filter tasks by due date (e.g., '2026-02-23', 'this week', 'next month')"
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
                            "description": "The ID of the task to update (can be the task title if ID is unknown)"
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
                        },
                        "due_date": {
                            "type": "string",
                            "description": "The new due date for the task in ISO format (YYYY-MM-DDTHH:MM:SS) or natural language (e.g., '2026-02-23', 'Feb 23, 2026')"
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
                            "description": "The ID of the task to complete (can be the task title if ID is unknown)"
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
                            "description": "The ID of the task to delete (can be the task title if ID is unknown)"
                        }
                    },
                    "required": ["task_id"]
                }
            }
        })

        tool_definitions.append({
            "type": "function",
            "function": {
                "name": "delete_all_tasks",
                "description": "Delete all tasks for the current user",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            }
        })

        tool_definitions.append({
            "type": "function",
            "function": {
                "name": "set_task_schedule",
                "description": "Set or update the schedule/due date for a specific task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "The ID of the task to update (can be the task title if ID is unknown)"
                        },
                        "due_date": {
                            "type": "string",
                            "description": "The due date for the task in ISO format (YYYY-MM-DDTHH:MM:SS) or natural language (e.g., '2026-02-23', 'Feb 23, 2026')"
                        }
                    },
                    "required": ["task_id", "due_date"]
                }
            }
        })

        tool_definitions.append({
            "type": "function",
            "function": {
                "name": "set_task_date",
                "description": "Set or update the due date for a specific task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "The ID of the task to update (can be the task title if ID is unknown)"
                        },
                        "due_date": {
                            "type": "string",
                            "description": "The due date for the task in ISO format (YYYY-MM-DDTHH:MM:SS) or natural language (e.g., '2026-02-23', 'Feb 23, 2026')"
                        }
                    },
                    "required": ["task_id", "due_date"]
                }
            }
        })

        tool_definitions.append({
            "type": "function",
            "function": {
                "name": "mark_task_incomplete",
                "description": "Mark a specific task as incomplete/pending",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "The ID of the task to mark as incomplete (can be the task title if ID is unknown)"
                        }
                    },
                    "required": ["task_id"]
                }
            }
        })

        return tool_definitions

    def process_request(self, user_input: str, conversation_history: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Process a user request through the OpenRouter API.

        Args:
            user_input: The user's natural language request
            conversation_history: The history of the conversation for context

        Returns:
            Dictionary containing the agent response and tool call metadata
        """
        # Check if OpenRouter API key is available
        if not self.openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY is not configured. Please set OPENROUTER_API_KEY in your environment.")

        # Register available tools
        tools = self._register_tools()

        # Build a system message that enables function calling
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an intelligent task-management chatbot.\n\n"
                    
                    "Your job is to understand what the user wants to do\n"
                    "and then make the correct backend/database operation.\n\n"
                    
                    "CORE RULE:\n"
                    "You are NOT allowed to guess or assume.\n"
                    "The database is the only source of truth.\n\n"
                    
                    "You MUST perform an actual backend action\n"
                    "before telling the user anything happened.\n\n"
                    
                    "USER INTENT UNDERSTANDING:\n"
                    "From every user message, determine EXACTLY ONE intent:\n\n"
                    
                    "- ADD_TASK            → user wants to add a new task\n"
                    "- UPDATE_TASK         → user wants to modify an existing task\n"
                    "- DELETE_TASK         → user wants to delete one task\n"
                    "- DELETE_ALL_TASKS    → user wants to delete all tasks\n"
                    "- LIST_TASKS          → user wants to see tasks\n"
                    "- MARK_COMPLETE       → user wants to mark task as complete\n"
                    "- MARK_INCOMPLETE     → user wants to mark task as incomplete\n\n"
                    
                    "Never mix intents.\n"
                    "Never default to ADD_TASK.\n\n"
                    
                    "INTENT EXAMPLES:\n"
                    "\"add gym at 6pm tomorrow\" → ADD_TASK\n"
                    "\"update grocery task to buy eggs\" → UPDATE_TASK\n"
                    "\"delete grocery task\" → DELETE_TASK\n"
                    "\"delete all my tasks\" → DELETE_ALL_TASKS\n"
                    "\"show my tasks\" → LIST_TASKS\n"
                    "\"mark gym as complete\" → MARK_COMPLETE\n"
                    "\"mark gym as incomplete\" → MARK_INCOMPLETE\n"
                    "\"mark [task name] as incomplete\" → MARK_INCOMPLETE\n"
                    "\"undo completion of [task name]\" → MARK_INCOMPLETE\n"
                    "\"set [task name] back to incomplete\" → MARK_INCOMPLETE\n"
                    "\"mark [task name] as not complete\" → MARK_INCOMPLETE\n"
                    "\"mark [task name] as undone\" → MARK_INCOMPLETE\n\n"
                    
                    "MANDATORY FLOW (NO EXCEPTIONS):\n"
                    "For EVERY request:\n\n"
                    
                    "1. Understand the user intent\n"
                    "2. Extract required data (task name, date, status, etc.)\n"
                    "3. Call the correct backend/database function\n"
                    "4. Wait for backend response\n"
                    "5. Respond ONLY using backend result\n\n"
                    
                    "RESPONSE RULES:\n"
                    "You may say an action was successful ONLY if:\n"
                    "- backend confirms success\n"
                    "- backend returns affected rows or task data\n\n"
                    
                    "If backend returns 0 or fails:\n"
                    "- say clearly that nothing was changed\n"
                    "- explain gently and honestly\n\n"
                    
                    "DELETE / UPDATE / STATUS RULE:\n"
                    "If user mentions a task that does not exist:\n"
                    "- Do NOT pretend it worked\n"
                    "- Say: \"I couldn't find that task in your database.\"\n\n"
                    
                    "LIST TASKS RULE:\n"
                    "When listing tasks:\n"
                    "- show only backend-returned tasks\n"
                    "- if list is empty, say so honestly\n\n"
                    
                    "DATE & TIME HANDLING:\n"
                    "Understand natural language dates:\n"
                    "\"today\", \"tomorrow\", \"25 feb 2026\", \"next monday\"\n\n"
                    
                    "Convert them properly.\n"
                    "Save or update them ONLY through backend.\n\n"
                    
                    "TONE & STYLE:\n"
                    "- Friendly\n"
                    "- Helpful\n"
                    "- Human\n"
                    "- Clear\n"
                    "- Never robotic\n"
                    "- Never fake-positive\n\n"
                    
                    "ABSOLUTE RESTRICTIONS:\n"
                    "- Never hallucinate success\n"
                    "- Never assume database state\n"
                    "- Never say something happened without backend proof\n"
                    "- If backend fails, say so clearly\n\n"
                    
                    "Your job is to understand, act, and then confirm — in that order.\n\n"
                    
                    "Use the user's request to determine if you need to call any functions. "
                    "If the user wants to create, list, update, complete, or delete tasks, call the appropriate function. "
                    "For create: use create_task function with title, description, and due_date "
                    "For list: use list_tasks function "
                    "For update: use update_task function with task_id and new information "
                    "For complete: use complete_task function with task_id "
                    "For delete: use delete_task function with task_id "
                    "For delete all: use delete_all_tasks function to delete all tasks "
                    "For setting task dates: use set_task_schedule function to update due dates "
                    "Only call functions when specifically requested by the user. For general questions, respond directly. "
                    "When users provide date information with tasks, extract the date and use it as the due_date parameter. "
                    "For example, if a user says 'add task name operation on 23 feb 2026', create a task with title 'operation' "
                    "and set the due_date parameter to '2026-02-23'. "
                    "For update tasks, recognize phrases like 'update task name', 'change task name', 'modify task', 'rename task', 'update task', 'update [taskname] task to [newname]', etc. "
                    "For example, if a user says 'update crocery task name to shopping with description cloths', "
                    "use update_task function with task_id='crocery' and new title='shopping' and description='cloths'. "
                    "Another example: if a user says 'update shopping task to Crocerry with description mugs', "
                    "use update_task function with task_id='shopping' and new title='Crocerry' and description='mugs'. "
                    "For update operations, extract the original task name, new task name, and description from the user's request. "
                    "For mark complete operations, if a user says 'mark grocery as complete', 'mark grocery task as complete', "
                    "or 'mark grocery task complete', use complete_task function with task_id='grocery'. "
                    "For mark incomplete operations, if a user says 'mark grocery as incomplete', 'mark grocery task as incomplete', "
                    "or 'mark grocery as not complete', use mark_task_incomplete function with task_id='grocery'. "
                    "Recognize common date formats like DD MMM YYYY, DD/MM/YYYY, DD-MM-YYYY, etc. "
                    "Support natural language date queries like 'overdue', 'today', 'this week', 'next week', 'this month' when listing tasks."
                )
            }
        ]

        # Add conversation history
        for msg in conversation_history:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            messages.append({"role": role, "content": content})

        # Add the current user input
        messages.append({"role": "user", "content": user_input})

        # Prepare the request payload
        # Note: OpenRouter has different support for tools/functions than OpenAI
        payload = {
            "model": settings.openrouter_model,
            "messages": messages,
            "temperature": float(os.getenv("AGENT_TEMPERATURE", settings.agent_temperature)),
            "max_tokens": int(os.getenv("MAX_RESPONSE_TOKENS", settings.max_response_tokens)),
        }
        
        # Only add tools parameter if the model supports it
        # Some OpenRouter models support function calling
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        headers = {
            "Authorization": f"Bearer {self.openrouter_api_key}",
            "Content-Type": "application/json"
        }

        try:
            # Make the API request directly
            response = requests.post(
                f"{self.settings.openrouter_base_url}/chat/completions",
                headers=headers,
                json=payload
            )

            # Check if the request was successful
            if response.status_code == 404:
                # If 404, the model might not support function calling
                # Fall back to a simple request without tools
                simple_payload = {
                    "model": settings.openrouter_model,
                    "messages": messages,
                    "temperature": float(os.getenv("AGENT_TEMPERATURE", settings.agent_temperature)),
                    "max_tokens": int(os.getenv("MAX_RESPONSE_TOKENS", settings.max_response_tokens)),
                }
                
                response = requests.post(
                    f"{self.settings.openrouter_base_url}/chat/completions",
                    headers=headers,
                    json=simple_payload
                )
                
                if response.status_code != 200:
                    logger.error(f"OpenRouter API error after fallback: {response.status_code} - {response.text}")
                    return {
                        "response": f"I'm sorry, I encountered an error with the AI service: {response.status_code}",
                        "tool_calls": [],
                        "status": "error"
                    }
            elif response.status_code != 200:
                logger.error(f"OpenRouter API error: {response.status_code} - {response.text}")
                return {
                    "response": f"I'm sorry, I encountered an error with the AI service: {response.status_code}",
                    "tool_calls": [],
                    "status": "error"
                }

            # Parse the response
            response_data = response.json()

            # Extract the AI response
            if "choices" in response_data and len(response_data["choices"]) > 0:
                choice = response_data["choices"][0]
                message = choice["message"]
                
                # Check if the model wants to call any functions
                # OpenRouter may return function calls in different formats
                tool_calls = []
                
                # Check for tool_calls in the response (OpenAI format)
                raw_tool_calls = message.get("tool_calls", [])
                
                # Alternative: Check for function_call in the response (older OpenAI format)
                if not raw_tool_calls and "function_call" in message:
                    raw_tool_calls = [{"id": "call_1", "function": message["function_call"], "type": "function"}]
                
                if raw_tool_calls:
                    # Process tool calls
                    for raw_tool_call in raw_tool_calls:
                        if raw_tool_call.get("type") == "function":
                            tool_call = raw_tool_call["function"]
                            tool_name = tool_call["name"]
                            tool_args = json.loads(tool_call["arguments"])
                            
                            # Execute the tool call and get result
                            tool_result = self._execute_tool(tool_name, tool_args)
                            
                            # Add the tool result to the conversation
                            messages.append({
                                "role": "tool",
                                "content": json.dumps(tool_result),
                                "tool_call_id": raw_tool_call["id"]
                            })
                            
                            tool_calls.append({
                                "name": tool_name,
                                "arguments": tool_args,
                                "result": tool_result
                            })
                        
                    # If there were tool calls, make a second request to get the final response
                    if tool_calls:
                        # Add assistant message acknowledging the tool call
                        assistant_message = {
                            "role": "assistant",
                            "content": None
                        }
                        if "tool_calls" in message:
                            assistant_message["tool_calls"] = message["tool_calls"]
                        messages.append(assistant_message)
                        
                        # Make a second API call to get the final response after tool execution
                        final_payload = {
                            "model": settings.openrouter_model,
                            "messages": messages,
                            "temperature": float(os.getenv("AGENT_TEMPERATURE", settings.agent_temperature)),
                            "max_tokens": int(os.getenv("MAX_RESPONSE_TOKENS", settings.max_response_tokens)),
                        }
                        
                        # Add tools to final payload if they were originally included
                        if tools:
                            final_payload["tools"] = tools
                        
                        final_response = requests.post(
                            f"{settings.openrouter_base_url}/chat/completions",
                            headers=headers,
                            json=final_payload
                        )
                        
                        if final_response.status_code == 200:
                            final_response_data = final_response.json()
                            if "choices" in final_response_data and len(final_response_data["choices"]) > 0:
                                final_message = final_response_data["choices"][0]["message"]
                                ai_response = final_message.get("content", "")

                                # If there's no content in the final response, use the tool result message
                                if not ai_response.strip():
                                    # Use the message from the first tool call result
                                    if tool_calls and len(tool_calls) > 0:
                                        first_tool_call = tool_calls[0]
                                        if "result" in first_tool_call:
                                            result = first_tool_call["result"]
                                            # Prioritize the message from the tool result if available
                                            if "message" in result:
                                                ai_response = result["message"]
                                            elif "error" in result:
                                                ai_response = result["error"]
                                            else:
                                                ai_response = "Operation completed successfully!"
                                        else:
                                            ai_response = "Operation completed successfully!"
                                else:
                                    # If AI provided a follow-up response, check if we should enhance it with tool results
                                    if tool_calls and len(tool_calls) > 0:
                                        first_tool_call = tool_calls[0]
                                        if "result" in first_tool_call:
                                            result = first_tool_call["result"]
                                            if "message" in result:
                                                # For list operations, we want to prioritize the detailed list message
                                                # rather than appending to a generic AI response
                                                if first_tool_call["name"] == "list_tasks":
                                                    # For list operations, use the detailed list message instead of AI's generic response
                                                    ai_response = result["message"]
                                                else:
                                                    # For other operations, append the success message if AI response is generic
                                                    if len(ai_response.strip()) < 50 and "operation" in ai_response.lower():
                                                        ai_response = result["message"]
                                                    else:
                                                        # Only append if it adds value
                                                        ai_response += f"\n\n{result['message']}"
                                            elif "error" in result:
                                                ai_response = result["error"]
                            else:
                                # If no choices in response, use the tool result message
                                if tool_calls and len(tool_calls) > 0:
                                    first_tool_call = tool_calls[0]
                                    if "result" in first_tool_call:
                                        result = first_tool_call["result"]
                                        if "message" in result:
                                            ai_response = result["message"]
                                        elif "error" in result:
                                            ai_response = result["error"]
                                        else:
                                            ai_response = "I've processed your request using the appropriate tools."
                                else:
                                    ai_response = "I've processed your request using the appropriate tools."
                        else:
                            # If the second request failed, use the message from the tool result
                            if tool_calls and len(tool_calls) > 0:
                                first_tool_call = tool_calls[0]
                                if "result" in first_tool_call:
                                    result = first_tool_call["result"]
                                    if "message" in result:
                                        ai_response = result["message"]
                                    elif "error" in result:
                                        ai_response = result["error"]
                                    else:
                                        ai_response = "Operation completed successfully!"
                                else:
                                    ai_response = "Operation completed successfully!"
                            else:
                                ai_response = "I've processed your request using the appropriate tools."
                    else:
                        ai_response = message.get("content", "")
                else:
                    ai_response = message.get("content", "")
                
                return {
                    "response": ai_response,
                    "tool_calls": tool_calls,
                    "status": "success"
                }
            else:
                logger.warning(f"Unexpected response format from OpenRouter: {response_data}")
                return {
                    "response": "I'm sorry, I received an unexpected response from the AI service.",
                    "tool_calls": [],
                    "status": "error"
                }

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error when calling OpenRouter API: {str(e)}")
            return {
                "response": f"I'm sorry, I encountered a network error: {str(e)}",
                "tool_calls": [],
                "status": "error"
            }
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error when parsing OpenRouter response: {str(e)}")
            logger.error(f"Response text: {response.text[:500]}...")  # Log first 500 chars of response
            return {
                "response": "I'm sorry, I received an invalid response from the AI service.",
                "tool_calls": [],
                "status": "error"
            }
        except Exception as e:
            logger.error(f"Unexpected error when calling OpenRouter API: {str(e)}")
            return {
                "response": f"I'm sorry, I encountered an unexpected error: {str(e)}",
                "tool_calls": [],
                "status": "error"
            }

    def _execute_tool(self, tool_name: str, tool_args: dict) -> dict:
        """
        Execute a specific tool with the given arguments.
        
        Args:
            tool_name: The name of the tool to execute
            tool_args: Arguments for the tool
            
        Returns:
            Result of the tool execution
        """
        try:
            if tool_name == "create_task":
                return self._create_task(tool_args)
            elif tool_name == "list_tasks":
                return self._list_tasks(tool_args)
            elif tool_name == "update_task":
                return self._update_task(tool_args)
            elif tool_name == "complete_task":
                return self._complete_task(tool_args)
            elif tool_name == "delete_task":
                return self._delete_task(tool_args)
            elif tool_name == "delete_all_tasks":
                return self._delete_all_tasks(tool_args)
            elif tool_name == "set_task_schedule":
                return self._set_task_schedule(tool_args)
            elif tool_name == "set_task_date":
                # Map set_task_date to the same function as set_task_schedule
                return self._set_task_schedule(tool_args)
            elif tool_name == "mark_task_incomplete":
                return self._mark_task_incomplete(tool_args)
            else:
                return {"error": f"Unknown tool: {tool_name}"}
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {str(e)}")
            return {"error": f"Error executing tool {tool_name}: {str(e)}"}

    def _create_task(self, args: dict) -> dict:
        """Create a new task in the database."""
        from ..models.task import Task
        from sqlmodel import select
        import uuid
        from datetime import datetime
        import re

        # Extract title and description from the input
        title = args.get("title", "")
        description = args.get("description", "")

        # If the title contains date information, separate it
        # Look for common date patterns in the title and move them to description
        date_patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',  # MM/DD/YYYY or MM-DD-YYYY
            r'\b\d{1,2}\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{2,4}\b',  # 23 Feb 2026
            r'\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{1,2},?\s*\d{2,4}\b',  # Feb 23, 2026
            r'\b\d{1,2}\s+(january|february|march|april|may|june|july|august|september|october|november|december)[a-z]*\s+\d{2,4}\b',  # 23 February 2026
        ]

        # Check if title contains a date pattern
        combined_text = f"{title} {description}".strip()
        for pattern in date_patterns:
            matches = re.findall(pattern, combined_text, re.IGNORECASE)
            if matches:
                # Extract the date part and remove it from the title
                for match in matches:
                    # If match is a tuple (from grouped patterns), get the first element
                    if isinstance(match, tuple):
                        match = match[0]
                    # Remove the date from the title to get a cleaner task name
                    if match.lower() in title.lower():
                        # Extract the main task name by removing the date part
                        clean_title = re.sub(r'\b(on|at|for)\s+' + re.escape(match) + r'\b', '', title, flags=re.IGNORECASE).strip()
                        clean_title = re.sub(r'\s+', ' ', clean_title)  # Clean up extra spaces
                        if clean_title:
                            title = clean_title
                        description = f"{description} Scheduled for: {match}".strip()
                    else:
                        description = f"{description} Scheduled for: {match}".strip()
                break

        # Extract and parse due date from description if present
        due_date = None
        # Look for date information in the description and parse it
        if "Scheduled for:" in description:
            date_part = description.split("Scheduled for:")[-1].strip()
            # Try to parse the date - this is a simplified version
            # In a production system, you'd want more robust date parsing
            try:
                import re
                from datetime import datetime
                # Look for common date formats in the description
                date_match = re.search(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})|(\d{1,2}\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{2,4})|((jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{1,2},?\s*\d{2,4})|(\d{1,2}\s+(january|february|march|april|may|june|july|august|september|october|november|december)[a-z]*\s+\d{2,4})', description, re.IGNORECASE)
                
                if date_match:
                    date_str = date_match.group(0)
                    # Try to parse the date in various formats
                    date_formats = [
                        '%m/%d/%Y', '%m-%d-%Y', '%d/%m/%Y', '%d-%m-%Y',
                        '%d %b %Y', '%d %B %Y', '%B %d, %Y', '%b %d, %Y',
                        '%B %d %Y', '%b %d %Y'
                    ]
                    
                    for fmt in date_formats:
                        try:
                            due_date = datetime.strptime(date_str, fmt)
                            break
                        except ValueError:
                            continue
            except:
                # If parsing fails, just continue without a due date
                pass
        
        # Create a new task
        task = Task(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            status="pending",
            priority=args.get("priority", "medium"),
            due_date=due_date,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            user_id=self.user_id
        )

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        return {"success": True, "task_id": task.id, "message": f"Got it! I've added your task '{task.title}' to your list 🌟"}

    def _list_tasks(self, args: dict) -> dict:
        """List tasks from the database."""
        from ..models.task import Task
        from sqlmodel import select
        from datetime import datetime, timedelta

        # Build query based on filters
        query = select(Task).where(Task.user_id == self.user_id)

        status = args.get("status")
        if status:
            query = query.where(Task.status == status)

        priority = args.get("priority")
        if priority:
            query = query.where(Task.priority == priority)

        due_date_filter = args.get("due_date")
        if due_date_filter:
            # Handle different due date filters
            if due_date_filter.lower() == "overdue":
                query = query.where(Task.due_date < datetime.utcnow())
            elif due_date_filter.lower() == "today":
                today_start = datetime.combine(datetime.utcnow().date(), datetime.min.time())
                today_end = datetime.combine(datetime.utcnow().date(), datetime.max.time())
                query = query.where(Task.due_date >= today_start).where(Task.due_date <= today_end)
            elif due_date_filter.lower() == "this week":
                week_start = datetime.utcnow() - timedelta(days=datetime.utcnow().weekday())
                week_end = week_start + timedelta(days=7)
                query = query.where(Task.due_date >= week_start).where(Task.due_date <= week_end)
            elif due_date_filter.lower() == "next week":
                next_week_start = datetime.utcnow() + timedelta(days=(7 - datetime.utcnow().weekday()))
                next_week_end = next_week_start + timedelta(days=7)
                query = query.where(Task.due_date >= next_week_start).where(Task.due_date <= next_week_end)
            elif due_date_filter.lower() == "this month":
                month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                if month_start.month == 12:
                    month_end = month_start.replace(year=month_start.year + 1, month=1, day=1) - timedelta(seconds=1)
                else:
                    month_end = month_start.replace(month=month_start.month + 1) - timedelta(seconds=1)
                query = query.where(Task.due_date >= month_start).where(Task.due_date <= month_end)
            else:
                # Try to parse as a specific date
                try:
                    parsed_date = datetime.strptime(due_date_filter, "%Y-%m-%d")
                    next_day = parsed_date + timedelta(days=1)
                    query = query.where(Task.due_date >= parsed_date).where(Task.due_date < next_day)
                except ValueError:
                    # If parsing fails, ignore the due_date filter
                    pass

        tasks = self.session.exec(query).all()

        # Format the response message based on the number of tasks
        if len(tasks) == 0:
            message = "You don't have any tasks in your list right now."
        elif len(tasks) == 1:
            message = f"You have 1 task in your list:"
        else:
            message = f"Here are your {len(tasks)} tasks:"

        # Format each task for display
        task_details = []
        for task in tasks:
            status_icon = "✅" if task.status == "completed" else "⏳" if task.status == "in-progress" else "📝"
            due_date_str = f" (Due: {task.due_date.strftime('%b %d, %Y')})" if task.due_date else ""
            task_details.append(f"{status_icon} {task.title} - {task.description or 'No description'}{due_date_str}")

        full_message = f"{message}\n\n" + "\n".join([f"• {detail}" for detail in task_details])

        return {
            "success": True,
            "tasks": [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "priority": task.priority,
                    "due_date": task.due_date.isoformat() if task.due_date else None
                }
                for task in tasks
            ],
            "message": full_message
        }

    def _update_task(self, args: dict) -> dict:
        """Update an existing task in the database."""
        from ..models.task import Task
        from sqlmodel import select
        from datetime import datetime

        task_id = args.get("task_id")

        # Try to find the task by ID first, then by title if ID not found
        task = self.session.get(Task, task_id)
        if not task:
            # If task_id is not a valid UUID, treat it as a title
            query = select(Task).where(
                (Task.title == task_id) & (Task.user_id == self.user_id)
            )
            task = self.session.exec(query).first()

        if not task:
            return {"error": f"⚠ I couldn't find the task '{task_id}' in your database."}

        # Update task properties
        if "title" in args:
            task.title = args["title"]
        if "description" in args:
            task.description = args["description"]
        if "status" in args:
            task.status = args["status"]
        if "priority" in args:
            task.priority = args["priority"]
        if "due_date" in args:
            task.due_date = args["due_date"]

        task.updated_at = datetime.utcnow()

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        return {"success": True, "task_id": task.id, "message": f"Perfect! I've updated your task to '{task.title}' 📝"}

    def _complete_task(self, args: dict) -> dict:
        """Mark a task as completed in the database."""
        from ..models.task import Task
        from sqlmodel import select
        from datetime import datetime

        task_id = args.get("task_id")

        # Try to find the task by ID first, then by title if ID not found
        task = self.session.get(Task, task_id)
        if not task:
            # If task_id is not a valid UUID, treat it as a title
            query = select(Task).where(
                (Task.title == task_id) & (Task.user_id == self.user_id)
            )
            task = self.session.exec(query).first()

        if not task:
            return {"error": f"⚠ I couldn't find the task '{task_id}' in your database."}

        task.status = "completed"
        task.completed_at = datetime.utcnow()
        task.updated_at = datetime.utcnow()

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        return {"success": True, "task_id": task.id, "message": f"Great job! I've marked '{task.title}' as completed ✅"}

    def _mark_task_incomplete(self, args: dict) -> dict:
        """Mark a task as incomplete in the database."""
        from ..models.task import Task
        from sqlmodel import select
        from datetime import datetime

        task_id = args.get("task_id")

        # Try to find the task by ID first, then by title if ID not found
        task = self.session.get(Task, task_id)
        if not task:
            # If task_id is not a valid UUID, treat it as a title
            query = select(Task).where(
                (Task.title == task_id) & (Task.user_id == self.user_id)
            )
            task = self.session.exec(query).first()

        if not task:
            return {"error": f"⚠ I couldn't find the task '{task_id}' in your database."}

        task.status = "pending"
        task.completed_at = None  # Clear the completion date
        task.updated_at = datetime.utcnow()

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        return {"success": True, "task_id": task.id, "message": f"✅ Task '{task.title}' is now marked as incomplete."}

    def _delete_task(self, args: dict) -> dict:
        """Delete a task from the database."""
        from ..models.task import Task
        from sqlmodel import select
        
        task_id = args.get("task_id")
        
        # Try to find the task by ID first, then by title if ID not found
        task = self.session.get(Task, task_id)
        if not task:
            # If task_id is not a valid UUID, treat it as a title
            query = select(Task).where(
                (Task.title == task_id) & (Task.user_id == self.user_id)
            )
            task = self.session.exec(query).first()
        
        if not task:
            return {"error": f"⚠ I couldn't find the task '{task_id}' in your database."}
        
        self.session.delete(task)
        self.session.commit()

        return {"success": True, "task_id": task.id, "message": f"Done! I've removed '{task.title}' from your list 🗑️"}

    def _delete_all_tasks(self, args: dict) -> dict:
        """Delete all tasks for the current user from the database."""
        from ..models.task import Task
        from sqlmodel import select

        # Query all tasks for the current user
        query = select(Task).where(Task.user_id == self.user_id)
        tasks = self.session.exec(query).all()

        # Delete all tasks
        for task in tasks:
            self.session.delete(task)

        self.session.commit()

        if len(tasks) > 0:
            return {"success": True, "deleted_count": len(tasks), "message": f"I've deleted all {len(tasks)} of your tasks 🗑️"}
        else:
            return {"success": True, "deleted_count": 0, "message": f"I checked your database and couldn't find any tasks to delete."}

    def _set_task_schedule(self, args: dict) -> dict:
        """Set or update the schedule/due date for a specific task."""
        from ..models.task import Task
        from sqlmodel import select
        from datetime import datetime
        import re

        task_id = args.get("task_id")
        due_date_str = args.get("due_date")

        # Try to find the task by ID first, then by title if ID not found
        task = self.session.get(Task, task_id)
        if not task:
            # If task_id is not a valid UUID, treat it as a title
            query = select(Task).where(
                (Task.title == task_id) & (Task.user_id == self.user_id)
            )
            task = self.session.exec(query).first()

        if not task:
            return {"error": f"⚠ I couldn't find the task '{task_id}' in your database."}

        # Parse the due date
        due_date = None
        if due_date_str:
            try:
                # Try to parse the date in various formats
                date_formats = [
                    '%Y-%m-%d', '%m/%d/%Y', '%m-%d-%Y', '%d/%m/%Y', '%d-%m-%Y',
                    '%d %b %Y', '%d %B %Y', '%B %d, %Y', '%b %d, %Y',
                    '%B %d %Y', '%b %d %Y'
                ]
                
                for fmt in date_formats:
                    try:
                        due_date = datetime.strptime(due_date_str, fmt)
                        break
                    except ValueError:
                        continue
                
                # If none of the standard formats work, try to extract date from natural language
                if due_date is None:
                    # Look for common date patterns in the string
                    date_patterns = [
                        r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',  # MM/DD/YYYY or MM-DD-YYYY
                        r'\b\d{1,2}\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{2,4}\b',  # 23 Feb 2026
                        r'\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{1,2},?\s*\d{2,4}\b',  # Feb 23, 2026
                        r'\b\d{1,2}\s+(january|february|march|april|may|june|july|august|september|october|november|december)[a-z]*\s+\d{2,4}\b',  # 23 February 2026
                    ]

                    for pattern in date_patterns:
                        matches = re.findall(pattern, due_date_str, re.IGNORECASE)
                        if matches:
                            date_str = matches[0]
                            if isinstance(date_str, tuple):
                                date_str = date_str[0]
                            
                            # Try to parse the extracted date
                            for fmt in date_formats:
                                try:
                                    due_date = datetime.strptime(date_str, fmt)
                                    break
                                except ValueError:
                                    continue
                            if due_date:
                                break
            except Exception:
                # If parsing fails, leave due_date as None
                pass

        # Update the task's due date
        task.due_date = due_date
        task.updated_at = datetime.utcnow()

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        if due_date:
            return {"success": True, "task_id": task.id, "message": f"Done! I've scheduled your task '{task.title}' for {due_date.strftime('%b %d, %Y')} 📅"}
        else:
            return {"success": True, "task_id": task.id, "message": f"Sorry, I couldn't understand the date for task '{task.title}'. Could you try a different format?"}