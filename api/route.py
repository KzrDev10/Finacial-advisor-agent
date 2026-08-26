from flask import Blueprint, request, jsonify
from agents.ai_agent import run_agent

chat_bp = Blueprint('chat_bp', __name__, url_prefix='/api/chat')

@chat_bp.route('/', methods=['POST'])
def chat():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'Message is required'}), 400

    user_message = data.get('message')
    
    # Run the AI agent
    try:
        response = run_agent(user_message)
        return jsonify({'response': response}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
