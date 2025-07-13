# Agentic Chatbot - Airline Support AI

An intelligent airline support chatbot with agent-based routing using LangGraph and Mistral LLM.

## 🚀 Features

- **Multi-Agent Architecture**: Router, Booking, Flight Status, and Baggage agents
- **Real-time Chat**: WebSocket-based chat interface
- **Intelligent Routing**: Automatic intent classification and agent routing
- **State Management**: Conversation state tracking with SQLite/PostgreSQL
- **Modern UI**: React frontend with Tailwind CSS
- **Local LLM**: Mistral-7B running locally with llama.cpp

## 🖥️ Frontend UI

The frontend is a modern React (TypeScript) application that provides a user-friendly chat interface for interacting with the agentic backend.

### Features
- **Resizable, Expandable Chat Window:** The chat window can be resized and maximized for a better user experience.
- **Session Persistence:** Chat history is preserved across browser refreshes for the current session using localStorage.
- **Explicit Session Reset:** A "New Chat" button allows users to start a fresh session, clearing previous history.
- **Real-Time Messaging:** Uses WebSocket for instant communication with the backend.
- **Conversation History:** On refresh, the UI fetches and displays the full conversation for the current session.
- **Intent and Agent Display:** Shows detected intent, topic, sentiment, and agent for each bot response.

### How It Works
- On first load, a session ID is created and stored in localStorage.
- All messages for that session are saved and loaded after refresh.
- If the user clicks "New Chat", the session ID is cleared and a new session starts (old history is not shown).
- The chat UI always shows only the current session's history.

### How to Use/Modify
- The main UI code is in `frontend/src/Chat.tsx` and `frontend/src/Chat.css`.
- To change the look and feel, edit the CSS or React component as needed.
- To add new features (e.g., avatars, timestamps), extend the `Message` interface and update the rendering logic.

