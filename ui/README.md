# 💬 My ChatGPT Clone (React)

A simple ChatGPT-style UI built with **React 19** and **Vite**.  
This project uses a dark-themed chat window centered on a white page, styled using plain CSS.

---

## 🚀 Features

- React 19 with functional components
- Vite for fast development and build
- Modular components: `ChatWindow`, `ChatInputArea`
- Simple CSS styling
- Clean and minimal ChatGPT-like UI

---

## 🛠 Prerequisites

Make sure you have the following installed:

- **Node.js** (v18 or later recommended)  
  👉 [Download Node.js here](https://nodejs.org)

---

## 📦 Getting Started

Follow these steps to set up and run the project:

### 1. **Clone the repository**

```bash
git clone https://github.com/Obi-Wan-Cloud/Agentic-Chatbot.git
cd Agentic-Chatbot/ui
```

### 2. Install dependencies
```bash
npm install
```

### 3. Run the development server
```bash
npm run dev
```

### 4. Then open your browser and go to:
http://localhost:5173


📁 Project Structure

my-react-app/
├── public/                # Static assets
├── src/
│   ├── components/        # Reusable components
│   │   ├── ChatWindow.jsx
│   │   └── ChatInputArea.jsx
│   ├── App.jsx            # Main App component
│   ├── App.css            # Styling
│   └── main.jsx           # React entry point
├── package.json
└── vite.config.js

### Available Commands
Command	                 Description
npm run dev	             Start development server
npm run build	         Build for production
npm run preview	         Preview production build locally
npm run lint	         Run ESLint on source files
