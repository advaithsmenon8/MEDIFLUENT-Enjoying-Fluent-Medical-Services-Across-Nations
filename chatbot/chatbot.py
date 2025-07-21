# chatbot/chatbot.py

from flask import Blueprint, render_template, request, jsonify
import ollama  # Ensure ollama is properly installed and imported

# Define the chatbot blueprint
chatbot_bp = Blueprint('chatbot', __name__, template_folder='../website/templates')  # Path to templates

# Chatbot main page route
@chatbot_bp.route('/chatbot')
def chatbot():
    return render_template('index.html')  # Chatbot UI page

# Chat route for chatbot interactions
@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    data = request.json
    drug_name = data.get('drug')
    country = data.get('country')

    # Instruct the model to provide concise responses
    response = ollama.chat(model='llama3', messages=[ 
        {'role': 'system', 'content': 'Provide only the name of the equivalent drug, without any extra details.'},
        {'role': 'user', 'content': f"Give the equivalent drug for {drug_name} in {country}."}
    ])
    
    return jsonify(response['message']['content'])  # Return only the message content
