import React from 'react';
import '../App.css'; // reuse styles

function ChatInputArea({ input, onChange, onSend }) {
  return (
    <div className="chat-input-area">
      <input
        type="text"
        placeholder="Type your message..."
        value={input}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && onSend()}
      />
      <button onClick={onSend}>Send</button>
    </div>
  );
}

export default ChatInputArea;
