from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI
from google import genai
import os

app = Flask(__name__)


# =========================================================
# AI CLIENTS
# =========================================================

openrouter = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY")
)

nvidia = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.environ.get("NVIDIA_API_KEY")
)

gemini = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)


# =========================================================
# SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = """
You are Forensix AI, an educational forensic science assistant.

Answer only as much as the user's question requires.

For normal/simple questions:
- Give a concise answer.
- Usually 2-5 short paragraphs or a few clear points.
- Do not automatically give a huge lecture.

Only give a long, deep and comprehensive answer when the user explicitly
asks for words such as:
deep, detailed, in detail, elaborate, comprehensive, long answer,
full explanation, deep dive, extensive explanation, or similar wording.

Do not begin every answer with:
"Hello! I am Forensix AI."

The website handles the welcome message.

Refer to yourself as "Forensix AI".

Focus on:
forensic science,
crime scene investigation,
forensic biology,
DNA,
fingerprints,
toxicology,
questioned documents,
forensic chemistry,
digital forensics,
forensic anthropology,
forensic pathology,
ballistics,
trace evidence,
and related educational subjects.

Be scientifically accurate.
Do not invent evidence or facts.
Mention uncertainty when appropriate.

Keep answers educational and clear.
"""


# =========================================================
# OPENROUTER
# =========================================================

def ask_openrouter(question):

    print("Trying provider 1: OpenRouter / GLM 5.3 Flash", flush=True)

    response = openrouter.chat.completions.create(
        model="z-ai/glm-5.3-flash",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": question
            }
        ],
        max_tokens=1000,
        temperature=0.4
    )

    answer = response.choices[0].message.content

    if not answer:
        raise Exception("OpenRouter returned empty response")

    print("Provider 1 SUCCESS", flush=True)

    return answer


# =========================================================
# NVIDIA
# =========================================================

def ask_nvidia(question):

    print("Trying provider 2: NVIDIA Nemotron", flush=True)

    response = nvidia.chat.completions.create(
        model="nvidia/nemotron-3.5-lightning-30b-a3b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": question
            }
        ],
        max_tokens=1000,
        temperature=0.4,

        extra_body={
            "chat_template_kwargs": {
                "enable_thinking": False
            }
        }
    )

    answer = response.choices[0].message.content

    if not answer:
        raise Exception("NVIDIA returned empty response")

    print("Provider 2 SUCCESS", flush=True)

    return answer


# =========================================================
# GEMINI
# =========================================================

def ask_gemini(question):

    print("Trying provider 3: Gemini", flush=True)

    response = gemini.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"""
{SYSTEM_PROMPT}

User question:
{question}
"""
    )

    answer = response.text

    if not answer:
        raise Exception("Gemini returned empty response")

    print("Provider 3 SUCCESS", flush=True)

    return answer


# =========================================================
# HOME
# =========================================================

HTML = """
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

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
}

.logo-sub {
    font-size: 10px;
    color: #81919d;
    letter-spacing: 2px;
}

.main {
    flex: 1;
    display: flex;
    width: 100%;
    margin: auto;
}

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
    scroll-behavior: smooth;
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

@media(max-width: 750px) {

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

<div class="logo-text">
Forensix AI
</div>

<div class="logo-sub">
FORENSIC INTELLIGENCE SYSTEM
</div>

</div>

</div>

</header>


<div class="main">

<section class="chat">


<div class="welcome" id="welcome">

<div class="welcome-symbol">
🔬
</div>

<h1>
Forensix AI
</h1>

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

<button onclick="askAI()">
➤
</button>

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


function scrollChat() {

    const messages =
        document.getElementById("messages");

    messages.scrollTo({
        top: messages.scrollHeight,
        behavior: "smooth"
    });

}


function addMessage(type, text) {

    const messages =
        document.getElementById("messages");

    const div =
        document.createElement("div");

    div.className = "message";

    const label =
        type === "user"
        ? "YOU"
        : "FORENSIX AI";

    const content =
        String(text)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/\\n/g, "<br>");

    div.innerHTML =
        '<div class="label">' +
        label +
        '</div>' +
        '<div class="' +
        type +
        '">' +
        content +
        '</div>';

    messages.appendChild(div);

    scrollChat();

}


async function askAI() {

    const box =
        document.getElementById("question");

    const question =
        box.value.trim();

    if (!question) return;


    document
        .getElementById("welcome")
        .style.display = "none";


    addMessage("user", question);

    box.value = "";

    addMessage(
        "ai",
        "Analyzing your question..."
    );


    const loading =
        document
        .getElementById("messages")
        .lastElementChild;


    try {

        const response =
            await fetch("/ask", {

                method: "POST",

                headers: {
                    "Content-Type":
                    "application/json"
                },

                body: JSON.stringify({
                    question: question
                })

            });


        const data =
            await response.json();


        loading.remove();


        if (response.ok && data.answer) {

            addMessage(
                "ai",
                data.answer
            );

        } else {

            addMessage(
                "ai",
                data.error ||
                "Unable to generate an answer."
            );

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


# =========================================================
# ROUTES
# =========================================================

@app.route("/", methods=["GET"])
def home():

    return render_template_string(HTML)


@app.route("/ask", methods=["POST"])
def ask():

    try:

        data = request.get_json(silent=True) or {}

        question = data.get(
            "question",
            ""
        ).strip()


        if not question:

            return jsonify({
                "error": "Question is required"
            }), 400


        # =================================================
        # PROVIDER 1
        # =================================================

        try:

            answer = ask_openrouter(question)

            return jsonify({
                "answer": answer,
                "provider": "OpenRouter"
            })

        except Exception as e:

            print(
                "OpenRouter FAILED:",
                repr(e),
                flush=True
            )


        # =================================================
        # PROVIDER 2
        # =================================================

        try:

            answer = ask_nvidia(question)

            return jsonify({
                "answer": answer,
                "provider": "NVIDIA"
            })

        except Exception as e:

            print(
                "NVIDIA FAILED:",
                repr(e),
                flush=True
            )


        # =================================================
        # PROVIDER 3
        # =================================================

        try:

            answer = ask_gemini(question)

            return jsonify({
                "answer": answer,
                "provider": "Gemini"
            })

        except Exception as e:

            print(
                "Gemini FAILED:",
                repr(e),
                flush=True
            )


        # =================================================
        # ALL FAILED
        # =================================================

        print(
            "ALL AI PROVIDERS FAILED",
            flush=True
        )

        return jsonify({
            "error":
            "All AI providers are temporarily unavailable. Please try again in a moment."
        }), 503


    except Exception as e:

        print(
            "FATAL /ask ERROR:",
            repr(e),
            flush=True
        )

        return jsonify({
            "error": "Internal server error"
        }), 500


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            7860
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
    )