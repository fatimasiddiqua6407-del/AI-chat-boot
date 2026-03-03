from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# API Key yahan safe rahegi
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
        
    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "http://localhost:5000", # Optional: OpenRouter requirements
                "X-Title": "My Local Bot",
            },
            model="openrouter/free",
            messages=[{"role": "user", "content": user_message}]
        )
        ai_response = completion.choices[0].message.content
        return jsonify({"response": ai_response})
    except Exception as e:
        print("Error details:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)