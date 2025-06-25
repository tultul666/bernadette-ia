from flask import Flask, render_template, request, jsonify, session
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
app.secret_key = 'bernadette_secret_key'

@app.route('/')
def index():
    session['history'] = []
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if 'history' not in session:
        session['history'] = []

    session['history'].append({"role": "user", "content": user_message})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Tu es Bernadette, une dinde intelligente, sarcastique et drôle."}] + session['history']
        )
        ai_reply = response['choices'][0]['message']['content']
        session['history'].append({"role": "assistant", "content": ai_reply})
    except Exception as e:
        ai_reply = f"Erreur : {e}"

    return jsonify({'response': ai_reply})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)
