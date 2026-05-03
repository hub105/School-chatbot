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
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'DM Sans', sans-serif;
            background: #f4f6f0;
            display: flex;
            flex-direction: column;
            height: 100vh;
            overflow: hidden;
        }

        /* ── HEADER ── */
        .header {
            background: #1b3a2d;
            color: white;
            padding: 12px 16px;
            display: flex;
            align-items: center;
            gap: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.25);
        }
        .header-avatar {
            background: #245c3e;
            border-radius: 50%;
            width: 46px;
            height: 46px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            border: 2px solid #7ec8a0;
            flex-shrink: 0;
        }
        .header-info h2 {
            font-family: 'Playfair Display', serif;
            font-size: 17px;
            color: #a8e6c0;
            letter-spacing: 0.3px;
        }
        .header-info p { font-size: 12px; opacity: 0.75; margin-top: 2px; }

        /* ── HERO ── */
        .hero {
            background: linear-gradient(rgba(10,40,22,0.72), rgba(10,40,22,0.72)),
                        url('https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=800') center/cover no-repeat;
            padding: 26px 20px;
            color: white;
            text-align: center;
        }
        .hero h3 {
            font-family: 'Playfair Display', serif;
            font-size: 20px;
            color: #a8e6c0;
            margin-bottom: 5px;
        }
        .hero p { font-size: 12px; opacity: 0.85; margin-bottom: 15px; }
        .hero-buttons { display: flex; gap: 9px; justify-content: center; flex-wrap: wrap; }
        .hero-btn {
            background: rgba(126,200,160,0.12);
            border: 1.5px solid #7ec8a0;
            color: #a8e6c0;
            padding: 7px 16px;
            border-radius: 20px;
            font-size: 12px;
            font-family: 'DM Sans', sans-serif;
            cursor: pointer;
            backdrop-filter: blur(4px);
            transition: all 0.2s;
        }
        .hero-btn:hover { background: #7ec8a0; color: #1b3a2d; font-weight: 600; }

        /* ── CHAT BOX ── */
        .chat-box {
            flex: 1;
            overflow-y: auto;
            padding: 14px 16px;
            background: #f0f3eb;
            scroll-behavior: smooth;
        }
        .chat-box::-webkit-scrollbar { width: 4px; }
        .chat-box::-webkit-scrollbar-thumb { background: #b0c8b8; border-radius: 4px; }

        .message { margin: 7px 0; display: flex; flex-direction: column; animation: fadeUp 0.25s ease; }
        @keyframes fadeUp {
            from { opacity: 0; transform: translateY(6px); }
            to   { opacity: 1; transform: translateY(0); }
        }
        .message.user  { align-items: flex-end; }
        .message.bot   { align-items: flex-start; }

        .bubble {
            max-width: 78%;
            padding: 10px 14px;
            border-radius: 18px;
            font-size: 14px;
            line-height: 1.65;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .user .bubble {
            background: #1b3a2d;
            color: #d4f0e2;
            border-bottom-right-radius: 4px;
            border: 1px solid #245c3e;
        }
        .bot .bubble {
            background: #ffffff;
            color: #2c3e35;
            border-bottom-left-radius: 4px;
            border: 1px solid #d8e8dd;
        }
        .time { font-size: 10px; color: #8aaa96; margin-top: 3px; padding: 0 4px; }

        /* ── INPUT ── */
        .input-area {
            display: flex;
            padding: 10px 12px;
            background: #e8ede4;
            gap: 9px;
            align-items: center;
            border-top: 1px solid #c8d8cc;
        }
        .input-area input {
            flex: 1;
            padding: 11px 16px;
            border: 1.5px solid #b0c8b8;
            border-radius: 24px;
            background: #ffffff;
            color: #2c3e35;
            font-size: 14px;
            font-family: 'DM Sans', sans-serif;
            outline: none;
            transition: border-color 0.2s;
        }
        .input-area input::placeholder { color: #9ab0a2; }
        .input-area input:focus { border-color: #3a8c5c; }
        .input-area button {
            background: linear-gradient(135deg, #3a8c5c, #1b3a2d);
            color: white;
            border: none;
            border-radius: 50%;
            width: 44px;
            height: 44px;
            font-size: 18px;
            cursor: pointer;
            box-shadow: 0 2px 6px rgba(58,140,92,0.35);
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            transition: transform 0.15s;
        }
        .input-area button:hover { transform: scale(1.08); }

        /* ── FOOTER ── */
        .footer {
            text-align: center;
            font-size: 11px;
            color: #3a8c5c;
            padding: 6px;
            background: #e8ede4;
            letter-spacing: 1px;
            border-top: 1px solid #c8d8cc;
        }

        /* ── TYPING DOTS ── */
        .dots span {
            display: inline-block;
            width: 7px; height: 7px;
            border-radius: 50%;
            background: #3a8c5c;
            margin: 0 2px;
            animation: blink 1.2s infinite;
        }
        .dots span:nth-child(2) { animation-delay: 0.2s; }
        .dots span:nth-child(3) { animation-delay: 0.4s; }
        @keyframes blink {
            0%, 100% { opacity: 0.2; }
            50%       { opacity: 1; }
        }
    </style>
</head>
<body>

    <!-- HEADER -->
    <div class="header">
        <div class="header-avatar">🎓</div>
        <div class="header-info">
            <h2>Greenfield Academy</h2>
            <p>🟢 Nova — AI School Assistant • Available 24/7</p>
        </div>
    </div>

    <!-- HERO -->
    <div class="hero">
        <h3>Welcome to Greenfield Academy</h3>
        <p>Admissions • Fees • Timetable • Activities</p>
        <div class="hero-buttons">
            <button class="hero-btn" onclick="quickSend('How do I apply for admission?')">📋 Admissions</button>
            <button class="hero-btn" onclick="quickSend('What are the school fees?')">💰 School Fees</button>
            <button class="hero-btn" onclick="quickSend('What is the school timetable?')">📅 Timetable</button>
            <button class="hero-btn" onclick="quickSend('What clubs and activities do you have?')">🏆 Activities</button>
        </div>
    </div>

    <!-- CHAT -->
    <div class="chat-box" id="chat">
        <div class="message bot">
            <div class="bubble">
                Hello! I'm <strong>Nova</strong>, your Greenfield Academy AI assistant 👋. 
                I can help you with admissions, school fees, timetables, exam schedules, clubs, and more. 
                How can I assist you today?
            </div>
            <div class="time">Now</div>
        </div>
    </div>

    <!-- FOOTER -->
    <div class="footer">🎓 Powered by Greenfield Academy AI</div>

    <!-- INPUT -->
    <div class="input-area">
        <input type="text" id="msg" placeholder="Ask me anything about the school..." />
        <button onclick="send()">➤</button>
    </div>

    <script>
        let messages = [
            {
                role: "system",
                content: `You are Nova, a warm and knowledgeable AI school assistant for Greenfield Academy. 
Help students, parents, and staff with the following:
- Admissions: applications open January–March each year, requirements include previous school results, birth certificate, and passport photos. Application fee is 5,000 Naira.
- School fees: Primary (JSS1-3) = 120,000 Naira/term, Senior Secondary (SSS1-3) = 180,000 Naira/term. Fees cover tuition, textbooks, and uniform. Bursary/scholarship available for top applicants.
- Academic calendar: First term Sept–Dec, Second term Jan–April, Third term May–July.
- Timetable: School runs Mon–Fri, 7:30am–2:30pm. Saturday lessons for exam classes (JSS3, SSS3) 8am–12pm.
- Subjects: Core and elective subjects across Sciences, Arts, and Commercial tracks.
- Exams: WAEC, NECO, and JAMB prep classes available. Mock exams held every February and October.
- Extracurricular: Football, basketball, debate club, science club, drama society, coding club, press club.
- School rules: Full uniform required Mon–Thu, casual Friday allowed. Zero tolerance for bullying and truancy.
- Contact: info@greenfieldacademy.edu | 08012345678 | Visiting hours Mon–Fri 8am–4pm.
Use an encouraging, friendly, and professional tone. Keep responses 2 to 4 sentences. Always end with a warm offer to assist further.`
            }
        ];

        function getTime() {
            return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        }

        function addMessage(text, sender) {
            const chat = document.getElementById("chat");
            const div = document.createElement("div");
            div.className = "message " + sender;
            div.innerHTML = '<div class="bubble">' + text + '</div><div class="time">' + getTime() + '</div>';
            chat.appendChild(div);
            chat.scrollTop = chat.scrollHeight;
        }

        function addTyping() {
            const chat = document.getElementById("chat");
            const div = document.createElement("div");
            div.className = "message bot";
            div.id = "typing-indicator";
            div.innerHTML = '<div class="bubble dots"><span></span><span></span><span></span></div>';
            chat.appendChild(div);
            chat.scrollTop = chat.scrollHeight;
        }

        function removeTyping() {
            const el = document.getElementById("typing-indicator");
            if (el) el.remove();
        }

        async function send() {
            const input = document.getElementById("msg");
            const text = input.value.trim();
            if (!text) return;

            addMessage(text, "user");
            input.value = "";
            messages.push({ role: "user", content: text });

            addTyping();

            try {
                const res = await fetch("/chat", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ messages: messages })
                });
                const data = await res.json();
                removeTyping();
                addMessage(data.reply, "bot");
                messages.push({ role: "assistant", content: data.reply });
            } catch (err) {
                removeTyping();
                addMessage("Sorry, I'm having trouble connecting right now. Please try again shortly.", "bot");
            }
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
