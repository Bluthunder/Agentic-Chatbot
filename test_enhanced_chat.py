#!/usr/bin/env python3
"""
Comprehensive test script for Enhanced Flask Chat Application
Tests session handling, message persistence, and API endpoints
"""

import requests
import sqlite3
import json
import time
import uuid
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"
DB_PATH = "chat.db"

class ChatTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name, success, message=""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        self.test_results.append({
            'test': test_name,
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
    
    def test_database_creation(self):
        """Test if database and tables are created properly"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            
            # Check if tables exist
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cur.fetchall()]
            
            required_tables = ['messages', 'sessions']
            missing_tables = [table for table in required_tables if table not in tables]
            
            if missing_tables:
                self.log_test("Database Schema", False, f"Missing tables: {missing_tables}")
            else:
                self.log_test("Database Schema", True, "All required tables exist")
            
            # Check table structure
            cur.execute("PRAGMA table_info(messages)")
            message_columns = [row[1] for row in cur.fetchall()]
            
            required_columns = ['id', 'session_id', 'role', 'content', 'timestamp', 'intent', 'confidence']
            missing_columns = [col for col in required_columns if col not in message_columns]
            
            if missing_columns:
                self.log_test("Messages Table Structure", False, f"Missing columns: {missing_columns}")
            else:
                self.log_test("Messages Table Structure", True, "All columns present")
            
            conn.close()
            
        except Exception as e:
            self.log_test("Database Creation", False, str(e))
    
    def test_session_creation(self):
        """Test session creation and cookie handling"""
        try:
            # Make request without session cookie
            response = self.session.get(BASE_URL)
            
            if response.status_code == 200:
                self.log_test("Initial Page Load", True, "Page loads successfully")
                
                # Check if session cookie is set
                if 'session_id' in self.session.cookies:
                    session_id = self.session.cookies['session_id']
                    self.log_test("Session Cookie Creation", True, f"Session ID: {session_id[:8]}...")
                else:
                    self.log_test("Session Cookie Creation", False, "No session cookie set")
            else:
                self.log_test("Initial Page Load", False, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_test("Session Creation", False, str(e))
    
    def test_message_persistence(self):
        """Test message sending and persistence"""
        try:
            # Send a test message
            test_message = f"Test message {uuid.uuid4().hex[:8]}"
            
            response = self.session.post(BASE_URL, data={'message': test_message})
            
            if response.status_code == 200:
                self.log_test("Message Sending", True, "Message sent successfully")
                
                # Check if message appears in response
                if test_message in response.text:
                    self.log_test("Message Display", True, "Message appears in chat")
                else:
                    self.log_test("Message Display", False, "Message not found in response")
                
                # Check database persistence
                session_id = self.session.cookies.get('session_id')
                if session_id:
                    conn = sqlite3.connect(DB_PATH)
                    cur = conn.cursor()
                    cur.execute(
                        "SELECT content FROM messages WHERE session_id = ? AND content = ?",
                        (session_id, test_message)
                    )
                    result = cur.fetchone()
                    conn.close()
                    
                    if result:
                        self.log_test("Database Persistence", True, "Message stored in database")
                    else:
                        self.log_test("Database Persistence", False, "Message not found in database")
                
            else:
                self.log_test("Message Sending", False, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_test("Message Persistence", False, str(e))
    
    def test_intent_classification(self):
        """Test intent classification functionality"""
        test_cases = [
            ("Hello there!", "greeting"),
            ("I need help with my account", "support"),
            ("I want a refund", "billing"),
            ("Goodbye", "farewell"),
            ("Random message", "general")
        ]
        
        for message, expected_intent in test_cases:
            try:
                # Send message
                response = self.session.post(BASE_URL, data={'message': message})
                
                if response.status_code == 200:
                    # Check database for intent classification
                    session_id = self.session.cookies.get('session_id')
                    if session_id:
                        conn = sqlite3.connect(DB_PATH)
                        cur = conn.cursor()
                        
                        # Get the most recent bot message for this session
                        cur.execute(
                            "SELECT intent, confidence FROM messages WHERE session_id = ? AND role = 'bot' ORDER BY timestamp DESC LIMIT 1",
                            (session_id,)
                        )
                        result = cur.fetchone()
                        conn.close()
                        
                        if result and result[0] == expected_intent:
                            self.log_test(f"Intent Classification - {expected_intent}", True, f"Confidence: {result[1]}")
                        else:
                            actual_intent = result[0] if result else 'None'
                            self.log_test(f"Intent Classification - {expected_intent}", False, f"Expected: {expected_intent}, Got: {actual_intent}")
                
            except Exception as e:
                self.log_test(f"Intent Classification - {expected_intent}", False, str(e))
    
    def test_api_endpoints(self):
        """Test API endpoints"""
        try:
            # Test stats endpoint
            response = self.session.get(f"{BASE_URL}/api/stats")
            
            if response.status_code == 200:
                data = response.json()
                if 'total_sessions' in data and 'total_messages' in data:
                    self.log_test("Stats API", True, f"Sessions: {data['total_sessions']}, Messages: {data['total_messages']}")
                else:
                    self.log_test("Stats API", False, "Missing required fields in response")
            else:
                self.log_test("Stats API", False, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_test("API Endpoints", False, str(e))
    
    def test_session_isolation(self):
        """Test that sessions are properly isolated"""
        try:
            # Create a new session
            new_session = requests.Session()
            
            # Send message in first session
            message1 = f"Session 1 message {uuid.uuid4().hex[:8]}"
            self.session.post(BASE_URL, data={'message': message1})
            
            # Send message in second session  
            message2 = f"Session 2 message {uuid.uuid4().hex[:8]}"
            new_session.get(BASE_URL)  # Initialize new session
            new_session.post(BASE_URL, data={'message': message2})
            
            # Check that session 1 doesn't see session 2's message
            response1 = self.session.get(BASE_URL)
            response2 = new_session.get(BASE_URL)
            
            session1_has_message1 = message1 in response1.text
            session1_has_message2 = message2 in response1.text
            session2_has_message1 = message1 in response2.text
            session2_has_message2 = message2 in response2.text
            
            if session1_has_message1 and not session1_has_message2 and session2_has_message2 and not session2_has_message1:
                self.log_test("Session Isolation", True, "Sessions properly isolated")
            else:
                self.log_test("Session Isolation", False, f"S1 has M1: {session1_has_message1}, S1 has M2: {session1_has_message2}, S2 has M1: {session2_has_message1}, S2 has M2: {session2_has_message2}")
                
        except Exception as e:
            self.log_test("Session Isolation", False, str(e))
    
    def test_clear_session(self):
        """Test session clearing functionality"""
        try:
            # Send a message
            test_message = f"Clear test message {uuid.uuid4().hex[:8]}"
            self.session.post(BASE_URL, data={'message': test_message})
            
            # Verify message exists
            response = self.session.get(BASE_URL)
            if test_message in response.text:
                # Clear session
                clear_response = self.session.get(f"{BASE_URL}/api/clear_session")
                
                if clear_response.status_code == 200:
                    # Check if message is gone
                    response_after_clear = self.session.get(BASE_URL)
                    if test_message not in response_after_clear.text:
                        self.log_test("Clear Session", True, "Session cleared successfully")
                    else:
                        self.log_test("Clear Session", False, "Message still visible after clear")
                else:
                    self.log_test("Clear Session", False, f"Clear failed with status: {clear_response.status_code}")
            else:
                self.log_test("Clear Session", False, "Test message not found initially")
                
        except Exception as e:
            self.log_test("Clear Session", False, str(e))
    
    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting Enhanced Flask Chat Tests\n")
        
        # Wait for server to be ready
        print("⏳ Waiting for server to be ready...")
        for i in range(10):
            try:
                response = requests.get(BASE_URL, timeout=5)
                if response.status_code == 200:
                    print("✅ Server is ready!\n")
                    break
            except:
                time.sleep(1)
        else:
            print("❌ Server not responding. Make sure the Flask app is running on localhost:5000")
            return
        
        # Run tests
        self.test_database_creation()
        self.test_session_creation()
        self.test_message_persistence()
        self.test_intent_classification()
        self.test_api_endpoints()
        self.test_session_isolation()
        self.test_clear_session()
        
        # Summary
        print("\n" + "="*50)
        print("📊 TEST SUMMARY")
        print("="*50)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%")
        
        if failed_tests > 0:
            print("\n❌ Failed Tests:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test']}: {result['message']}")
        
        # Save results to file
        with open('test_results.json', 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"\n📄 Detailed results saved to test_results.json")
        
        return passed_tests == total_tests

def main():
    """Main test runner"""
    tester = ChatTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed! Your Flask chat app is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main()) 