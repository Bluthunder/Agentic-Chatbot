#!/usr/bin/env python3
"""
Setup script for Agentic Chatbot
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    print("🚀 Setting up Agentic Chatbot...")
    
    # Check if Python 3.8+ is available
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install Python dependencies
    if not run_command("pip3 install -r requirements.txt", "Installing Python dependencies"):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creating .env file from template...")
        try:
            with open("env.example", "r") as f:
                env_content = f.read()
            with open(".env", "w") as f:
                f.write(env_content)
            print("✅ .env file created")
        except FileNotFoundError:
            print("⚠️  env.example not found, creating basic .env file...")
            basic_env = """# LLM Configuration
LLM_BACKEND=mistral
MISTRAL_MODEL_PATH=models/mistral-7b-instruct-v0.2.Q4_K_M.gguf

# Database Configuration
POSTGRES_URI=postgresql://postgres@localhost/chatbot

# API Configuration
PORT=8000
HOST=0.0.0.0

# Development Configuration
DEBUG=true
LOG_LEVEL=INFO
"""
            with open(".env", "w") as f:
                f.write(basic_env)
            print("✅ Basic .env file created")
    
    # Check if model file exists
    model_path = Path("src/ai_agent/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf")
    if not model_path.exists():
        print("⚠️  Warning: Mistral model file not found at expected location")
        print("   You may need to download it or update MISTRAL_MODEL_PATH in .env")
    
    # Install frontend dependencies
    frontend_dir = Path("frontend")
    if frontend_dir.exists():
        print("📦 Installing frontend dependencies...")
        os.chdir(frontend_dir)
        if run_command("npm install", "Installing frontend dependencies"):
            os.chdir("..")
            print("✅ Frontend dependencies installed")
        else:
            os.chdir("..")
            print("⚠️  Frontend dependency installation failed")
    
    print("\n🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("1. Copy env.example to .env and configure your settings")
    print("2. Ensure you have the Mistral model file in the correct location")
    print("3. Run 'make run-dev' to start the development server")
    print("4. Run 'cd frontend && npm start' to start the frontend")

if __name__ == "__main__":
    main() 