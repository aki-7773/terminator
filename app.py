#Flask web server (main entry point)
"""
Peak AI - Web Application
Flask server for the Terminator AI Chatbot
"""

from flask import Flask, render_template, request, jsonify
from chat import PeakAI
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-for-terminator')

# Initialize the AI
ai = PeakAI("Terminator AI")

@app.route('/')
def index():
    """Render the main chat interface"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Get AI response
        response = ai.process_input(user_message)
        
        return jsonify({
            'response': response,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/reset', methods=['POST'])
def reset():
    """Reset the conversation"""
    global ai
    ai = PeakAI("Terminator AI")
    return jsonify({'status': 'reset'})

@app.route('/status', methods=['GET'])
def status():
    """Get AI status"""
    return jsonify({
        'name': ai.name,
        'version': ai.version,
        'conversations': len(ai.conversation_history),
        'internet': ai.utils.internet_enabled
    })

if __name__ == '__main__':
    # For local development
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
