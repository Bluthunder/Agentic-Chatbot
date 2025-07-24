import React, { useEffect, useRef, useState } from 'react';
import ChatHeader from './ChatHeader';
import ChatMessages from './ChatMessages';
import TypingIndicator from './TypingIndicator';
import ChatInput from './ChatInput';
import './ChatWidget.css';
import barryImg from '../assets/BarryPilot.png';

 const ChatWidget = ({toggleChat, toggleExpand, isExpanded}) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  // const [socket, setSocket] = useState(null);
  const socketRef = useRef(null)



  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  // Scroll to bottom on new message
  const scrollToBottom = () => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };

   useEffect(scrollToBottom, [messages]);

  // Connect WebSocket on mount
  useEffect(() => {
    // let ws;
    const connectWebSocket = () => {
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const wsUrl = `ws://localhost:8000/chat`;
      // ws = new WebSocket(wsUrl);
      // setSocket(ws);

      const ws = new WebSocket(wsUrl)
      socketRef.current = ws

      ws.onopen = () => {
        console.log('WebSocket connected');
        setIsConnected(true);
      };

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleBotMessage(data);
      };

      ws.onclose = () => {
        console.log('WebSocket disconnected. Reconnecting...');
        setIsConnected(false);
        setTimeout(connectWebSocket, 3000);
      };

      ws.onerror = (err) => {
        console.error('WebSocket error:', err);
        setIsConnected(false);
        ws.close();
      };
    };

    connectWebSocket();
  }, []);


  const handleSend = () => {
    const user_msg = input.trim();
    if (!user_msg || !socketRef.current || socketRef.current.readyState !== WebSocket.OPEN) return;

    // Add user message
    setMessages((prev) => [
      ...prev,
      { sender: 'user', text: user_msg }
    ]);

    setInput('');
    setIsTyping(true);

    // socket.send(JSON.stringify({ message: trimmed }));
    socketRef.current.send(JSON.stringify({query: user_msg}))
  };

  console.log("Sending via socket", socketRef.current);

  const handleBotMessage = (data) => {
    setIsTyping(false);

    const response = data.response || data.message || "Sorry, I couldn't process your request.";
    const metadata = {
      intent: data.intent || 'unknown',
      topic: data.topic || 'unknown',
      agent: data.agent_name || 'Unknown Agent'
    };

    setMessages((prev) => [
      ...prev,
      { sender: 'bot', text: response }
    ]);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }

    // Auto-resize textarea
    const textarea = e.target;
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
  };

  const renderMessageText = (text) => {
  const lines = text.split('\n');

  // Detect if it's a numbered list
  const isNumberedList = lines.every(line => /^\d+\.\s+/.test(line.trim()));

  if (isNumberedList) {
    return (
      <ul>
        {lines.map((line, idx) => {
          const content = line.replace(/^\d+\.\s+/, ''); // remove "1. "
          const number = line.match(/^(\d+)\./)?.[1]; // extract "1"
          return (
            <li key={idx}>
              <strong>{number}.</strong> {content}
            </li>
          );
        })}
      </ul>
    );
  }

  // Default: just render each line as a <p>
  return lines.map((line, idx) => <p key={idx}>{line}</p>);
};
  

  // Dragging logic
  const handleMouseDown = (e) => {
    const widget = widgetRef.current;
    pos.current = {
      x: e.clientX - widget.getBoundingClientRect().left,
      y: e.clientY - widget.getBoundingClientRect().top,
    };
    document.addEventListener('mousemove', handleDrag);
    document.addEventListener('mouseup', () => {
      document.removeEventListener('mousemove', handleDrag);
    });
  };

  const handleDrag = (e) => {
    const widget = widgetRef.current;
    widget.style.left = `${e.clientX - pos.current.x}px`;
    widget.style.top = `${e.clientY - pos.current.y}px`;
  };

  return (
    <div className={`chat-widget-popup ${isExpanded ? 'expanded' : ''}`}>
    <div className="chat-container" id="chatContainer">
      <div className="chat-header">
        <div style={{display: 'flex', justifyContent: 'space-between'}}>
            <div className="status-indicator">
              <div className={`status-dot ${isConnected ? 'connected' : ''}`}></div>
              <span>{isConnected ? 'Online' : 'Connecting...'}</span>
            </div>
              <div className="chat-header-buttons">
              <button className="chat-header-btn" onClick={toggleExpand} title="Expand/Collapse">⤢</button>
              <button className="close-chat" onClick={toggleChat} title="Close">×</button>
            </div>
        </div>
        
        <h1 style ={{display:'flex', justifyContent:'center'}}><img src={barryImg} style={{ width: '35px', height: '35px', marginTop: '4px' }} />Barry</h1>
        <p>AI Powered Travel Assistant</p>
      </div>

      <div className="chat-messages" id="chatMessages">
        {messages.length === 0 && (
          <div className="welcome-message">
            <h3>Hello! I'm Barry ✈️</h3>
            <p style={{color:'black'}}>Ask me about bookings, schedules, or travel recommendations!</p>
          </div>
        )}
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.sender}`}>
            <div className="message-avatar">{msg.sender === 'user' ? '🧑' : '👨‍✈️'}</div>
            <div className="message-content">
              {
                renderMessageText(msg.text)
              /* {msg.text.split('\n').map((line, i) => (
                <div key={i}>{line}</div>
              ))} */
              
              }

              {msg.metadata && (
                <div className="message-meta">
                  {Object.entries(msg.metadata).map(([k, v]) => (
                    <span key={k} className="meta-item">{k}: {v}</span>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        {isTyping && (
          <div className="typing-indicator">
            <div className="typing-dots">
              <div className="typing-dot"></div>
              <div className="typing-dot"></div>
              <div className="typing-dot"></div>
            </div>
            <span>Barry is processing...</span>
          </div>
        )}
        <div ref={messagesEndRef}></div>
      </div>

      <div className="chat-input-container" id="chatContainer">
        <div className="chat-input-wrapper">
          <textarea
            ref={textareaRef}
            className="chat-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={!isConnected}
            placeholder={isConnected ? "Type your message here..." : "Connecting to server..."}
            rows={1}
          />
          <button
            className="send-button"
            onClick={handleSend}
            disabled={!isConnected || !input.trim()}
          >
            ➤
          </button>
        </div>
      </div>
    </div>
    </div>
  );
};

export default ChatWidget;
