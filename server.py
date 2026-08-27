from flask import Flask, request, jsonify
from google import genai
import os

app = Flask(__name__)

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

@app.route("/")
def home():
    return "Forensic AI is online!"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")

    if not question:
        return jsonify({"error": "Question is required"}), 400

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"""
You are Forensic AI, an educational forensic science assistant.

Answer the user's question accurately, clearly and in detail.
Use forensic science terminology where appropriate.
Do not invent facts.
If information is uncertain, clearly say so.

User question:
{question}
"""
    )

    return jsonify({"answer": response.text})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)