import React, { useState } from 'react';
import './App.css';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Features from './components/Features';
import Destinations from './components/Destinations';
import Services from './components/Services';
import Footer from './components/Footer';
import ChatWidget from './components/ChatWidget';

function App() {

  const [isChatOpen, setIsChatOpen] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);


// Chat functionality
/**function toggleChat() {
  console.log("toggleChat Clicked");
    const chatContainer = document.getElementById('chatContainer');
    const chatBackdrop = document.getElementById('chatBackdrop');
    const isVisible = chatContainer.style.display === 'flex';
    
    if (!isVisible) {
        chatContainer.style.display = 'flex';
        chatBackdrop.style.display = 'block';
        //connectWebSocket();
        setIsChatOpen(true)
    } else {
        chatContainer.style.display = 'none';
        chatBackdrop.style.display = 'none';
        // Reset to normal size when closing
        chatContainer.classList.remove('expanded');
        setIsChatOpen(false);
    }
}*/

const toggleChat = () => {
  console.log("toggle clicked ", isChatOpen)
  setIsChatOpen(prev => !prev);
}


 function toggleExpand() {
  setIsExpanded(prev => !prev);
}

  return (
    <>
      <div className="chat-backdrop" id="chatBackdrop" onClick={toggleChat}></div>
        <Navbar />
        <Hero />
        {/* <Features /> */}
        <button className="chat-button" onClick={toggleChat}>💬</button>
        <Destinations />
        <Services />
        <Footer/>
        { isChatOpen && <ChatWidget toggleChat={toggleChat} toggleExpand={toggleExpand} isExpanded={isExpanded}/>}

    </>
  );
}

export default App;
