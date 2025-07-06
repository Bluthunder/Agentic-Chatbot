#!/usr/bin/env python3
"""
Simple test to verify intent classification is working
"""

import requests
import sqlite3
import time

# Configuration
BASE_URL = "http://localhost:5000"
DB_PATH = "chat.db"

def test_intent_classification():
    """Test intent classification with direct messages"""
    
    test_cases = [
        ("Hello", "greeting"),
        ("I need help", "support"),
        ("I want a refund", "billing"),
        ("Goodbye", "farewell"),
    ]
    
    print("🧪 Testing Intent Classification")
    print("=" * 40)
    
    for message, expected_intent in test_cases:
        print(f"\nTesting: '{message}' -> Expected: {expected_intent}")
        
        # Create a fresh session for each test
        session = requests.Session()
        
        # First, get the initial page to establish session
        initial_response = session.get(BASE_URL)
        session_id = session.cookies.get('session_id')
        print(f"   Initial Session ID: {session_id}")
        
        # Send message (this will redirect)
        response = session.post(BASE_URL, data={'message': message}, allow_redirects=True)
        
        # Check if session ID changed
        final_session_id = session.cookies.get('session_id')
        print(f"   Final Session ID: {final_session_id}")
        
        if response.status_code == 200 and final_session_id:
            # Give database a moment to process
            time.sleep(0.1)
            
            # Check database for all messages in this session
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            
            # Debug: Check all messages for this session
            cur.execute("""
                SELECT role, content, intent, confidence 
                FROM messages 
                WHERE session_id = ? 
                ORDER BY timestamp ASC
            """, (final_session_id,))
            
            all_messages = cur.fetchall()
            print(f"   Total messages in session: {len(all_messages)}")
            
            for msg in all_messages:
                role, content, intent, confidence = msg
                print(f"   {role}: {content} (intent: {intent}, confidence: {confidence})")
            
            # Get latest bot message
            cur.execute("""
                SELECT intent, confidence, content 
                FROM messages 
                WHERE session_id = ? AND role = 'bot' 
                ORDER BY timestamp DESC 
                LIMIT 1
            """, (final_session_id,))
            
            result = cur.fetchone()
            conn.close()
            
            if result:
                actual_intent, confidence, bot_response = result
                status = "✅ PASS" if actual_intent == expected_intent else "❌ FAIL"
                print(f"{status} Got: {actual_intent} (Confidence: {confidence})")
                print(f"   Bot Response: {bot_response}")
            else:
                print("❌ FAIL No bot response found")
        else:
            print(f"❌ FAIL HTTP {response.status_code}")
            print(f"   Response: {response.text[:200]}...")

if __name__ == "__main__":
    # Wait for server
    print("⏳ Waiting for server...")
    time.sleep(2)
    
    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code == 200:
            print("✅ Server is ready!")
            test_intent_classification()
        else:
            print("❌ Server not responding")
    except Exception as e:
        print(f"❌ Error: {e}") 