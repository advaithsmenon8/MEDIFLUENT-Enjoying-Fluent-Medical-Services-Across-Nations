from flask import Blueprint, render_template, request, jsonify
import ollama

# Define the blueprint
chatbot2_bp = Blueprint('chatbot2', __name__, template_folder='templates')

# Define routes under the chatbot2 blueprint
@chatbot2_bp.route('/')
def home():
    return render_template('emergency.html')  # Update with correct path to your emergency chatbot template

@chatbot2_bp.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']

    # Sending the message to the Ollama model
    response = ollama.chat(
        model='llama3',
        messages=[
            {'role': 'system', 'content': (
                'Respond in a clearly formatted point-wise list. Use HTML <ul> and <li> tags with numbered points and bold headings for each point. '
                'Ensure each response is formatted like: <li><strong>1. Heading:</strong> Explanation...</li>.'  
            )},
            {'role': 'user', 'content': user_message}
        ]
    )

    # Format the response in a <ul> tag for proper HTML display
    formatted_response = f"<ul>{response['message']['content']}</ul>"
    return jsonify({'content': formatted_response})

