from flask import Flask, render_template, request, jsonify, session
import openai
import os

app = Flask(__name__)
app.secret_key = "bernadette-super-secrete"

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    if 'history' not in session:
        session['history'] = []
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json['message']
    session['history'].append({"role": "user", "content": user_input})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es Bernadette, une dinde super intelligente, sarcastique et drôle."}
            ] + session['history']
        )
        ai_reply = response['choices'][0]['message']['content']
        session['history'].append({"role": "assistant", "content": ai_reply})
    except Exception as e:
        ai_reply = f"Erreur : {e}"

    return jsonify({'response': ai_reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
