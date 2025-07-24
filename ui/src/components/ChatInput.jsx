import React, { useRef, useEffect } from 'react';

const ChatInput = ({ input, setInput, onSend, isConnected }) => {
  const textareaRef = useRef(null);

  // Auto-resize textarea height
  useEffect(() => {
    if (textareaRef.current) {
      //textareaRef.current.style.height = 'auto';
      //textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 120) + 'px';
    }
  }, [input]);

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      onSend();
    }
  };

  return (
    <div className="chat-input-container">
      <div className="chat-input-wrapper">
        <textarea
          ref={textareaRef}
          className="chat-input"
          placeholder={'Type your message here...'}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={!isConnected}
          rows={1}
        ></textarea>
        <button
          className="send-button"
          onClick={onSend}
          disabled={!input.trim() || !isConnected}
        >
          ➤
        </button>
      </div>
    </div>
  );
};

export default ChatInput;
