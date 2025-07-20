# Skyline Airway - Static Website with BARRY Chatbot

A modern, responsive airline website featuring the BARRY AI assistant chatbot integrated with the existing Agentic Chatbot backend.

## 🌟 Features

### **Website Features**
- **Modern Design**: Professional airline-themed design with blue gradient
- **Responsive Layout**: Works perfectly on desktop, tablet, and mobile
- **Smooth Animations**: CSS animations and transitions for enhanced UX
- **Interactive Elements**: Hover effects, loading states, and smooth scrolling
- **Mobile Navigation**: Hamburger menu for mobile devices

### **Chatbot Integration**
- **BARRY Assistant**: AI-powered chatbot with airline expertise
- **Real-time Chat**: WebSocket connection to the existing backend
- **Session Persistence**: Chat history saved across browser sessions
- **Typing Indicators**: Visual feedback when BARRY is responding
- **Metadata Display**: Shows intent, topic, and agent routing information

## 🚀 Quick Start

### **Prerequisites**
- Backend server running (FastAPI on port 8000)
- BARRY icon image (`barry-icon.png`)

### **Setup Instructions**

1. **Add BARRY Icon**
   ```bash
   # Replace the placeholder with your actual BARRY icon
   # Copy your barry-icon.png to the static_website directory
   ```

2. **Start the Backend** (if not already running)
   ```bash
   cd "/Users/nsureka/Documents/gitrepo/public/IISc Capstone Project/Agentic-Chatbot-main_UI"
   source venv/bin/activate
   make run-dev
   ```

3. **Open the Website**
   ```bash
   # Open index.html in your browser
   # Or serve it using a local server:
   python -m http.server 8080
   # Then visit: http://localhost:8080
   ```

## 📁 File Structure

```
static_website/
├── index.html          # Main website HTML
├── styles.css          # Complete CSS styling
├── script.js           # JavaScript functionality
├── barry-icon.png      # BARRY chatbot icon (add your own)
└── README.md           # This file
```

## 🎨 Design Features

### **Color Scheme**
- **Primary Blue**: #1e40af (Deep Blue)
- **Secondary Blue**: #3b82f6 (Medium Blue)
- **Accent Blue**: #60a5fa (Light Blue)
- **Background**: #f8fafc (Light Gray)
- **Text**: #333 (Dark Gray)

### **Typography**
- **Font Family**: Segoe UI, Tahoma, Geneva, Verdana, sans-serif
- **Headings**: Bold weights with blue accent
- **Body Text**: Clean, readable styling

### **Animations**
- **Plane Animation**: Flying plane in hero section
- **Card Hover Effects**: Elevation and scaling
- **Fade-in Animations**: Elements appear on scroll
- **Smooth Transitions**: All interactive elements

## 🤖 Chatbot Features

### **BARRY Integration**
- **WebSocket Connection**: Real-time communication with backend
- **Session Management**: Persistent chat sessions
- **Message History**: Loads previous conversations
- **Typing Indicators**: Shows when BARRY is thinking
- **Metadata Display**: Intent, topic, and agent information

### **Chatbot UI**
- **Floating Button**: Always accessible chat support
- **Pop-up Interface**: Clean, modern chat window
- **Message Bubbles**: Distinct user and bot messages
- **Avatar System**: BARRY icon for bot messages
- **Responsive Design**: Full-screen on mobile

## 📱 Responsive Design

### **Desktop (1200px+)**
- Full navigation menu
- Side-by-side layouts
- Large chatbot window

### **Tablet (768px - 1199px)**
- Adjusted grid layouts
- Medium chatbot window
- Optimized spacing

### **Mobile (< 768px)**
- Hamburger navigation
- Single-column layouts
- Full-screen chatbot
- Touch-optimized buttons

## 🔧 Technical Implementation

### **Frontend Technologies**
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with Flexbox and Grid
- **JavaScript (ES6+)**: Interactive functionality
- **WebSocket API**: Real-time communication

### **Integration Points**
- **Backend API**: ws://localhost:8000/api/v1/chat
- **Session Storage**: localStorage for session persistence
- **Message Format**: JSON with metadata

### **Performance Features**
- **Lazy Loading**: Images and animations
- **Optimized CSS**: Efficient selectors and properties
- **Minimal JavaScript**: Lightweight functionality
- **Fast Loading**: Optimized assets and structure

## 🎯 User Experience

### **Navigation**
- **Smooth Scrolling**: Animated section transitions
- **Fixed Navigation**: Always accessible menu
- **Active States**: Visual feedback for current section
- **Mobile Menu**: Touch-friendly hamburger navigation

### **Content Sections**
- **Hero Section**: Eye-catching introduction with CTA buttons
- **Destinations**: Popular travel destinations with pricing
- **Services**: Key airline services and features
- **About**: Company information and statistics
- **Contact**: Contact form and information

### **Interactive Elements**
- **Hover Effects**: Cards and buttons respond to interaction
- **Loading States**: Visual feedback for actions
- **Form Validation**: Real-time input validation
- **Smooth Animations**: Professional transitions

## 🚀 Deployment

### **Local Development**
```bash
# Simple HTTP server
python -m http.server 8080

# Or use any static file server
npx serve static_website
```

### **Production Deployment**
- Upload files to any web hosting service
- Ensure backend is accessible at the correct URL
- Update WebSocket URL in `script.js` if needed

## 🔗 Backend Integration

The website integrates with the existing Agentic Chatbot backend:

- **WebSocket Endpoint**: `ws://localhost:8000/api/v1/chat`
- **Session Management**: Automatic session creation and persistence
- **Message Routing**: Intelligent agent routing via BARRY
- **Response Handling**: Real-time AI responses with metadata

## 🎨 Customization

### **Colors**
Edit the CSS variables in `styles.css`:
```css
:root {
    --primary-blue: #1e40af;
    --secondary-blue: #3b82f6;
    --accent-blue: #60a5fa;
}
```

### **Content**
- Update airline information in `index.html`
- Modify destinations and services
- Change contact information
- Update company statistics

### **Styling**
- Modify CSS classes for different themes
- Adjust animations and transitions
- Change typography and spacing
- Update responsive breakpoints

## 📞 Support

For technical support or customization requests:
- Check the backend logs for WebSocket issues
- Ensure the backend server is running
- Verify the BARRY icon is properly placed
- Test on different devices and browsers

## 🎉 Ready to Launch!

Your Skyline Airway website with BARRY chatbot is ready to provide an exceptional user experience. The combination of modern design, responsive layout, and intelligent AI assistance creates a professional airline website that stands out from the competition. 