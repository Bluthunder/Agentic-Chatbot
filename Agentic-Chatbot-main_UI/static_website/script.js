// Mobile Navigation Toggle
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
});

// Close mobile menu when clicking on a link
document.querySelectorAll('.nav-menu a').forEach(link => {
    link.addEventListener('click', () => {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
    });
});

// Navbar scroll effect
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 100) {
        navbar.style.background = 'rgba(255, 255, 255, 0.98)';
        navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
    } else {
        navbar.style.background = 'rgba(255, 255, 255, 0.95)';
        navbar.style.boxShadow = 'none';
    }
});

// Chatbot Variables
let ws = null;
let sessionId = null;
let isConnected = false;
let reconnectAttempts = 0;
const maxReconnectAttempts = 3;
let isExpanded = false;

// Chatbot Functions
function openChatbot() {
    const chatbot = document.getElementById('chatbot-container');
    const floatButton = document.querySelector('.chat-support-float');
    
    if (!chatbot || !floatButton) {
        console.error('Chatbot elements not found');
        return;
    }
    
    chatbot.style.display = 'flex';
    floatButton.style.display = 'none';
    
    // Initialize WebSocket connection
    initializeWebSocket();
    
    // Add welcome message if no messages exist
    const messagesContainer = document.getElementById('chat-messages');
    if (messagesContainer && messagesContainer.children.length === 0) {
        addMessage('bot', "Hello! I'm BARRY, your Skyline Airway assistant. How can I help you today?");
    }
    
    // Focus on input
    setTimeout(() => {
        const input = document.getElementById('chat-input');
        if (input) input.focus();
    }, 300);
}

function closeChatbot() {
    const chatbot = document.getElementById('chatbot-container');
    const floatButton = document.querySelector('.chat-support-float');
    
    if (!chatbot || !floatButton) {
        console.error('Chatbot elements not found');
        return;
    }
    
    chatbot.style.display = 'none';
    floatButton.style.display = 'flex';
    
    // Reset expansion state
    isExpanded = false;
    chatbot.classList.remove('expanded');
    updateExpandButton();
    
    // Close WebSocket connection
    if (ws) {
        ws.close();
        ws = null;
    }
    isConnected = false;
    reconnectAttempts = 0;
}

function toggleChatbotSize() {
    const chatbot = document.getElementById('chatbot-container');
    if (!chatbot) return;
    
    isExpanded = !isExpanded;
    
    if (isExpanded) {
        chatbot.classList.add('expanded');
    } else {
        chatbot.classList.remove('expanded');
    }
    
    updateExpandButton();
}

function updateExpandButton() {
    const expandBtn = document.querySelector('.chatbot-btn:not(.close-btn)');
    if (expandBtn) {
        const icon = expandBtn.querySelector('i');
        if (icon) {
            icon.className = isExpanded ? 'fas fa-compress' : 'fas fa-expand';
        }
        expandBtn.title = isExpanded ? 'Collapse' : 'Expand';
    }
}

function initializeWebSocket() {
    if (ws && ws.readyState === WebSocket.OPEN) {
        console.log('WebSocket already connected');
        return;
    }
    
    if (reconnectAttempts >= maxReconnectAttempts) {
        console.error('Max reconnection attempts reached');
        addSystemMessage('Connection failed. Please try again later.');
        return;
    }
    
    const wsUrl = sessionId ? 
        `ws://localhost:8000/api/v1/chat?session_id=${sessionId}` : 
        'ws://localhost:8000/api/v1/chat';
    
    console.log('Connecting to WebSocket:', wsUrl);
    
    try {
        ws = new WebSocket(wsUrl);
        
        ws.onopen = function() {
            console.log('WebSocket connected successfully');
            isConnected = true;
            reconnectAttempts = 0;
            updateConnectionStatus(true);
            hideTypingIndicator();
        };
        
        ws.onclose = function(event) {
            console.log('WebSocket disconnected:', event.code, event.reason);
            isConnected = false;
            updateConnectionStatus(false);
            
            // Attempt to reconnect if not a normal closure
            if (event.code !== 1000 && reconnectAttempts < maxReconnectAttempts) {
                reconnectAttempts++;
                console.log(`Reconnection attempt ${reconnectAttempts}/${maxReconnectAttempts}`);
                setTimeout(() => {
                    initializeWebSocket();
                }, 2000 * reconnectAttempts); // Exponential backoff
            }
        };
        
        ws.onerror = function(error) {
            console.error('WebSocket error:', error);
            isConnected = false;
            updateConnectionStatus(false);
        };
        
        ws.onmessage = function(event) {
            try {
                const data = JSON.parse(event.data);
                handleWebSocketMessage(data);
            } catch (e) {
                console.error('Error parsing WebSocket message:', e);
                addSystemMessage('Error processing response. Please try again.');
            }
        };
        
    } catch (error) {
        console.error('Error creating WebSocket:', error);
        addSystemMessage('Failed to connect to chat service.');
    }
}

function handleWebSocketMessage(data) {
    console.log('Received WebSocket message:', data);
    
    if (data.type === 'session_ready' && data.session_id) {
        sessionId = data.session_id;
        localStorage.setItem('skyline_session_id', sessionId);
        console.log('Session ready:', sessionId);
        return;
    }
    
    // Hide typing indicator
    hideTypingIndicator();
    
    // Handle bot response
    if (data.response) {
        addMessage('bot', data.response, {
            intent: data.intent,
            topic: data.topic,
            sentiment: data.sentiment,
            routed_to: data.routed_to
        });
    }
}

