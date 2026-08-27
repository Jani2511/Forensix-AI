from flask import Flask, request, jsonify, render_template_string
from google import genai
import os

app = Flask(__name__)

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Forensix AI</title>

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    background: #080d12;
    color: #e8edf2;
    font-family: Arial, Helvetica, sans-serif;
}

.app {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

/* HEADER */

.header {
    height: 72px;
    background: #0d141b;
    border-bottom: 1px solid #26343f;
    display: flex;
    align-items: center;
    padding: 0 28px;
}

.logo {
    display: flex;
    align-items: center;
    gap: 12px;
}

.logo-icon {
    width: 42px;
    height: 42px;
    border: 1px solid #526675;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 21px;
    background: #111b23;
}

.logo-text {
    font-size: 21px;
    font-weight: 700;
    letter-spacing: 0.5px;
}

.logo-sub {
    font-size: 10px;
    color: #81919d;
    letter-spacing: 2px;
}

/* MAIN */

.main {
    flex: 1;
    display: flex;
    max-width: 1200px;
    width: 100%;
    margin: auto;
}

/* SIDEBAR */

.sidebar {
    width: 245px;
    border-right: 1px solid #26343f;
    padding: 25px 18px;
}

.side-title {
    font-size: 11px;
    color: #71828e;
    letter-spacing: 2px;
    margin-bottom: 15px;
}

.case-card {
    background: #0e171f;
    border: 1px solid #25343f;
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 10px;
}

.case-card strong {
    display: block;
    font-size: 13px;
    margin-bottom: 6px;
}

.case-card span {
    font-size: 11px;
    color: #778893;
}

/* CHAT */

.chat {
    flex: 1;
    display: flex;
    flex-direction: column;
    min-width: 0;
}

.welcome {
    padding: 65px 30px 25px;
    text-align: center;
}

.welcome-symbol {
    width: 68px;
    height: 68px;
    margin: auto;
    border: 1px solid #526675;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 30px;
    background: #101a22;
}

.welcome h1 {
    margin: 20px 0 8px;
    font-size: 30px;
}

.welcome p {
    color: #82929d;
    margin: 0;
    font-size: 14px;
}

.messages {
    flex: 1;
    overflow-y: auto;
    padding: 25px 30px;
}

.message {
    max-width: 850px;
    margin: 0 auto 22px;
}

.user {
    background: #16212a;
    border: 1px solid #2a3a46;
    border-radius: 10px;
    padding: 14px 16px;
}

.ai {
    padding: 5px 4px;
    line-height: 1.65;
}

.label {
    font-size: 10px;
    letter-spacing: 1.5px;
    color: #718490;
    margin-bottom: 7px;
}

/* INPUT */

.input-area {
    padding: 18px 30px 25px;
    border-top: 1px solid #26343f;
    background: #0b1117;
}

.input-box {
    max-width: 850px;
    margin: auto;
    position: relative;
}

textarea {
    width: 100%;
    resize: none;
    height: 65px;
    background: #111a22;
    color: #edf2f5;
    border: 1px solid #334550;
    border-radius: 10px;
    padding: 16px 65px 16px 16px;
    font-size: 14px;
    outline: none;
}

textarea:focus {
    border-color: #637986;
}

button {
    position: absolute;
    right: 9px;
    bottom: 9px;
    width: 42px;
    height: 42px;
    border: 1px solid #566975;
    background: #1b2933;
    color: white;
    border-radius: 8px;
    cursor: pointer;
    font-size: 18px;
}

button:hover {
    background: #263843;
}

.status {
    max-width: 850px;
    margin: 8px auto 0;
    font-size: 10px;
    color: #61727e;
}

/* MOBILE */

@media(max-width: 750px) {

    .sidebar {
        display: none;
    }

    .header {
        padding: 0 16px;
    }

    .messages {
        padding: 20px 16px;
    }

    .welcome {
        padding: 45px 20px 20px;
    }

    .input-area {
        padding: 12px 16px 18px;
    }
}
</style>
</head>

<body>

<div class="app">

<header class="header">

    <div class="logo">

        <div class="logo-icon">🔬</div>

        <div>
            <div class="logo-text">Forensix AI</div>
            <div class="logo-sub">FORENSIC INTELLIGENCE SYSTEM</div>
        </div>

    </div>

</header>


<div class="main">

<aside class="sidebar">

    <div class="side-title">FORENSIC MODULES</div>

    <div class="case-card">
        <strong>DNA Analysis</strong>
        <span>Biological evidence</span>
    </div>

    <div class="case-card">
        <strong>Fingerprint Analysis</strong>
        <span>Pattern & ridge examination</span>
    </div>

    <div class="case-card">
        <strong>Crime Scene</strong>
        <span>Evidence interpretation</span>
    </div>

    <div class="case-card">
        <strong>Toxicology</strong>
        <span>Drugs & poisons</span>
    </div>

    <div class="case-card">
        <strong>Digital Forensics</strong>
        <span>Digital evidence</span>
    </div>

</aside>


<section class="chat">

<div class="welcome" id="welcome">

    <div class="welcome-symbol">🔬</div>

    <h1>Forensix AI</h1>

    <p>
        Your educational forensic science intelligence assistant.
    </p>

</div>


<div class="messages" id="messages"></div>


<div class="input-area">

    <div class="input-box">

        <textarea
            id="question"
            placeholder="Ask a forensic science question..."
            onkeydown="handleKey(event)"
        ></textarea>

        <button onclick="askAI()">➤</button>

    </div>

    <div class="status">
        Forensix AI • Educational use • AI-generated information
    </div>

</div>

</section>

</div>

</div>


<script>

function handleKey(event) {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();

        askAI();
    }
}


