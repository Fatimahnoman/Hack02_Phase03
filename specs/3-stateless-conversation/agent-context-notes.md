# Agent Context Update Notes: Stateless Conversation Cycle

## Context Added to Agent

### Key Principles of Stateless Operation
- The chatbot operates without storing or reusing chat history
- Each message is treated as a fresh request
- All state comes from user input, database, and tool results only
- No reliance on past conversation memory

### Processing Workflow
1. **Intent-First Processing**: Parse user intent from current input only
2. **Data Fetch Before Action**: Always read from DB before updating/deleting/completing tasks
3. **Tool Execution Discipline**: Call only one tool per intent with full validated parameters
4. **Tool Result Validation**: Check tool return status; report errors honestly if failure
5. **Response From Reality**: Generate response from tool output and database state only

### Database Integration Points
- User state queries before actions
- Task retrieval and updates
- Conversation context storage (in DB, not memory)
- Intent logging for audit and consistency verification

### Validation Requirements
- Restart-safe behavior (identical inputs produce identical outputs after restart)
- Stateless operation (no assumed context between requests)
- Agent compatibility (works with existing tooling and frameworks)

### Error Handling Patterns
- Handle database query failures gracefully
- Process malformed inputs without conversation context
- Manage concurrent requests safely
- Respond appropriately when database records are unavailable

### Testing Considerations
- Verify deterministic behavior across server restarts
- Ensure responses reflect actual database state
- Test concurrent user scenarios
- Validate tool execution success/failure handling