from flask import Flask, render_template, request, jsonify
from datetime import datetime
import ollama

app = Flask(__name__)

@app.route('/')
def index():
    current_date = datetime.now().strftime('%m-%d-%Y')
    return render_template('index.html', current_date=current_date)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json['message']
    
    try:
        response = ollama.chat(model='llama3.1', messages=[
            {
                'role': 'user',
                'content': user_message,
            },
        ])
        ai_message = response['message']['content']
        print(ai_message)
        return jsonify({"response": ai_message})
    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 500

@app.template_filter('format_date')
def format_date(date):
    """
    Format a date string in a user-friendly way.
    """
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month, day, year = date.split('-')
    return f"{months[int(month) - 1]} {day}, {year}"

if __name__ == '__main__':
    app.run(debug=True)