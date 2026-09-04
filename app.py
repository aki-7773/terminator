#Flask web server (main entry point)
"""
Peak AI - Web Application with Multi-Chat Support
"""

# --- CRITICAL: Set Matplotlib backend BEFORE importing anything else ---
import matplotlib
matplotlib.use('Agg')

from flask import Flask, render_template, request, jsonify, abort
from chat import PeakAI
import os
import json
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-for-terminator')

# ---------- Chat Data Management ----------
CHATS_FILE = 'chats_data.json'
MAX_CHATS = 5

def load_chats():
    """Load chat data from JSON file, or create default if missing."""
    if os.path.exists(CHATS_FILE):
        with open(CHATS_FILE, 'r') as f:
            data = json.load(f)
        # Recreate AI instances for each chat
        for chat_id, chat_data in data.items():
            ai = PeakAI(chat_data.get('name', 'Terminator AI'))
            if 'history' in chat_data:
                ai.conversation_history = chat_data['history']
            chat_data['ai'] = ai
        return data
    else:
        # Create a default chat
        default_id = str(uuid.uuid4())
        ai = PeakAI("Terminator AI")
        return {
            default_id: {
                'id': default_id,
                'name': 'Chat 1',
                'ai': ai,
                'history': ai.conversation_history,
                'created_at': datetime.now().isoformat()
            }
        }

def save_chats():
    """Save chat data to JSON file (excluding AI instances)."""
    data = {}
    for chat_id, chat_data in chats.items():
        data[chat_id] = {
            'id': chat_data['id'],
            'name': chat_data['name'],
            'history': chat_data['ai'].conversation_history,
            'created_at': chat_data.get('created_at', datetime.now().isoformat())
        }
    with open(CHATS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Load chats on startup
chats = load_chats()

# ---------- Routes ----------

@app.route('/')
def index():
    """Render main chat interface."""
    return render_template('index.html')

@app.route('/chats', methods=['GET'])
def list_chats():
    """Return list of all chats (id, name, preview)."""
    result = []
    for chat_id, chat_data in chats.items():
        history = chat_data['ai'].conversation_history
        preview = ''
        if history:
            for msg in reversed(history):
                if msg.startswith('You:'):
                    preview = msg[5:][:50] + ('...' if len(msg) > 55 else '')
                    break
        result.append({
            'id': chat_id,
            'name': chat_data['name'],
            'preview': preview,
            'created_at': chat_data.get('created_at', '')
        })
    return jsonify(result)

@app.route('/chat/<chat_id>', methods=['GET'])
def get_chat(chat_id):
    """Return full conversation history for a chat."""
    if chat_id not in chats:
        abort(404)
    history = chats[chat_id]['ai'].conversation_history
    return jsonify({'history': history})

@app.route('/chat/new', methods=['POST'])
def new_chat():
    """Create a new chat (if under max)."""
    if len(chats) >= MAX_CHATS:
        return jsonify({'error': f'Maximum {MAX_CHATS} chats allowed'}), 400
    
    data = request.get_json() or {}
    name = data.get('name', f'Chat {len(chats)+1}')
    chat_id = str(uuid.uuid4())
    ai = PeakAI("Terminator AI")
    chats[chat_id] = {
        'id': chat_id,
        'name': name,
        'ai': ai,
        'history': ai.conversation_history,
        'created_at': datetime.now().isoformat()
    }
    save_chats()
    return jsonify({
        'id': chat_id,
        'name': name,
        'created_at': chats[chat_id]['created_at']
    })

@app.route('/chat/<chat_id>/delete', methods=['DELETE'])
def delete_chat(chat_id):
    """Delete a chat (only if more than 1)."""
    if len(chats) <= 1:
        return jsonify({'error': 'Cannot delete the last chat'}), 400
    if chat_id not in chats:
        abort(404)
    del chats[chat_id]
    save_chats()
    return jsonify({'status': 'deleted'})

@app.route('/chat/<chat_id>/send', methods=['POST'])
def send_message(chat_id):
    """Send a message to a specific chat and get AI response."""
    if chat_id not in chats:
        return jsonify({'error': 'Chat not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request'}), 400
    
    user_message = data.get('message', '').strip()
    if not user_message:
        return jsonify({'error': 'Empty message'}), 400
    
    try:
        ai = chats[chat_id]['ai']
        response = ai.process_input(user_message)
        save_chats()  # persist
        return jsonify({
            'response': response,
            'history': ai.conversation_history
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat/<chat_id>/rename', methods=['POST'])
def rename_chat(chat_id):
    """Rename a chat."""
    if chat_id not in chats:
        abort(404)
    data = request.get_json()
    new_name = data.get('name', '').strip()
    if not new_name:
        return jsonify({'error': 'Name cannot be empty'}), 400
    chats[chat_id]['name'] = new_name
    save_chats()
    return jsonify({'name': new_name})

@app.route('/reset', methods=['POST'])
def reset_conversation():
    return jsonify({'error': 'Use per-chat reset if needed'}), 400

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        'name': 'Terminator AI',
        'version': '3.0',
        'chats': len(chats),
        'status': 'success'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
