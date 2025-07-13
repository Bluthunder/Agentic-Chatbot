import React, { useEffect, useRef, useState } from 'react';
import './Chat.css';
import axios from 'axios';

interface Message {
  sender: 'user' | 'bot';
  text: string;
  meta?: {
    intent?: string;
    topic?: string;
    sentiment?: string;
    routed_to?: string;
  };
}

const WS_URL = 'ws://localhost:8000/api/v1/chat'; // Updated to match backend route

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [connected, setConnected] = useState(false);
  const [maximized, setMaximized] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [wsReady, setWsReady] = useState(false); // new state to control ws opening
  const ws = useRef<WebSocket | null>(null);
  const bottomRef = useRef<HTMLDivElement | null>(null);

  // New Chat handler
  const startNewChat = () => {
    localStorage.removeItem('lastSessionId');
    setSessionId(null);
    setMessages([]);
    window.location.reload(); // reload to re-initiate ws with new session
  };

  // On mount, if lastSessionId exists, fetch and display its history, then open ws
  useEffect(() => {
    const storedSessionId = localStorage.getItem('lastSessionId');
    if (storedSessionId) {
      setSessionId(storedSessionId);
      axios.get(`/api/v1/session/${storedSessionId}`)
        .then(res => {
          if (res.data && res.data.messages) {
            const loadedMsgs: Message[] = [];
            res.data.messages.forEach((msg: any) => {
              if (msg.user) {
                loadedMsgs.push({ sender: 'user', text: msg.user });
              }
              if (msg.agent) {
                loadedMsgs.push({
                  sender: 'bot',
                  text: msg.agent,
                  meta: msg.intent ? {
                    intent: msg.intent,
                    topic: msg.topic,
                    sentiment: msg.sentiment,
                    routed_to: msg.agent_name,
                  } : undefined,
                });
              }
            });
            console.log('LoadedMsgs for chat:', loadedMsgs); // DEBUG LOG
            setMessages(loadedMsgs);
          }
          setWsReady(true);
        })
        .catch(() => {
          setMessages([]);
          setWsReady(true);
        });
    } else {
      setWsReady(true);
    }
  }, []);

  // WebSocket connection (depends on sessionId and wsReady)
  useEffect(() => {
    if (!wsReady) return;
    const wsUrl = sessionId ? `${WS_URL}?session_id=${sessionId}` : WS_URL;
    ws.current = new window.WebSocket(wsUrl);
    ws.current.onopen = () => setConnected(true);
    ws.current.onclose = () => setConnected(false);
    ws.current.onerror = () => setConnected(false);
    ws.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        // On session_ready, store sessionId if not already set
        if (data.type === 'session_ready' && data.session_id && !sessionId) {
          localStorage.setItem('lastSessionId', data.session_id);
          setSessionId(data.session_id);
        }
        // Always add the new bot message (ignore session_ready)
        if (!data.type || data.type !== 'session_ready') {
          setMessages((msgs) => [
            ...msgs,
            {
              sender: 'bot',
              text: data.response,
              meta: {
                intent: data.intent,
                topic: data.topic,
                sentiment: data.sentiment,
                routed_to: data.routed_to,
              },
            },
          ]);
        }
      } catch (e) {
        // ignore
      }
    };
    return () => {
      ws.current?.close();
    };
  }, [sessionId, wsReady]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || !connected) return;
    ws.current?.send(input);
    setMessages((msgs) => [
      ...msgs,
      { sender: 'user', text: input },
    ]);
    setInput('');
  };

  return (
    <div className={`chat-container${maximized ? ' maximized' : ''}`}>
      <header className="chat-header">
        Customer Support Chatbot
        <button
          className="chat-maximize-btn"
          title={maximized ? 'Restore' : 'Maximize'}
          onClick={() => setMaximized((m) => !m)}
          style={{ position: 'absolute', right: 48, top: 14, background: 'none', border: 'none', cursor: 'pointer', fontSize: '1.3rem', color: '#fff' }}
        >
          {maximized ? '🗗' : '🗖'}
        </button>
        <button
          className="chat-new-btn"
          title="Start New Chat"
          onClick={startNewChat}
          style={{ position: 'absolute', right: 18, top: 14, background: 'none', border: 'none', cursor: 'pointer', fontSize: '1.1rem', color: '#fff', padding: 0 }}
        >
          &#x2716;
        </button>
      </header>
      <div className="chat-messages">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`chat-message ${msg.sender}`}
          >
            <div className="chat-bubble">
              {/* Format bot and user messages for better readability */}
              {msg.text.split('\n').map((line, i) => (
                <p key={i} style={{ margin: 0 }}>{line}</p>
              ))}
              {/* Remove intent, topic, sentiment, agent display */}
            </div>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>
      <form className="chat-input-row" onSubmit={sendMessage}>
        <input
          className="chat-input"
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={connected ? 'Type your message...' : 'Connecting...'}
          disabled={!connected}
        />
        <button className="chat-send" type="submit" disabled={!connected || !input.trim()}>
          Send
        </button>
      </form>
      {!connected && <div className="chat-status">Connecting to server...</div>}
    </div>
  );
};

export default Chat; 