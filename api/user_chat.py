from flask import request, redirect, Blueprint
from modules.chat_history import ChatBotHistory


chat_bp = Blueprint('chat_bp', __name__)

assistant = ChatBotHistory()
assistant.setup_openai()

@chat_bp.route('/chatassistant', methods=['GET'])
# Function for the bot response
def get_bot_response():
    try:
        userText = request.args.get('msg')
        response = assistant.get_response(userText)
        return str(response)
    except Exception as e:
        return str(e)