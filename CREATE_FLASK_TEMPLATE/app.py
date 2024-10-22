from flask import Flask, render_template, request, jsonify
from functions.ollama_utils import get_ollama_response
from functions.template_utils import format_message

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.json
    user_message = data['message']
    temperature = float(data.get('temperature', 0.7))
    max_length = int(data.get('max_length', 500))
    top_p = float(data.get('top_p', 0.9))
    
    response = get_ollama_response(user_message, temperature, max_length, top_p)
    return jsonify({'response': response})


if __name__ == '__main__':
    app.run(debug=True, port=8080)