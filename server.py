from flask import Flask, request, jsonify, render_template_string
from google import genai
import os

app = Flask(__name__)

# Gemini
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY environment variable is missing.")

client = genai.Client(api_key=api_key)


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

html,
body {
    margin: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    font-family: Arial, Helvetica, sans-serif;
    background: #080d12;
    color: #e8edf2;
}

body {
    display: flex;
}

/* APP */

.app {
    width: 100%;
    height: 100vh;
    display: flex;
    flex-direction: column;
}

/* HEADER */

.header {
    height: 70px;
    flex-shrink: 0;

    display: flex;
    align-items: center;

    padding: 0 28px;

    background: rgba(10, 16, 22, 0.96);

    border-bottom: 1px solid #26343f;

    z-index: 10;
}

.logo {
    display: flex;
    align-items: center;
    gap: 12px;
}

.logo-icon {
    width: 42px;
    height: 42px;

    display: flex;
    align-items: center;
    justify-content: center;

    border: 1px solid #536774;
    border-radius: 9px;

    background: #111b23;

    font-size: 21px;
}

.logo-text {
    font-size: 21px;
    font-weight: 700;
    letter-spacing: 0.5px;
}

.logo-sub {
    margin-top: 3px;

    font-size: 9px;
    color: #718490;

    letter-spacing: 2px;
}

/* CHAT */

.chat {
    flex: 1;
    min-height: 0;

    display: flex;
    flex-direction: column;
}

/* WELCOME */

.welcome {
    flex-shrink: 0;

    text-align: center;

    padding: 45px 20px 20px;
}

.welcome-symbol {
    width: 64px;
    height: 64px;

    margin: auto;

    display: flex;
    align-items: center;
    justify-content: center;

    border: 1px solid #536774;
    border-radius: 14px;

    background: #101a22;

    font-size: 28px;
}

.welcome h1 {
    margin: 17px 0 7px;

    font-size: 30px;
}

.welcome p {
    margin: 0;

    color: #7e909c;

    font-size: 14px;
}

/* MESSAGES */

.messages {
    flex: 1;
    min-height: 0;

    overflow-y: auto;

    padding: 15px 25px 30px;

    scroll-behavior: smooth;
}

.message {
    max-width: 850px;

    margin: 0 auto 25px;
}

.label {
    margin-bottom: 7px;

    font-size: 9px;

    letter-spacing: 1.6px;

    color: #718490;
}

/* USER */

.user {
    display: inline-block;

    max-width: 80%;

    padding: 13px 16px;

    background: #17232c;

    border: 1px solid #2c3c47;

    border-radius: 12px;

    line-height: 1.55;

    white-space: pre-wrap;

    word-wrap: break-word;
}

/* AI */

.ai {
    padding: 5px 2px;

    line-height: 1.7;

    white-space: pre-wrap;

    word-wrap: break-word;
}

/* LOADING */

.loading {
    color: #82939e;

    font-style: italic;

    animation: pulse 1.4s infinite;
}

@keyframes pulse {

    0% {
        opacity: 0.45;
    }

    50% {
        opacity: 1;
    }

    100% {
        opacity: 0.45;
    }

}

/* INPUT */

.input-area {
    flex-shrink: 0;

    padding: 15px 25px 20px;

    background: rgba(8, 13, 18, 0.97);

    border-top: 1px solid #26343f;
}

.input-box {
    max-width: 850px;

    margin: auto;

    position: relative;
}

textarea {
    width: 100%;

    height: 62px;

    resize: none;

    padding: 15px 60px 15px 16px;

    background: #111a22;

    color: #edf2f5;

    border: 1px solid #334550;

    border-radius: 11px;

    outline: none;

    font-family: inherit;

    font-size: 14px;

    line-height: 1.5;
}

textarea:focus {
    border-color: #617582;
}

textarea::placeholder {
    color: #667781;
}

/* SEND */

.send {
    position: absolute;

    right: 8px;
    bottom: 8px;

    width: 44px;
    height: 44px;

    border: 1px solid #536774;

    border-radius: 9px;

    background: #1a2933;

    color: white;

    font-size: 18px;

    cursor: pointer;
}

.send:hover {
    background: #263843;
}

.send:disabled {
    opacity: 0.45;

    cursor: not-allowed;
}

/* STATUS */

.status {
    max-width: 850px;

    margin: 7px auto 0;

    font-size: 9px;

    color: #5f717c;
}

/* SCROLLBAR */

.messages::-webkit-scrollbar {
    width: 6px;
}

.messages::-webkit-scrollbar-track {
    background: transparent;
}

.messages::-webkit-scrollbar-thumb {
    background: #263640;

    border-radius: 10px;
}

/* MOBILE */

@media(max-width: 700px) {

    .header {
        padding: 0 16px;
    }

    .messages {
        padding: 15px 16px 25px;
    }

    .input-area {
        padding: 12px 16px 16px;
    }

    .welcome {
        padding-top: 35px;
    }

    .welcome h1 {
        font-size: 25px;
    }

    .user {
        max-width: 90%;
    }

}

</style>

</head>


<body>

<div class="app">


<header class="header">

    <div class="logo">

        <div class="logo-icon">
            🔬
        </div>

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


<div
    class="messages"
    id="messages"
></div>


