import React from 'react';

const ChatHeader = ({ isConnected, toggleExpand, toggleChat}) => {
  return (
    <div className="chat-header">
      <div className="status-indicator">
        <div className={`status-dot ${isConnected ? 'connected' : ''}`}></div>
        <span>{isConnected ? 'Connected' : 'Connecting...'}</span>
      </div>
      <h1>🤖 Agentic Chatbot</h1>
      <p>AI-Powered Travel Assistant with Multi-Agent Intelligence</p>
      <div className="chat-header-buttons">
        <button className="chat-header-btn" onClick={toggleExpand} title="Expand/Collapse">⤢</button>
        <button className="close-chat" onClick={toggleChat} title="Close">×</button>
    </div>
    </div>
  );
};

export default ChatHeader;
