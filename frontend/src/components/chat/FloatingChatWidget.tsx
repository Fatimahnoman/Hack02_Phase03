import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../../hooks/useAuth';

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
}

const FloatingChatWidget: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [inputMessage, setInputMessage] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);
  const { user, isAuthenticated } = useAuth();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading || !isAuthenticated) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputMessage,
      role: 'user',
      timestamp: new Date(),
    };

    // Add user message to UI immediately
    setMessages(prev => [...prev, userMessage]);
    const messageToSend = inputMessage;
    setInputMessage('');
    setIsLoading(true);

    try {
      // Call the backend chat API
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/chat/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: JSON.stringify({
          user_input: messageToSend,
          user_id: user ? user.id.toString() : 'anonymous',
          session_metadata: {
            conversation_id: currentConversationId || undefined
          }
        }),
      });

      if (!response.ok) {
        throw new Error(`Chat API error: ${response.status}`);
      }

      const data = await response.json();

      // Update conversation ID if this is the first message
      if (!currentConversationId) {
        setCurrentConversationId(data.conversation_id);
      }

      const assistantMessage: Message = {
        id: Date.now().toString(),
        content: data.response,
        role: 'assistant',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        id: Date.now().toString(),
        content: 'Sorry, I encountered an error. Please try again.',
        role: 'assistant',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const startNewConversation = () => {
    setMessages([]);
    setCurrentConversationId(null);
  };

  return (
    <div className="floating-chat-widget">
      {/* Floating Button */}
      <button
        className={`chat-toggle-btn ${isOpen ? 'open' : ''}`}
        onClick={() => {
          if (isAuthenticated) {
            setIsOpen(!isOpen);
          } else {
            alert('Please sign in to use the chat');
          }
        }}
      >
        {isOpen ? '×' : '💬'}
      </button>

      {/* Chat Popup */}
      {isOpen && isAuthenticated && (
        <div className="chat-popup">
          <div className="chat-header">
            <h3>AI Assistant</h3>
            <button onClick={startNewConversation} className="new-conversation-btn">
              New Chat
            </button>
            <button
              onClick={() => setIsOpen(false)}
              className="close-btn"
            >
              ×
            </button>
          </div>

          <div className="messages-container">
            {messages.length === 0 ? (
              <div className="welcome-message">
                <h4>Hello! I'm your AI assistant.</h4>
                <p>Ask me anything about your todos, or just chat with me!</p>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`message ${message.role}`}
                >
                  <div className="message-content">
                    {message.content}
                  </div>
                  <div className="message-timestamp">
                    {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                </div>
              ))
            )}
            {isLoading && (
              <div className="message assistant">
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="input-container">
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              disabled={isLoading}
              rows={2}
            />
            <button
              onClick={sendMessage}
              disabled={isLoading || !inputMessage.trim()}
              className="send-button"
            >
              Send
            </button>
          </div>
        </div>
      )}

      {/* Auth Prompt when not authenticated */}
      {isOpen && !isAuthenticated && (
        <div className="chat-popup">
          <div className="chat-header">
            <h3>AI Assistant</h3>
            <button
              onClick={() => setIsOpen(false)}
              className="close-btn"
            >
              ×
            </button>
          </div>
          <div className="auth-prompt">
            <p>Please sign in to use the chat assistant.</p>
          </div>
        </div>
      )}

      <style jsx>{`
        .floating-chat-widget {
          position: fixed;
          bottom: 20px;
          right: 20px;
          z-index: 1000;
        }

        .chat-toggle-btn {
          width: 60px;
          height: 60px;
          border-radius: 50%;
          border: none;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          font-size: 24px;
          cursor: pointer;
          box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
          display: flex;
          align-items: center;
          justify-content: center;
          transition: all 0.3s ease;
        }

        .chat-toggle-btn:hover {
          transform: scale(1.1);
          box-shadow: 0 6px 25px rgba(0, 0, 0, 0.3);
        }

        .chat-toggle-btn.open {
          background: #e53e3e;
        }

        .chat-popup {
          position: absolute;
          bottom: 80px;
          right: 0;
          width: 350px;
          height: 500px;
          background: white;
          border-radius: 16px;
          box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
          display: flex;
          flex-direction: column;
          overflow: hidden;
        }

        .chat-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 15px 20px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
        }

        .chat-header h3 {
          margin: 0;
          font-size: 1.2rem;
        }

        .new-conversation-btn {
          background: rgba(255, 255, 255, 0.2);
          color: white;
          border: 1px solid rgba(255, 255, 255, 0.3);
          padding: 5px 10px;
          border-radius: 6px;
          cursor: pointer;
          font-size: 0.8rem;
          margin-right: 10px;
        }

        .new-conversation-btn:hover {
          background: rgba(255, 255, 255, 0.3);
        }

        .close-btn {
          background: none;
          border: none;
          color: white;
          font-size: 24px;
          cursor: pointer;
          padding: 0;
          width: 30px;
          height: 30px;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .messages-container {
          flex: 1;
          overflow-y: auto;
          padding: 20px;
          display: flex;
          flex-direction: column;
          gap: 15px;
          background: #f8fafc;
        }

        .welcome-message {
          text-align: center;
          padding: 20px;
          color: #718096;
        }

        .welcome-message h4 {
          margin: 0 0 10px 0;
          color: #2d3748;
        }

        .message {
          max-width: 80%;
          padding: 12px 15px;
          border-radius: 18px;
          position: relative;
          animation: fadeIn 0.3s ease;
        }

        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }

        .user {
          align-self: flex-end;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border-bottom-right-radius: 5px;
        }

        .assistant {
          align-self: flex-start;
          background: #e6fffa;
          color: #234e52;
          border: 1px solid #b2f5ea;
          border-bottom-left-radius: 5px;
        }

        .message-content {
          word-wrap: break-word;
        }

        .typing-indicator {
          display: flex;
          gap: 5px;
        }

        .typing-indicator span {
          width: 8px;
          height: 8px;
          background: #a0aec0;
          border-radius: 50%;
          animation: bounce 1.5s infinite ease-in-out;
        }

        .typing-indicator span:nth-child(2) {
          animation-delay: 0.2s;
        }

        .typing-indicator span:nth-child(3) {
          animation-delay: 0.4s;
        }

        @keyframes bounce {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-5px); }
        }

        .message-timestamp {
          font-size: 0.7rem;
          color: #a0aec0;
          text-align: right;
          margin-top: 5px;
        }

        .input-container {
          display: flex;
          padding: 15px;
          background: white;
          border-top: 1px solid #e2e8f0;
        }

        textarea {
          flex: 1;
          padding: 10px 12px;
          border: 1px solid #e2e8f0;
          border-radius: 12px;
          resize: none;
          font-family: inherit;
          font-size: 0.9rem;
          outline: none;
          transition: border-color 0.3s ease;
        }

        textarea:focus {
          border-color: #667eea;
        }

        .send-button {
          margin-left: 10px;
          padding: 10px 16px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border: none;
          border-radius: 12px;
          cursor: pointer;
          transition: opacity 0.3s ease;
          font-size: 0.9rem;
        }

        .send-button:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }

        .send-button:not(:disabled):hover {
          opacity: 0.9;
        }

        .auth-prompt {
          flex: 1;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 20px;
          text-align: center;
          color: #718096;
        }

        @media (max-width: 768px) {
          .chat-popup {
            width: 300px;
            height: 400px;
            right: 0;
          }

          .chat-toggle-btn {
            width: 50px;
            height: 50px;
          }
        }
      `}</style>
    </div>
  );
};

export default FloatingChatWidget;