function addMessage(type, text) {

    const messages = document.getElementById("messages");

    const div = document.createElement("div");

    div.className = "message";

    const label = type === "user" ? "YOU" : "FORENSIX AI";

    div.innerHTML =
        '<div class="label">' + label + '</div>' +
        '<div class="' + type + '">' +
        text.replace(/\\n/g, "<br>") +
        '</div>';

    messages.appendChild(div);

    messages.scrollTop = messages.scrollHeight;
}


async function askAI() {

    const box = document.getElementById("question");

    const question = box.value.trim();

    if (!question) return;

    document.getElementById("welcome").style.display = "none";

    addMessage("user", question);

    box.value = "";

    addMessage("ai", "Analyzing your question...");

    const loading =
        document.getElementById("messages").lastElementChild;

    try {

        const response = await fetch("/ask", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })

        });

        const data = await response.json();

        loading.remove();

        if (data.answer) {

            addMessage("ai", data.answer);

        } else {

            addMessage("ai", "Unable to generate an answer.");

        }

    } catch (error) {

        loading.remove();

        addMessage(
            "ai",
            "Connection error. Please try again."
        );

    }
}

</script>

</body>
</html>
"""


@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML)


@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()

    question = data.get("question", "").strip()

    if not question:
        return jsonify({
            "error": "Question is required"
        }), 400


    response = client.models.generate_content(

        model="gemini-3.6-flash",

        contents=f"""
You are Forensix AI, an educational forensic science assistant.

IMPORTANT RESPONSE LENGTH RULE:

Give the user ONLY as much information as their question requires.

For normal/simple questions:
Give a concise answer, usually around 2-5 paragraphs or a few clear points.

Do NOT automatically give a huge lecture.

ONLY provide a long, deep, comprehensive answer when the user explicitly asks for:
deep explanation, detailed explanation, in detail, elaborate, comprehensive,
long answer, full explanation, deep dive, extensive explanation,
or similar wording.

If the question is simple, keep the answer simple.

Do not begin every answer with:
"Hello! I am Forensix AI."

The welcome message is handled by the website.

Use the name "Forensix AI" when referring to yourself.

Focus on forensic science, crime scene investigation, forensic biology,
DNA, fingerprints, toxicology, questioned documents, forensic chemistry,
digital forensics, forensic anthropology, forensic pathology and related
educational subjects.

Be scientifically accurate.
Do not invent evidence or facts.
Clearly mention uncertainty when appropriate.

User question:
{question}
"""
    )

    return jsonify({
        "answer": response.text
    })


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 7860))

    app.run(
        host="0.0.0.0",
        port=port
    )