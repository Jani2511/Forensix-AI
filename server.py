from flask import Flask, request, jsonify, render_template_string
from google import genai
import os

app = Flask(__name__)

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Forensic AI</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
        }
        h1 {
            text-align: center;
        }
        textarea {
            width: 100%;
            height: 120px;
            padding: 12px;
            box-sizing: border-box;
        }
        button {
            margin-top: 12px;
            padding: 12px 24px;
            cursor: pointer;
        }
        #answer {
            margin-top: 25px;
            padding: 20px;
            white-space: pre-wrap;
            border: 1px solid #ddd;
        }
    </style>
</head>
<body>

<h1>🔬 Forensic AI</h1>

<textarea id="question" placeholder="Ask a forensic science question..."></textarea>

<button onclick="askAI()">Ask Forensic AI</button>

<div id="answer">Your answer will appear here.</div>

<script>
async function askAI() {
    const question = document.getElementById("question").value;
    const answer = document.getElementById("answer");

    if (!question.trim()) {
        answer.innerText = "Please enter a question.";
        return;
    }

    answer.innerText = "Thinking...";

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

    answer.innerText = data.answer || data.error;
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
        return jsonify({"error": "Question is required"}), 400

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"""
You are Forensic AI, an educational forensic science assistant.

Give accurate, clear and detailed forensic science answers.
Explain concepts in a student-friendly way.
Do not invent facts.
If information is uncertain, clearly state that.

Question:
{question}
"""
    )

    return jsonify({"answer": response.text})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)