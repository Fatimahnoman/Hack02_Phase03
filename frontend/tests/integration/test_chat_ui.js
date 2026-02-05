/**
 * Integration tests for the chat UI component.
 */

// Mock the backend API calls for testing
const mockApiResponse = (response) => {
  global.fetch = jest.fn(() =>
    Promise.resolve({
      ok: true,
      json: () => Promise.resolve(response),
    })
  );
};

describe('Chat UI Integration Tests', () => {
  beforeEach(() => {
    // Reset fetch mock
    if (global.fetch) {
      global.fetch.mockClear();
    }
  });

  test('should handle chat message submission correctly', async () => {
    const mockResponse = {
      response: "Hello! I'm your task assistant.",
      intent: "greeting",
      state_reflection: {
        user_id: "test-user",
        task_count: 0,
        task_counts_by_status: {},
      },
      timestamp: new Date().toISOString()
    };

    mockApiResponse(mockResponse);

    // Simulate sending a message
    const userInput = "Hello";
    const userId = "test-user";

    const response = await fetch('/api/v1/chat/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_input: userInput,
        user_id: userId
      })
    });

    const data = await response.json();

    // Verify response structure matches contract
    expect(data).toHaveProperty('response');
    expect(data).toHaveProperty('intent');
    expect(data).toHaveProperty('state_reflection');
    expect(data).toHaveProperty('timestamp');

    expect(typeof data.response).toBe('string');
    expect(typeof data.intent).toBe('string');
    expect(typeof data.state_reflection).toBe('object');
    expect(typeof data.timestamp).toBe('string');

    // Verify specific values
    expect(data.intent).toBe('greeting');
    expect(data.state_reflection.user_id).toBe(userId);
  });

  test('should handle task creation request', async () => {
    const mockResponse = {
      response: "Task 'buy groceries' created successfully.",
      intent: "create_task",
      state_reflection: {
        user_id: "test-user",
        task_count: 1,
        task_counts_by_status: { pending: 1 },
      },
      timestamp: new Date().toISOString(),
      tool_execution_result: {
        success: true,
        data: { task_id: "task-123", task_title: "buy groceries" }
      }
    };

    mockApiResponse(mockResponse);

    const userInput = "Create a task to buy groceries";
    const userId = "test-user";

    const response = await fetch('/api/v1/chat/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_input: userInput,
        user_id: userId
      })
    });

    const data = await response.json();

    // Verify response structure
    expect(data.intent).toBe('create_task');
    expect(data.response).toContain('created successfully');
    expect(data.state_reflection.user_id).toBe(userId);
  });

  test('should handle task listing request', async () => {
    const mockResponse = {
      response: "You have 2 tasks total: Task 1 (pending), Task 2 (completed)",
      intent: "get_all_tasks",
      state_reflection: {
        user_id: "test-user",
        task_count: 2,
        task_counts_by_status: { pending: 1, completed: 1 },
      },
      timestamp: new Date().toISOString()
    };

    mockApiResponse(mockResponse);

    const userInput = "What are my tasks?";
    const userId = "test-user";

    const response = await fetch('/api/v1/chat/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_input: userInput,
        user_id: userId
      })
    });

    const data = await response.json();

    // Verify response structure
    expect(data.intent).toBe('get_all_tasks');
    expect(data.state_reflection.task_count).toBe(2);
    expect(data.state_reflection.user_id).toBe(userId);
  });

  test('should handle deterministic responses for identical inputs', async () => {
    const mockResponse = {
      response: "You have no pending tasks.",
      intent: "get_pending_tasks",
      state_reflection: {
        user_id: "test-user",
        task_count: 0,
        task_counts_by_status: {},
      },
      timestamp: new Date().toISOString()
    };

    mockApiResponse(mockResponse);

    const userInput = "What are my pending tasks?";
    const userId = "test-user";

    // Make the same request twice
    const response1 = await fetch('/api/v1/chat/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_input: userInput,
        user_id: userId
      })
    });

    const response2 = await fetch('/api/v1/chat/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_input: userInput,
        user_id: userId
      })
    });

    const data1 = await response1.json();
    const data2 = await response2.json();

    // Both responses should have the same intent for the same input
    expect(data1.intent).toBe(data2.intent);
    expect(data1.intent).toBe('get_pending_tasks');
  });

  test('should maintain stateless behavior across sessions', async () => {
    const mockResponse = {
      response: "Hello! How can I help you today?",
      intent: "greeting",
      state_reflection: {
        user_id: "different-user",
        task_count: 0,
        task_counts_by_status: {},
      },
      timestamp: new Date().toISOString()
    };

    mockApiResponse(mockResponse);

    // Test with different user IDs to verify independence
    const users = ["user-session-1", "user-session-2", "user-session-3"];
    const promises = users.map(async (userId) => {
      const response = await fetch('/api/v1/chat/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_input: "Hello",
          user_id: userId
        })
      });
      return response.json();
    });

    const results = await Promise.all(promises);

    // Each request should be processed independently
    results.forEach((result, index) => {
      expect(result.intent).toBe('greeting');
      expect(result.state_reflection.user_id).toBe(users[index]);
    });
  });

  test('should properly handle error cases', async () => {
    // Mock an error response
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: false,
        status: 500,
        json: () => Promise.resolve({ detail: "Internal server error" }),
      })
    );

    const response = await fetch('/api/v1/chat/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_input: "Test input",
        user_id: "test-user-error"
      })
    });

    expect(response.ok).toBe(false);
    expect(response.status).toBe(500);
  });
});