### Running the Frontend
```bash
cd frontend
npm install
npm start
```
The app will be available at [http://localhost:3000](http://localhost:3000).

---

## 🖥️ Step-by-Step UI & Backend Setup Guide

### 1. Clone the Repository
```bash
git clone git@github.com:Obi-Wan-Cloud/Agentic-Chatbot.git
cd Agentic-Chatbot-main
```

### 2. Python Environment Setup
- **Recommended:** Use a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
- Copy the example env file and edit as needed:
```bash
cp env.example .env
# Edit .env to set LLM, database, and other config
```

### 5. Database Setup
#### **A. SQLite (Default, No Extra Setup Needed)**
- The backend will use `chat_sessions.db` in the project root by default.
- No further action required for local development.

#### **B. PostgreSQL (For Production or Large Sessions)**
- Install Postgres (e.g., `brew install postgresql` or use Docker)
- Create a database and user:
```bash
createdb chatbot
# Optionally: createuser -P postgres
```
- Update your `.env`:
```
POSTGRES_URI=postgresql://postgres@localhost/chatbot
```
- The backend will automatically migrate long sessions to Postgres.

### 6. Start the Backend
```bash
make run-dev
# or
python3 -m uvicorn app:app --reload --port 8000
```
- The API will be available at [http://localhost:8000](http://localhost:8000)
- WebSocket endpoint: `ws://localhost:8000/api/v1/chat`
- REST endpoint for session history: `/api/v1/session/{session_id}`

### 7. Frontend UI Setup
```bash
cd frontend
npm install
npm start
```
- The UI will be available at [http://localhost:3000](http://localhost:3000)

### 8. Using the Chat UI
- Open [http://localhost:3000](http://localhost:3000)
- Type your message and interact with the AI chatbot.
- **Session Persistence:** Your chat history is saved for the current session and will be restored after a refresh.
- **New Chat:** Click the "New Chat" (×) button to start a fresh session (old history will not be shown).
- **Resizable UI:** Drag the chat window to resize or maximize for a better experience.

### 9. Customizing the UI
- Edit `frontend/src/Chat.tsx` and `frontend/src/Chat.css` to change the look, feel, or features.
- To add avatars, timestamps, or other enhancements, extend the `Message` interface and update the rendering logic.

### 10. Troubleshooting
- **Database Issues:** Ensure you are always starting the backend from the project root so the correct `chat_sessions.db` is used.
- **Push Protection:** If you encounter GitHub push protection errors, ensure no secrets or private keys are present in your repo or commit history.
- **Session Not Loading:** Make sure the backend is running and the session ID in localStorage matches the one in the database.

---

## 🗄️ Database Setup: SQLite & PostgreSQL

### **A. SQLite (Recommended for Local Development)**

**SQLite is lightweight and requires no extra installation on most systems.**

1. **No installation needed** (Python comes with SQLite support).
2. The backend will automatically create and use `chat_sessions.db` in the project root.
3. No manual configuration is required for local development.
4. To inspect the database, you can use [DB Browser for SQLite](https://sqlitebrowser.org/):
   - Download and install DB Browser for SQLite.
   - Open `chat_sessions.db` to view or edit chat sessions.

**.env example for SQLite:**
```
# No changes needed for SQLite (default)
```

---

### **B. PostgreSQL (Recommended for Production or Large Sessions)**

**PostgreSQL is robust and suitable for production or handling large chat histories.**

#### **1. Install PostgreSQL**
- **macOS (Homebrew):**
  ```bash
  brew install postgresql
  brew services start postgresql
  ```
- **Ubuntu/Debian:**
  ```bash
  sudo apt update
  sudo apt install postgresql postgresql-contrib
  sudo service postgresql start
  ```
- **Windows:**
  - Download and install from [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)

#### **2. Create Database and User**
```bash
# Switch to the postgres user (Linux/macOS)
sudo -u postgres psql
# Or just: psql (if your user has access)

# In the psql prompt:
CREATE DATABASE chatbot;
CREATE USER chatbot_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE chatbot TO chatbot_user;
\q
```

#### **3. Update Your .env File**
```
POSTGRES_URI=postgresql://chatbot_user:yourpassword@localhost/chatbot
```

#### **4. Verify Connection**
- The backend will automatically create tables in Postgres on startup.
- You can use a tool like [pgAdmin](https://www.pgadmin.org/) or `psql` to inspect the database.

#### **5. Run the Backend**
```bash
make run-dev
# or
python3 -m uvicorn app:app --reload --port 8000
```

#### **6. How It Works**
- Short sessions are stored in SQLite by default.
- When a session grows large (over 20 messages or 10,000 characters), it is automatically migrated to PostgreSQL.

---

## 🏗️ Architecture

See [HighLevelDiagram.md](HighLevelDiagram.md) for detailed architecture overview.

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL (optional, for production)
- 8GB+ RAM (for local LLM)

## 🛠️ Quick Start

### 1. Setup

```bash
# Clone and setup
git clone <repository-url>
cd Agentic-Chatbot-main

# Run setup script
make setup
```

### 2. Configure Environment

Copy the environment template and configure:

```bash
cp env.example .env
# Edit .env with your settings
```

### 3. Download Model (if needed)

The setup will check for the Mistral model. If missing, download it:

```bash
# Download Mistral-7B-Instruct-v0.2 Q4_K_M
# Place in: src/ai_agent/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf
```

### 4. Run Development Server

```bash
# Backend
make run-dev

# Frontend (in another terminal)
cd frontend && npm start
```

## 🧪 Testing

```bash
# Run all tests
make test

# Run specific test
pytest test/test_router_agent.py
```

## 🐳 Docker

```bash
# Build and run with Docker
make docker-build
make docker-run
```

## 📁 Project Structure

```
Agentic-Chatbot-main/
├── api/                    # FastAPI endpoints
├── frontend/              # React frontend
├── src/ai_agent/          # AI agent system
│   ├── agents/            # Agent implementations
│   ├── tools/             # LLM and utility tools
│   ├── state/             # Conversation state
│   └── models/            # Data models
├── test/                  # Test suite
└── makefile               # Build commands
```

## 🔧 Configuration

Key environment variables in `.env`:

- `LLM_BACKEND`: LLM backend (mistral)
- `MISTRAL_MODEL_PATH`: Path to Mistral model file
- `POSTGRES_URI`: PostgreSQL connection string
- `PORT`: API server port

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details. 