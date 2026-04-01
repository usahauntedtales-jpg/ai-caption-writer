import os
import google.generativeai as genai
from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- TERI GEMINI API KEY ---
GEMINI_KEY = "AIzaSyCohNDZnm_ys8ksoMIA_zlw0b68XwbFHC8"
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

# --- MODERN INSTAGRAM-STYLE UI ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jaivik AI - Caption Guru</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Helvetica Neue', sans-serif; }
        body { background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%); min-height: 100vh; display: flex; justify-content: center; align-items: center; padding: 20px; }
        .card { background: white; padding: 30px; border-radius: 25px; box-shadow: 0 15px 35px rgba(0,0,0,0.2); width: 100%; max-width: 500px; text-align: center; }
        .logo { font-size: 1.8em; font-weight: bold; background: -webkit-linear-gradient(#f09433, #bc1888); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px; }
        .subtitle { color: #666; margin-bottom: 25px; font-size: 0.9em; }
        textarea { width: 100%; padding: 15px; border-radius: 12px; border: 1px solid #ddd; font-size: 1em; height: 100px; outline: none; margin-bottom: 15px; resize: none; }
        .gen-btn { width: 100%; background: #bc1888; color: white; border: none; padding: 15px; border-radius: 12px; font-size: 1.1em; font-weight: bold; cursor: pointer; transition: 0.3s; }
        .gen-btn:hover { opacity: 0.9; transform: scale(0.98); }
        .result-area { margin-top: 25px; text-align: left; background: #fafafa; padding: 15px; border-radius: 12px; border: 1px solid #eee; white-space: pre-wrap; color: #333; line-height: 1.6; }
        .copy-hint { font-size: 0.8em; color: #999; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="card">
        <div class="logo">Jaivik AI Writer ✍️</div>
        <div class="subtitle">Enter your photo topic to get Viral Captions!</div>
        <form method="POST">
            <textarea name="topic" placeholder="Example: Jaipur trip with family, New bike, Morning tea..." required></textarea>
            <button type="submit" class="gen-btn">Generate Magic ✨</button>
        </form>
        
        {% if results %}
            <div class="result-area">
                <strong>🚀 Your AI Captions:</strong><br><br>{{ results }}
            </div>
            <p class="copy-hint">Copy and paste these to your Instagram/Twitter!</p>
        {% endif %}
        
        {% if error %}
            <p style="color: red; margin-top: 15px;">{{ error }}</p>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    results = None
    error = None
    if request.method == "POST":
        topic = request.form.get("topic", "")
        prompt = f"Write 3 different viral captions for an Instagram/Twitter post about: '{topic}'. One should be funny, one emotional, and one professional. Also add 10 trending hashtags."
        
        try:
            response = model.generate_content(prompt)
            results = response.text
        except Exception as e:
            error = "Bhai, API limit ya connection ka chakkar hai. Phir se try karo!"
            
    return render_template_string(HTML_TEMPLATE, results=results, error=error)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
  
