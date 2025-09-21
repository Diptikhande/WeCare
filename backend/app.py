from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging
from app.chatbot import TherapistChatbot

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize chatbot
chatbot = None

def initialize_chatbot():
    """Initialize the therapist chatbot with vector database"""
    global chatbot
    try:
        chatbot = TherapistChatbot()
        logger.info("Therapist chatbot initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize chatbot: {str(e)}")
        chatbot = None

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'chatbot_ready': chatbot is not None
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        if not chatbot:
            return jsonify({
                'error': 'Chatbot not initialized'
            }), 500
        
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({
                'error': 'No message provided'
            }), 400
        
        user_message = data['message']
        session_id = data.get('session_id', 'default')
        
        # Get response from chatbot
        response = chatbot.get_response(user_message, session_id)
        
        return jsonify({
            'response': response,
            'session_id': session_id
        })
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'error': 'Internal server error'
        }), 500

@app.route('/api/chat/history/<session_id>', methods=['GET'])
def get_chat_history(session_id):
    """Get chat history for a session"""
    try:
        if not chatbot:
            return jsonify({
                'error': 'Chatbot not initialized'
            }), 500
        
        history = chatbot.get_chat_history(session_id)
        return jsonify({
            'history': history
        })
        
    except Exception as e:
        logger.error(f"Error getting chat history: {str(e)}")
        return jsonify({
            'error': 'Internal server error'
        }), 500

@app.route('/api/chat/reset/<session_id>', methods=['POST'])
def reset_chat(session_id):
    """Reset chat session"""
    try:
        if not chatbot:
            return jsonify({
                'error': 'Chatbot not initialized'
            }), 500
        
        chatbot.reset_session(session_id)
        return jsonify({
            'message': 'Session reset successfully'
        })
        
    except Exception as e:
        logger.error(f"Error resetting chat: {str(e)}")
        return jsonify({
            'error': 'Internal server error'
        }), 500

if __name__ == '__main__':
    initialize_chatbot()
    app.run(
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    )