<div class="input-area">

    <div class="input-box">

        <textarea
            id="question"
            placeholder="Ask a forensic science question..."
        ></textarea>

        <button
            class="send"
            id="sendButton"
            onclick="askAI()"
        >
            ➤
        </button>

    </div>

    <div class="status">
        Forensix AI • Educational use • AI-generated information
    </div>

</div>


</section>


</div>


<script>

const questionBox =
    document.getElementById("question");

const messages =
    document.getElementById("messages");

const sendButton =
    document.getElementById("sendButton");

const welcome =
    document.getElementById("welcome");


/* ENTER TO SEND */

questionBox.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            askAI();
        }

    }
);


/* SCROLL */

function scrollToBottom() {

    requestAnimationFrame(function() {

        messages.scrollTop =
            messages.scrollHeight;

    });

}


/* ADD MESSAGE */

function addMessage(type, text) {

    const wrapper =
        document.createElement("div");

    wrapper.className =
        "message";

    const label =
        document.createElement("div");

    label.className =
        "label";

    label.textContent =
        type === "user"
            ? "YOU"
            : "FORENSIX AI";

    const content =
        document.createElement("div");

    content.className =
        type;

    content.textContent =
        text;

    wrapper.appendChild(label);

    wrapper.appendChild(content);

    messages.appendChild(wrapper);

    scrollToBottom();

    return wrapper;
}


/* ASK AI */

async function askAI() {

    const question =
        questionBox.value.trim();

    if (!question) {
        return;
    }


    /* HIDE WELCOME */

    welcome.style.display =
        "none";


    /* ADD USER MESSAGE */

    addMessage(
        "user",
        question
    );


    questionBox.value = "";

    sendButton.disabled = true;


    /* LOADING */

    const loadingMessage =
        addMessage(
            "ai",
            "Analyzing your question..."
        );

    loadingMessage
        .querySelector(".ai")
        .classList.add("loading");


    try {

        const response =
            await fetch(
                "/ask",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        question:
                            question
                    })
                }
            );


        let data;

        try {

            data =
                await response.json();

        } catch {

            throw new Error(
                "Server returned an invalid response."
            );

        }


        /* REMOVE LOADING */

        loadingMessage.remove();


        if (!response.ok) {

            addMessage(
                "ai",
                data.error ||
                "The server could not process your question."
            );

            return;
        }


        if (
            !data.answer ||
            !data.answer.trim()
        ) {

            addMessage(
                "ai",
                "No answer was returned."
            );

            return;
        }


        /* ANSWER */

        addMessage(
            "ai",
            data.answer
        );

    }

    catch (error) {

        loadingMessage.remove();

        addMessage(
            "ai",
            "Connection error: " +
            error.message
        );

    }

    finally {

        sendButton.disabled =
            false;

        questionBox.focus();

        scrollToBottom();

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

    try:

        data = request.get_json(
            silent=True
        )

        if not data:

            return jsonify({
                "error":
                "Invalid request."
            }), 400


        question = str(
            data.get("question", "")
        ).strip()


        if not question:

            return jsonify({
                "error":
                "Question is required."
            }), 400


        # Detect whether the user wants a deep answer
        question_lower = question.lower()

        deep_words = [
            "deep",
            "deeply",
            "detailed",
            "detail",
            "in detail",
            "elaborate",
            "elaboration",
            "comprehensive",
            "comprehensively",
            "long answer",
            "full explanation",
            "extensive",
            "deep dive",
            "explain thoroughly",
            "explain deeply"
        ]

        wants_deep_answer = any(
            word in question_lower
            for word in deep_words
        )


        if wants_deep_answer:

            length_instruction = """
The user explicitly wants a deep or detailed answer.

Give a comprehensive explanation with useful structure,
examples where appropriate, important forensic considerations,
and relevant scientific context.

Do not add unnecessary repetition.
"""

        else:

            length_instruction = """
The user did NOT ask for a deep or detailed answer.

Keep the answer concise and focused.

For a simple question, normally answer in roughly
3-6 sentences or a few short bullet points.

Do not turn a simple question into a long lecture.
"""


        prompt = f"""
You are Forensix AI, an educational forensic science assistant.

Your name is ALWAYS "Forensix AI".

Never start an answer with:
"Hello! I am Forensix AI"
or
"Hello, I am Forensix AI".

The website handles the initial welcome message.

{length_instruction}

Answer the user's actual question directly.

Focus on accurate forensic science education including:
crime scene investigation,
forensic biology,
DNA,
fingerprints,
forensic chemistry,
toxicology,
questioned documents,
firearms and toolmarks,
trace evidence,
digital forensics,
forensic anthropology,
forensic pathology,
and related forensic subjects.

Use clear language suitable for a forensic science student.

Do not invent facts, evidence, case details, statistics,
or scientific findings.

If something is uncertain or depends on circumstances,
say so clearly.

User question:
{question}
"""


        response = client.models.generate_content(

            model="gemini-3.6-flash",

            contents=prompt
        )


        answer = response.text


        if not answer:

            return jsonify({
                "error":
                "The AI returned an empty response."
            }), 502


        return jsonify({
            "answer":
            answer
        })


    except Exception as e:

        print(
            "ERROR /ask:",
            repr(e),
            flush=True
        )

        return jsonify({
            "error":
            "Forensix AI could not process this request right now. "
            "Please try again."
        }), 500


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