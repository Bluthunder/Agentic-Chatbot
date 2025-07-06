from flask import Flask, request, redirect, render_template, make_response, jsonify
import sqlite3
import uuid
import logging
import os
from datetime import datetime
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chat_app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Database configuration
DB_PATH = "chat.db"

def get_conn():
    """Get database connection with error handling"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}")
        raise

def init_database():
    """Initialize database with proper schema"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        # Create messages table with better schema
        cur.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('user', 'bot')),
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                intent TEXT,
                confidence REAL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create sessions table for better session tracking
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_activity DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_agent TEXT,
                ip_address TEXT
            )
        """)
        
        # Create indexes for performance
        cur.execute("CREATE INDEX IF NOT EXISTS idx_messages_session_id ON messages(session_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp)")
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
        
    except sqlite3.Error as e:
        logger.error(f"Database initialization error: {e}")
        raise

# Initialize database on module import
init_database()

def get_session_id():
    """Get or create session ID with tracking"""
    session_id = request.cookies.get("session_id")
    
    if not session_id:
        session_id = str(uuid.uuid4())
        logger.info(f"New session created: {session_id}")
        
        # Track new session
        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO sessions (session_id, user_agent, ip_address) 
                VALUES (?, ?, ?)
            """, (session_id, request.headers.get('User-Agent', ''), request.remote_addr))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            logger.error(f"Error tracking new session: {e}")
    else:
        # Update last activity
        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("""
                UPDATE sessions 
                SET last_activity = CURRENT_TIMESTAMP 
                WHERE session_id = ?
            """, (session_id,))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            logger.error(f"Error updating session activity: {e}")
    
    return session_id

