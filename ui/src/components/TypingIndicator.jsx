import React from 'react';

const TypingIndicator = ({ isTyping }) => {
  if (!isTyping) return null;

  return (
    <div className="typing-indicator" id="typingIndicator">
      <div className="typing-dots">
        <div className="typing-dot"></div>
        <div className="typing-dot"></div>
        <div className="typing-dot"></div>
      </div>
      <span>Barry is processing</span>
    </div>
  );
};

export default TypingIndicator;
