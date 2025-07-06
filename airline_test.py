#!/usr/bin/env python3
"""
Comprehensive test for airline industry intent classification
Tests all 26 categories with realistic airline customer service scenarios
"""

import requests
import sqlite3
import time

# Configuration
BASE_URL = "http://localhost:5000"
DB_PATH = "chat.db"

def test_airline_intents():
    """Test all airline industry intent categories"""
    
    test_cases = [
        # Core booking and cancellation
        ("I want to book a flight to New York", "Booking"),
        ("Please help me reserve a seat", "Booking"),
        ("Cancel my flight booking", "Cancellation"),
        ("I need to cancel my reservation", "Cancellation"),
        
        # Inquiries and complaints
        ("What time does my flight depart?", "Inquiry"),
        ("I have a question about baggage", "Inquiry"),
        ("I'm very unhappy with the service", "Complaint"),
        ("There's a problem with my booking", "Complaint"),
        
        # Feedback and support
        ("I want to leave feedback about my experience", "Feedback"),
        ("Here's my review of the flight", "Feedback"),
        ("I need help with my booking", "Support"),
        ("Can you assist me please?", "Support"),
        
        # Refunds and changes
        ("I want my money back", "Refund"),
        ("Request a refund for my ticket", "Refund"),
        ("I need to change my flight date", "Change"),
        ("Can I modify my booking?", "Change"),
        
        # Upgrades and rescheduling
        ("I want to upgrade to business class", "Upgrade"),
        ("Can I get a premium seat?", "Upgrade"),
        ("I need to reschedule my flight", "Reschedule"),
        ("Change my flight to a different time", "Reschedule"),
        
        # Check-in and boarding
        ("How do I check in online?", "Check-in"),
        ("I need help with check-in", "Check-in"),
        ("What gate is my flight boarding from?", "Boarding"),
        ("When does boarding start?", "Boarding"),
        
        # Seating and amenities
        ("I want a window seat", "Seating"),
        ("Can I select my seat?", "Seating"),
        ("What amenities are available on the flight?", "Amenities"),
        ("Do you have Wi-Fi on board?", "Amenities"),
        
        # Meals and information
        ("What meal options do you have?", "Meals"),
        ("I have dietary restrictions", "Meals"),
        ("Tell me about your flight schedules", "Information"),
        ("I need information about baggage allowance", "Information"),
        
        # Loyalty and rewards
        ("How do I join your frequent flyer program?", "Loyalty Programs"),
        ("What are the benefits of membership?", "Loyalty Programs"),
        ("How can I redeem my miles?", "Rewards"),
        ("What rewards can I earn?", "Rewards"),
        
        # Promotions and offers
        ("Do you have any special deals?", "Promotions"),
        ("Are there any current promotions?", "Promotions"),
        ("What offers are available?", "Offers"),
        ("Show me your latest deals", "Offers"),
        
        # Discounts and policies
        ("Can I get a discount on my ticket?", "Discounts"),
        ("Do you offer student discounts?", "Discounts"),
        ("What is your cancellation policy?", "Policies"),
        ("Tell me about your refund policy", "Policies"),
        
        # Procedures and regulations
        ("How do I change my booking?", "Procedures"),
        ("What's the process for upgrades?", "Procedures"),
        ("What are the travel requirements?", "Regulations"),
        ("Do I need a visa for this destination?", "Regulations"),
        
        # Security and safety
        ("What items are prohibited in carry-on?", "Security"),
        ("Tell me about security procedures", "Security"),
        ("Is it safe to fly during the pandemic?", "Safety"),
        ("What safety measures do you have?", "Safety"),
    ]
    
    print("🛫 Testing Airline Industry Intent Classification")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    for message, expected_intent in test_cases:
        print(f"\nTesting: '{message}' -> Expected: {expected_intent}")
        
        # Create a fresh session for each test
        session = requests.Session()
        
        # First, get the initial page to establish session
        initial_response = session.get(BASE_URL)
        session_id = session.cookies.get('session_id')
        
        # Send message (this will redirect)
        response = session.post(BASE_URL, data={'message': message}, allow_redirects=True)
        
        # Check if session ID changed
        final_session_id = session.cookies.get('session_id')
        
        if response.status_code == 200 and final_session_id:
            # Give database a moment to process
            time.sleep(0.1)
            
            # Check database for latest bot message
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            
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
                if actual_intent == expected_intent:
                    status = "✅ PASS"
                    passed += 1
                else:
                    status = "❌ FAIL"
                    failed += 1
                
                print(f"{status} Got: {actual_intent} (Confidence: {confidence})")
                print(f"   Bot Response: {bot_response[:80]}...")
            else:
                print("❌ FAIL No bot response found")
                failed += 1
        else:
            print(f"❌ FAIL HTTP {response.status_code}")
            failed += 1
    
    print("\n" + "="*50)
    print("🛫 AIRLINE INTENT TEST SUMMARY")
    print("="*50)
    print(f"Total Tests: {passed + failed}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {(passed/(passed+failed)*100):.1f}%")
    
    return passed == (passed + failed)

if __name__ == "__main__":
    # Wait for server
    print("⏳ Waiting for server...")
    time.sleep(2)
    
    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code == 200:
            print("✅ Server is ready!")
            success = test_airline_intents()
            if success:
                print("\n🎉 All airline intent tests passed!")
            else:
                print("\n⚠️ Some tests failed. Check output above.")
        else:
            print("❌ Server not responding")
    except Exception as e:
        print(f"❌ Error: {e}") 