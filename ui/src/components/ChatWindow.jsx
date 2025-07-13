import React from 'react';
import '../App.css'; // reuse styles

function ChatWindow({ messages }) {
  return (
    <div className="chat-window">
      {messages.map((msg, idx) => (
        <div key={idx} className={`chat-message ${msg.sender}`}>
          {msg.text}
        </div>
      ))}
    </div>
  );
}

export default ChatWindow;
