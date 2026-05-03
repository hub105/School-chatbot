from flask import Flask, request, jsonify, render_template_string
from groq import Groq

app = Flask(__name__)

API_KEY = "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"
client = Groq(api_key=API_KEY)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Greenfield Academy</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #f0f0f0; display: flex; flex-direction: column; height: 100vh; }
        .header { background: #0a2a1a; color: white; padding: 12px 16px; display: flex; align-items: center; gap: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.3); }
        .header-avatar { background: #123d26; border-radius: 50%; width: 45px; height: 45px; display: flex; align-items: center; justify-content: center; font-size: 22px; border: 2px solid #4caf82; }
        .header-info h2 { font-size: 17px; color: #85e8b8; }
        .header-info p { font-size: 12px; opacity: 0.8; }
        .hero { background: linear-gradient(rgba(0,0,0,0.60), rgba(0,0,0,0.60)), url('https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=800') center/cover; padding: 28px 20px; color: white; text-align: center; }
        .hero h3 { font-size: 20px; margin-bottom: 6px; color: #85e8b8; }
        .hero p { font-size: 13px; opacity: 0.9; margin-bottom: 16px; }
        .hero-buttons { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; }
        .hero-btn { background: rgba(76,175,130,0.15); border: 2px solid #4caf82; color: #85e8b8; padding: 8px 18px; border-radius: 20px; font-size: 13px; cursor: pointer; backdrop-filter: blur(4px); }
        .hero-btn:hover { background: #4caf82; color: #0a2a1a; }
        .chat-box { flex: 1; overflow-y: auto; padding: 12px 16px; background: #f4f7f5; }
        .message { margin: 6px 0; display: flex; flex-direction: column; }
        .message.user { align-items: flex-end; }
        .message.bot { align-items: flex-start; }
        .bubble { max-width: 78%; padding: 10px 14px; border-radius: 18px; font-size: 14px; line-height: 1.6; position: relative; box-shadow: 0 1px 2px rgba(0,0,0,0.15); }
        .user .bubble { background: #0a2a1a; border: 1px solid #4caf82; color: #85e8b8; border-bottom-right-radius: 4px; }
        .bot .bubble { background: #ffffff; border: 1px solid rgba(76,175,130,0.3); color: #1a3a2a; border-bottom-left-radius: 4px; }
        .time { font-size: 10px; color: #888; margin-top: 3px; padding: 0 4px; }
        .input-area { display: flex; padding: 10px 12px; background: #e8f0ec; gap: 8px; align-items: center; border-top: 1px solid rgba(76,175,130,0.3); }
        .input-area input { flex: 1; padding: 11px 16px; border: 1px solid rgba(76,175,130,0.4); border-radius: 24px; background: #ffffff; color: #1a3a2a; font-size: 14px; outline: none; }
        .input-area input::placeholder { color: #888; }
        .input-area input:focus { border-color: #4caf82; }
        .input-area button { background: linear-gradient(135deg, #4caf82, #2d7a55); color: white; border: none; border-radius: 50%; width: 44px; height: 44px; font-size: 18px; cursor: pointer; box-shadow: 0 2px 5px rgba(76,175,130,0.4); font-weight: bold; }
        .footer { text-align: center; font-size: 11px; color: #4caf82; padding: 6px; background: #e8f0ec; letter-spacing: 1px; }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-avatar">🎓</div>
        <div class="header-info">
            <h2>Greenfield Academy</h2>
            <p>🟢 Nova AI Assistant • Available 24/7</p>
        </div>
    </div>

    <div class="hero">
        <h3>Welcome to Greenfield Academy</h3>
        <p>Admissions • School Fees • Timetable • Activities</p>
        <div class="hero-buttons">
            <button class="hero-btn" onclick="quickSend('How do I apply for admission?')">📋 Admissions</button>
            <button class="hero-btn" onclick="quickSend('What are the school fees?')">💰 School Fees</button>
            <button class="hero-btn" onclick="quickSend('What is the school timetable?')">📅 Timetable</button>
            <button class="hero-btn" onclick="quickSend('What clubs and activities do you have?')">🏆 Activities</button>
        </div>
    </div>

    <div class="chat-box" id="chat">
        <div class="message bot">
            <div class="bubble">Hello! I am Nova, your Greenfield Academy AI assistant. Whether you need help with admissions, school fees, timetables, or extracurricular activities — I am here for you. How may I assist you today?</div>
            <div class="time">Now</div>
        </div>
    </div>

    <div class="footer">🎓 Powered by Atlas Automations AI</div>

    <div class="input-area">
        <input type="text" id="msg" placeholder="Ask me anything about the school..." />
        <button onclick="send()">➤</button>
    </div>

    <script>
        let messages = [{role:"system", content:"You are Nova, a friendly and knowledgeable AI school assistant for Greenfield Academy. Help students, parents, and staff with: admissions (applications open January to March, requirements include previous school results, birth certificate, and passport photos, application fee is 5000 Naira), school fees (Primary and JSS 120000 Naira per term, Senior Secondary SSS 180000 Naira per term, fees cover tuition textbooks and uniform), academic calendar (First term September to December, Second term January to April, Third term May to July), timetable (school runs Monday to Friday 7:30am to 2:30pm, Saturday lessons for exam classes JSS3 and SSS3 8am to 12pm), subjects across Science Arts and Commercial tracks, exams (WAEC NECO JAMB prep available, mock exams held every February and October), extracurricular activities (football, basketball, debate club, science club, drama society, coding club, press club), school rules (full uniform Monday to Thursday, casual Friday, zero tolerance for bullying and truancy), contact info (info@greenfieldacademy.edu, 08012345678, visiting hours Monday to Friday 8am to 4pm). Collect the name of the student or parent when making enquiries. Use a warm, encouraging and professional tone. Keep responses 2 to 4 sentences. Always end with a warm offer to assist further."}];

        function getTime() {
            return new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        }

        function addMessage(text, sender) {
            const chat = document.getElementById("chat");
            const div = document.createElement("div");
            div.className = "message " + sender;
            div.innerHTML = '<div class="bubble">' + text + '</div><div class="time">' + getTime() + '</div>';
            chat.appendChild(div);
            chat.scrollTop = chat.scrollHeight;
        }

        async function send() {
            const input = document.getElementById("msg");
            const text = input.value.trim();
            if (!text) return;
            addMessage(text, "user");
            input.value = "";
            messages.push({role: "user", content: text});
            addMessage("typing...", "bot");
            const res = await fetch("/chat", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({messages: messages})
            });
            const data = await res.json();
            const chat = document.getElementById("chat");
            chat.removeChild(chat.lastChild);
            addMessage(data.reply, "bot");
            messages.push({role: "assistant", content: data.reply});
        }

        function quickSend(text) {
            document.getElementById("msg").value = text;
            send();
        }

        document.getElementById("msg").addEventListener("keypress", function(e) {
            if (e.key === "Enter") send();
        });
    </script>
</body>
</html>
'''

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    messages = data["messages"]
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )
    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