def simulate_bot_response(user_message, session_id):
    """Simulate bot response with comprehensive airline/travel industry intent detection"""
    user_message_lower = user_message.lower()
    
    # Comprehensive airline/travel industry intent classification with priority order
    # More specific intents first, then broader ones
    
    # Cancellation (high priority - specific action)
    if any(phrase in user_message_lower for phrase in ['cancel booking', 'cancel flight', 'cancel my', 'cancel reservation']) or \
       (any(word in user_message_lower for word in ['cancel', 'cancellation']) and 
        any(word in user_message_lower for word in ['booking', 'flight', 'reservation', 'ticket'])):
        intent = 'Cancellation'
        response = "I can assist you with canceling your booking. Please provide your booking reference number."
        confidence = 0.9
        
    # Refund (high priority - specific action)
    elif any(phrase in user_message_lower for phrase in ['money back', 'refund request', 'want refund', 'need refund']) or \
         any(word in user_message_lower for word in ['refund', 'reimbursement', 'compensation']):
        intent = 'Refund'
        response = "I can help you with refund requests. Please provide your booking details and reason for the refund."
        confidence = 0.9
        
    # Check-in (specific action)
    elif any(phrase in user_message_lower for phrase in ['check in', 'check-in', 'online check', 'boarding pass']):
        intent = 'Check-in'
        response = "I can help with check-in procedures. You can check in online up to 24 hours before your flight."
        confidence = 0.9
        
    # Upgrade (specific action)
    elif any(phrase in user_message_lower for phrase in ['business class', 'first class', 'premium seat']) or \
         any(word in user_message_lower for word in ['upgrade', 'premium']):
        intent = 'Upgrade'
        response = "I can assist with seat upgrades. Let me check available options for your flight."
        confidence = 0.9
        
    # Reschedule (specific action)
    elif any(phrase in user_message_lower for phrase in ['reschedule', 'change date', 'change time', 'different flight', 'different time']):
        intent = 'Reschedule'
        response = "I can help you reschedule your flight. What new date and time would you prefer?"
        confidence = 0.85
        
    # Seating (specific feature)
    elif any(phrase in user_message_lower for phrase in ['window seat', 'aisle seat', 'seat selection', 'select seat', 'choose seat']) or \
         (any(word in user_message_lower for word in ['seat', 'seating']) and 
          not any(word in user_message_lower for word in ['upgrade', 'premium', 'business', 'first'])):
        intent = 'Seating'
        response = "I can help you with seat selection. Would you like to choose your seats now?"
        confidence = 0.9
        
    # Meals (specific feature)
    elif any(phrase in user_message_lower for phrase in ['meal options', 'food options', 'dietary restrictions', 'special meal']) or \
         any(word in user_message_lower for word in ['meals', 'food', 'dining', 'dietary']):
        intent = 'Meals'
        response = "I can help you with meal options and special dietary requirements for your flight."
        confidence = 0.85
        
    # Boarding (specific process)
    elif any(phrase in user_message_lower for phrase in ['boarding time', 'boarding start', 'gate number', 'what gate']) or \
         (any(word in user_message_lower for word in ['boarding', 'board', 'gate']) and 
          not any(word in user_message_lower for word in ['check', 'pass'])):
        intent = 'Boarding'
        response = "Boarding information will be displayed on airport screens and announced at the gate."
        confidence = 0.85
        
    # Amenities (specific features)
    elif any(phrase in user_message_lower for phrase in ['wi-fi', 'wifi', 'entertainment', 'amenities available']) or \
         any(word in user_message_lower for word in ['amenities', 'facilities', 'services', 'entertainment']):
        intent = 'Amenities'
        response = "Our flights offer various amenities including entertainment, Wi-Fi, and comfort features."
        confidence = 0.8
        
    # Loyalty Programs (specific program)
    elif any(phrase in user_message_lower for phrase in ['frequent flyer', 'loyalty program', 'join program', 'membership benefits']) or \
         any(word in user_message_lower for word in ['loyalty', 'membership', 'miles', 'points']) and \
         any(word in user_message_lower for word in ['program', 'join', 'benefits']):
        intent = 'Loyalty Programs'
        response = "I can help you with our loyalty program. Are you interested in joining or have questions about your membership?"
        confidence = 0.85
        
    # Rewards (specific to earning/redeeming)
    elif any(phrase in user_message_lower for phrase in ['redeem miles', 'earn points', 'redeem points', 'reward redemption']) or \
         (any(word in user_message_lower for word in ['rewards', 'redeem', 'earn']) and 
          any(word in user_message_lower for word in ['miles', 'points', 'benefits'])):
        intent = 'Rewards'
        response = "Let me help you with reward redemption and earning opportunities."
        confidence = 0.8
        
    # Security (specific procedures)
    elif any(phrase in user_message_lower for phrase in ['prohibited items', 'carry-on restrictions', 'security procedures', 'tsa', 'screening']):
        intent = 'Security'
        response = "I can help you understand security procedures and what items are allowed in carry-on and checked baggage."
        confidence = 0.85
        
    # Safety (specific measures)
    elif any(phrase in user_message_lower for phrase in ['safety measures', 'safe to fly', 'safety procedures']) or \
         any(word in user_message_lower for word in ['safety', 'safe', 'emergency', 'health']):
        intent = 'Safety'
        response = "Safety is our top priority. I can provide information about our safety measures and procedures."
        confidence = 0.85
        
    # Promotions and Offers (marketing)
    elif any(phrase in user_message_lower for phrase in ['special deals', 'current promotions', 'special offers']) or \
         any(word in user_message_lower for word in ['promotion', 'promo', 'deal']):
        intent = 'Promotions'
        response = "Check out our current promotions and special offers for great deals on flights."
        confidence = 0.85
    elif any(word in user_message_lower for word in ['offers', 'deals', 'bargains', 'sales']):
        intent = 'Offers'
        response = "I can show you our latest offers and deals. What type of travel are you planning?"
        confidence = 0.8
        
    # Discounts (price-related)
    elif any(phrase in user_message_lower for phrase in ['student discount', 'get discount', 'lower price', 'save money']) or \
         any(word in user_message_lower for word in ['discount', 'cheaper']):
        intent = 'Discounts'
        response = "I can help you find discounted fares and ways to save on your booking."
        confidence = 0.85
        
    # Policies (rules and terms)
    elif any(phrase in user_message_lower for phrase in ['cancellation policy', 'refund policy', 'baggage policy']) or \
         (any(word in user_message_lower for word in ['policy', 'policies', 'rules', 'terms']) and 
          not any(word in user_message_lower for word in ['how', 'process', 'procedure'])):
        intent = 'Policies'
        response = "I can explain our policies regarding booking, cancellation, and travel requirements."
        confidence = 0.8
        
    # Procedures (how-to processes)
    elif any(phrase in user_message_lower for phrase in ['how do i', 'what is the process', 'how to']) or \
         any(word in user_message_lower for word in ['procedure', 'procedures', 'process']):
        intent = 'Procedures'
        response = "I can guide you through our procedures step by step. What process do you need help with?"
        confidence = 0.8
        
    # Regulations (travel requirements)
    elif any(phrase in user_message_lower for phrase in ['travel requirements', 'visa requirements', 'need visa']) or \
         any(word in user_message_lower for word in ['regulation', 'regulations', 'requirements', 'compliance']):
        intent = 'Regulations'
        response = "I can provide information about travel regulations and requirements for your destination."
        confidence = 0.8
        
    # Complaint (negative sentiment)
    elif any(phrase in user_message_lower for phrase in ['very unhappy', 'not satisfied', 'poor service']) or \
         any(word in user_message_lower for word in ['complaint', 'complain', 'dissatisfied', 'unhappy', 'problem', 'issue']):
        intent = 'Complaint'
        response = "I apologize for any inconvenience. Please describe the issue you're experiencing so I can help resolve it."
        confidence = 0.85
        
    # Feedback (reviews and suggestions)
    elif any(phrase in user_message_lower for phrase in ['leave feedback', 'share feedback', 'my review']) or \
         any(word in user_message_lower for word in ['feedback', 'review', 'comment', 'suggestion', 'opinion']):
        intent = 'Feedback'
        response = "Thank you for wanting to share your feedback. Your input helps us improve our services."
        confidence = 0.8
        
    # Change (modifications)
    elif any(phrase in user_message_lower for phrase in ['change booking', 'modify booking', 'update booking']) or \
         (any(word in user_message_lower for word in ['change', 'modify', 'update', 'alter']) and 
          any(word in user_message_lower for word in ['booking', 'flight', 'reservation'])):
        intent = 'Change'
        response = "I can help you change your booking. What modifications would you like to make?"
        confidence = 0.85
        
    # Booking (reservations and scheduling)
    elif any(phrase in user_message_lower for phrase in ['book flight', 'book a flight', 'make reservation', 'reserve seat']) or \
         any(word in user_message_lower for word in ['book', 'booking', 'reserve', 'reservation', 'schedule']) or \
         'flight' in user_message_lower:
        intent = 'Booking'
        response = f"I can help you with booking flights. What destination are you looking for? (Session: {session_id[:8]}...)"
        confidence = 0.85
        
    # Information (general info requests)
    elif any(phrase in user_message_lower for phrase in ['tell me about', 'information about', 'need information']) or \
         any(word in user_message_lower for word in ['information', 'info', 'details']):
        intent = 'Information'
        response = "I'm happy to provide information. What specific details would you like to know?"
        confidence = 0.75
        
    # Inquiry (questions)
    elif any(phrase in user_message_lower for phrase in ['i have a question', 'what time', 'how much', 'when does']) or \
         any(word in user_message_lower for word in ['inquiry', 'inquire', 'question', 'ask']):
        intent = 'Inquiry'
        response = "I'm here to answer your questions. What would you like to know?"
        confidence = 0.8
        
    # Support (general help)
    elif any(word in user_message_lower for word in ['support', 'help', 'assist', 'assistance']):
        intent = 'Support'
        response = "I'm here to provide support. How can I assist you today?"
        confidence = 0.85
        
    # Greeting and farewell intents
    elif any(word in user_message_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
        intent = 'Support'
        response = f"Hello! Welcome to our airline customer service. How can I help you today? (Session: {session_id[:8]}...)"
        confidence = 0.9
    elif any(word in user_message_lower for word in ['bye', 'goodbye', 'thank you', 'thanks', 'exit']):
        intent = 'Support'
        response = "Thank you for choosing our airline. Have a great day and safe travels!"
        confidence = 0.85
    else:
        intent = 'Inquiry'
        response = f"I understand you said: '{user_message}'. Could you please provide more details so I can assist you better?"
        confidence = 0.6
    
    return response, intent, confidence

def get_session_stats(session_id):
    """Get comprehensive session statistics for the management panel"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Get session info
    cur.execute("""
        SELECT created_at, last_activity 
        FROM sessions 
        WHERE session_id = ?
    """, (session_id,))
    session_info = cur.fetchone()
    
    # Get message counts
    cur.execute("""
        SELECT COUNT(*) as total_messages,
               SUM(CASE WHEN role = 'user' THEN 1 ELSE 0 END) as user_messages,
               SUM(CASE WHEN role = 'bot' THEN 1 ELSE 0 END) as bot_messages,
               AVG(CASE WHEN confidence IS NOT NULL THEN confidence * 100 ELSE NULL END) as avg_confidence
        FROM messages 
        WHERE session_id = ?
    """, (session_id,))
    message_stats = cur.fetchone()
    
    # Get intent distribution for this session
    cur.execute("""
        SELECT intent, COUNT(*) as count 
        FROM messages 
        WHERE session_id = ? AND intent IS NOT NULL 
        GROUP BY intent 
        ORDER BY count DESC
    """, (session_id,))
    intent_distribution = cur.fetchall()
    
    conn.close()
    
    # Format the data
    stats = {
        'session_id': session_id,
        'created_at': session_info[0] if session_info else 'Unknown',
        'last_activity': session_info[1] if session_info else 'Unknown',
        'message_count': message_stats[0] if message_stats else 0,
        'user_messages': message_stats[1] if message_stats else 0,
        'bot_messages': message_stats[2] if message_stats else 0,
        'avg_confidence': message_stats[3] if message_stats else None,
        'intent_distribution': [
            {'intent': intent, 'count': count} 
            for intent, count in intent_distribution
        ]
    }
    
    return stats

@app.route("/", methods=["GET", "POST"])
def chat():
    """Main chat interface"""
    session_id = get_session_id()
    
    if request.method == "POST":
        try:
            user_message = request.form.get("message", "").strip()
            
            if not user_message:
                logger.warning(f"Empty message received from session {session_id}")
                return redirect("/")
            
            logger.info(f"Message received from {session_id}: {user_message}")
            
            conn = get_conn()
            cur = conn.cursor()
            
            # Insert user message
            cur.execute("""
                INSERT INTO messages (session_id, role, content) 
                VALUES (?, 'user', ?)
            """, (session_id, user_message))
            
            # Generate bot response
            bot_reply, intent, confidence = simulate_bot_response(user_message, session_id)
            
            # Insert bot response with intent data
            cur.execute("""
                INSERT INTO messages (session_id, role, content, intent, confidence) 
                VALUES (?, 'bot', ?, ?, ?)
            """, (session_id, bot_reply, intent, confidence))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Bot response sent to {session_id}: {bot_reply} (Intent: {intent}, Confidence: {confidence})")
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
        
        return redirect("/")
    
    # GET request - display chat history
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        # Get messages with intent data
        cur.execute("""
            SELECT role, content, timestamp, intent, confidence 
            FROM messages 
            WHERE session_id = ? 
            ORDER BY timestamp ASC
        """, (session_id,))
        
        messages = cur.fetchall()
        
        # Get session stats
        cur.execute("""
            SELECT COUNT(*) as message_count,
                   MIN(timestamp) as first_message,
                   MAX(timestamp) as last_message
            FROM messages 
            WHERE session_id = ?
        """, (session_id,))
        
        stats = cur.fetchone()
        conn.close()
        
        # Prepare data for template
        message_list = []
        for msg in messages:
            message_list.append({
                'role': msg['role'],
                'content': msg['content'],
                'timestamp': msg['timestamp'],
                'intent': msg['intent'],
                'confidence': msg['confidence']
            })
        
        session_stats = {
            'session_id': session_id,
            'message_count': stats['message_count'] if stats else 0,
            'first_message': stats['first_message'] if stats else None,
            'last_message': stats['last_message'] if stats else None
        }
        
    except Exception as e:
        logger.error(f"Error retrieving messages: {e}")
        message_list = []
        session_stats = {'session_id': session_id, 'message_count': 0}
    
    resp = make_response(render_template("enhanced_chat.html", 
                                       messages=message_list, 
                                       stats=session_stats))
    resp.set_cookie("session_id", session_id, max_age=30*24*60*60)  # 30 days
    return resp

@app.route("/api/stats")
def api_stats():
    """API endpoint for chat statistics"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        # Overall stats
        cur.execute("SELECT COUNT(DISTINCT session_id) as total_sessions FROM sessions")
        total_sessions = cur.fetchone()['total_sessions']
        
        cur.execute("SELECT COUNT(*) as total_messages FROM messages")
        total_messages = cur.fetchone()['total_messages']
        
        cur.execute("""
            SELECT intent, COUNT(*) as count 
            FROM messages 
            WHERE intent IS NOT NULL 
            GROUP BY intent 
            ORDER BY count DESC
        """)
        intent_distribution = cur.fetchall()
        
        conn.close()
        
        return jsonify({
            'total_sessions': total_sessions,
            'total_messages': total_messages,
            'intent_distribution': [dict(row) for row in intent_distribution]
        })
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({'error': 'Failed to retrieve stats'}), 500

@app.route("/api/clear_session")
def clear_session():
    """Clear current session for testing"""
    session_id = get_session_id()
    
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
        conn.commit()
        conn.close()
        
        logger.info(f"Cleared session: {session_id}")
        
    except Exception as e:
        logger.error(f"Error clearing session: {e}")
    
    resp = make_response(redirect("/"))
    resp.set_cookie("session_id", "", expires=0)  # Clear cookie
    return resp

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return render_template('error.html', error="Internal server error"), 500

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error="Page not found"), 404

if __name__ == "__main__":
    # Run in debug mode for development
    app.run(debug=True, host="0.0.0.0", port=5000) 