import os
import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- TERI API KEY ---
GEMINI_KEY = "AIzaSyBvkE49kLx0pURGIaMX0HvIbQL5kMkGlWM"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jaivik AI - Caption Guru</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', sans-serif; }
        body { background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%); min-height: 100vh; display: flex; justify-content: center; align-items: center; padding: 20px; }
        .card { background: white; padding: 30px; border-radius: 25px; box-shadow: 0 15px 35px rgba(0,0,0,0.2); width: 100%; max-width: 500px; text-align: center; }
        .logo { font-size: 1.8em; font-weight: bold; background: -webkit-linear-gradient(#f09433, #bc1888); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px; display: inline-block; }
        textarea { width: 100%; padding: 15px; border-radius: 12px; border: 1px solid #ddd; font-size: 1em; height: 100px; outline: none; margin-bottom: 15px; resize: none; }
        .gen-btn { width: 100%; background: #bc1888; color: white; border: none; padding: 15px; border-radius: 12px; font-size: 1.1em; font-weight: bold; cursor: pointer; }
        .result-area { margin-top: 25px; text-align: left; background: #fafafa; padding: 15px; border-radius: 12px; border: 1px solid #eee; white-space: pre-wrap; color: #333; line-height: 1.6; }
    </style>
</head>
<body>
    <div class="card">
        <div class="logo">Jaivik AI Writer ✍️</div>
        <form method="POST">
            <textarea name="topic" placeholder="Example: Jaipur trip with family..." required></textarea>
            <button type="submit" class="gen-btn">Generate Magic ✨</button>
        </form>
        {% if results %}<div class="result-area"><strong>🚀 Your AI Captions:</strong><br><br>{{ results }}</div>{% endif %}
        {% if error %}<p style="color: red; margin-top: 15px;">{{ error }}</p>{% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    results, error = None, None
    if request.method == "POST":
        topic = request.form.get("topic", "")
        # Pure REST API call - Sabse stable tarika
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{
                "parts": [{"text": f"Write 3 short viral Instagram captions for: {topic}. Add emojis."}]
            }]
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response_json = response.json()
            # Extracting text from Gemini response
            results = response_json['candidates']['content']['parts']['text']
        except Exception as e:
            error = "Bhai, API thoda busy hai. Ek baar refresh karke try karo."
            
    return render_template_string(HTML_TEMPLATE, results=results, error=error)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
    
