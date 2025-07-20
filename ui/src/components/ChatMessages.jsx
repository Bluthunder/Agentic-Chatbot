import React from 'react';
import '../app.css';


const ChatMessages = ({ messages, onExampleClick }) => {
  return (
    <div className="chat-messages" id="chatMessages">
      {/* Welcome Message (shown only if no chat history) */}
      {messages.length === 0 && (
        <div className="welcome-message">
          <h3>Welcome to Agentic Chatbot!</h3>
          <p>
            I'm your intelligent travel assistant powered by multiple AI agents. I can help you with:
          </p>
          <div className="example-queries">
            <div className="example-query" onClick={() => onExampleClick('Book a flight from Mumbai to Delhi on December 15th')}>
              ✈️ Flight Booking
            </div>
            <div className="example-query" onClick={() => onExampleClick("What's the status of my flight FL123?")}>
              📊 Flight Status
            </div>
            <div className="example-query" onClick={() => onExampleClick("I want to cancel my booking")}>
              ❌ Cancel Booking
            </div>
            <div className="example-query" onClick={() => onExampleClick("Hello, how can you help me?")}>
              👋 General Help
            </div>
          </div>
        </div>
      )}

      {/* Chat Messages */}
      {messages.map((msg, idx) => (
        <div key={idx} className={`message ${msg.sender}`}>
          <div className="message-avatar">{msg.sender === 'user' ? '👤' : '🤖'}</div>
          <div className="message-content">
            <div dangerouslySetInnerHTML={{ __html: msg.text.replace(/\n/g, '<br>') }}></div>
            {msg.metadata && (
              <div className="message-meta">
                {Object.entries(msg.metadata).map(([key, value]) => (
                  <span key={key} className="meta-item">
                    {key}: {value}
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};

export default ChatMessages;
