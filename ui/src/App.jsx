import { useState } from 'react';
import './App.css';
import ChatWindow from './components/ChatWindow';
import ChatInputArea from './components/ChatInputArea';

function App() {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Hello! How can I help you today?' },
  ]);
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (!input.trim()) return;
    setMessages([...messages, { sender: 'user', text: input }]);
    setInput('');
  };

  return (
    <div className="app-wrapper">
      <div className="chat-container">
        <header className="chat-header">Hi, This is Barry</header>
        <ChatWindow messages={messages} />
        <ChatInputArea
          input={input}
          onChange={setInput}
          onSend={handleSend}
        />
      </div>
    </div>
  );
}

export default App;