function sendMessage() {
    const input = document.getElementById('chat-input');
    if (!input) {
        console.error('Chat input not found');
        return;
    }
    
    const message = input.value.trim();
    
    if (!message) {
        return;
    }
    
    if (!isConnected) {
        addSystemMessage('Connecting to chat service...');
        initializeWebSocket();
        return;
    }
    
    // Add user message to chat
    addMessage('user', message);
    
    // Show typing indicator
    showTypingIndicator();
    
    // Send message via WebSocket
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(message);
    } else {
        console.error('WebSocket not connected');
        addSystemMessage('Connection lost. Attempting to reconnect...');
        initializeWebSocket();
    }
    
    // Clear input
    input.value = '';
}

function addMessage(sender, text, meta = null) {
    const messagesContainer = document.getElementById('chat-messages');
    if (!messagesContainer) {
        console.error('Chat messages container not found');
        return;
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    
    // Create avatar content based on sender
    if (sender === 'bot') {
        avatar.innerHTML = '<span>B</span>';
    } else {
        avatar.innerHTML = '<span>U</span>';
    }
    
    const content = document.createElement('div');
    content.className = 'message-content';
    
    const textP = document.createElement('p');
    textP.textContent = text;
    content.appendChild(textP);
    
    // Note: Removed metadata display for user experience
    // Meta information (intent, topic, agent) is still logged to console for debugging
    if (sender === 'bot' && meta) {
        console.log('Bot message metadata:', meta);
    }
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    messagesContainer.appendChild(messageDiv);
    
    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function addSystemMessage(text) {
    const messagesContainer = document.getElementById('chat-messages');
    if (!messagesContainer) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message system-message';
    messageDiv.style.textAlign = 'center';
    messageDiv.style.margin = '10px 0';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    content.style.background = '#f3f4f6';
    content.style.color = '#6b7280';
    content.style.fontSize = '0.9rem';
    content.style.padding = '8px 12px';
    content.style.borderRadius = '15px';
    content.style.display = 'inline-block';
    content.style.maxWidth = '80%';
    
    content.textContent = text;
    messageDiv.appendChild(content);
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function updateConnectionStatus(connected) {
    const input = document.getElementById('chat-input');
    const sendBtn = document.getElementById('chat-send');
    
    if (!input || !sendBtn) {
        console.error('Chat input or send button not found');
        return;
    }
    
    if (connected) {
        input.placeholder = 'Type your message...';
        input.disabled = false;
        sendBtn.disabled = false;
        sendBtn.style.opacity = '1';
    } else {
        input.placeholder = 'Connecting...';
        input.disabled = true;
        sendBtn.disabled = true;
        sendBtn.style.opacity = '0.5';
    }
}

function showTypingIndicator() {
    const messagesContainer = document.getElementById('chat-messages');
    if (!messagesContainer) return;
    
    // Remove existing typing indicator
    hideTypingIndicator();
    
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message typing-indicator';
    typingDiv.id = 'typing-indicator';
    
    typingDiv.innerHTML = `
        <div class="message-avatar">
            <span>B</span>
        </div>
        <div class="message-content">
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;
    
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Load session ID from localStorage
    const storedSessionId = localStorage.getItem('skyline_session_id');
    if (storedSessionId) {
        sessionId = storedSessionId;
    }
    
    // Initialize connection status
    updateConnectionStatus(false);
    
    // Add event listeners
    const chatInput = document.getElementById('chat-input');
    const chatSend = document.getElementById('chat-send');
    
    if (chatInput) {
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }
    
    if (chatSend) {
        chatSend.addEventListener('click', sendMessage);
    }
});

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe elements for animation
document.querySelectorAll('.destination-card, .service-card, .stat').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// Form submission handling
document.querySelector('.contact-form form')?.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const name = this.querySelector('input[type="text"]').value;
    const email = this.querySelector('input[type="email"]').value;
    const message = this.querySelector('textarea').value;
    
    if (!name || !email || !message) {
        alert('Please fill in all fields');
        return;
    }
    
    alert('Thank you for your message! We will get back to you soon.');
    this.reset();
});

// Add loading animation for buttons
document.querySelectorAll('.btn-primary, .btn-secondary').forEach(button => {
    button.addEventListener('click', function() {
        if (this.textContent.includes('Book Flight') || this.textContent.includes('View Destinations')) {
            const originalText = this.textContent;
            this.textContent = 'Loading...';
            this.disabled = true;
            
            setTimeout(() => {
                this.textContent = originalText;
                this.disabled = false;
                alert('This feature is coming soon!');
            }, 1000);
        }
    });
});

// Add hover effects for destination cards
document.querySelectorAll('.destination-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-10px) scale(1.02)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) scale(1)';
    });
});

// Add CSS for typing indicator and system messages
const additionalCSS = `
    .typing-dots {
        display: flex;
        gap: 4px;
        align-items: center;
    }
    
    .typing-dots span {
        width: 8px;
        height: 8px;
        background: #1e40af;
        border-radius: 50%;
        animation: typing 1.4s infinite ease-in-out;
    }
    
    .typing-dots span:nth-child(1) { animation-delay: -0.32s; }
    .typing-dots span:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes typing {
        0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
        40% { transform: scale(1); opacity: 1; }
    }
    
    .system-message .message-content {
        background: #f3f4f6 !important;
        color: #6b7280 !important;
        border: none !important;
    }
    
    .chat-input-container input:disabled {
        background: #f9fafb;
        cursor: not-allowed;
    }
    
    #chat-send:disabled {
        background: #9ca3af !important;
        cursor: not-allowed;
    }
    
    .chatbot-btn {
        transition: all 0.3s ease;
    }
    
    .chatbot-btn:hover {
        transform: scale(1.1);
    }
    
    .chatbot-btn.close-btn:hover {
        background: #ef4444 !important;
    }
`;

// Inject additional CSS
const style = document.createElement('style');
style.textContent = additionalCSS;
document.head.appendChild(style); 