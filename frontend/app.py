import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, jsonify
from retrieval.search import search_query
from llm.groq_llama import get_llama_response

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    # Accept JSON input instead of form
    data = request.get_json()
    query = data.get("query", "")

    # Get matched questions from retrieval system
    matched_questions = search_query(query)
    context = "\n\n".join(
        f"Q: {item['question']}\nA: {item['answer']}" for item in matched_questions
    )

    # Prepare prompt for LLM
    system_prompt = "You're a tutor helping with JEE/NEET questions. Explain step-by-step how to approach the problem."
    final_prompt = f"Question: {query}\n\nRelated Examples:\n{context}\n\nStep-by-step solution:"

    # Get response from LLM
    llm_response = get_llama_response(prompt=final_prompt, system_prompt=system_prompt)

    # Return JSON response
    return jsonify({
        "response": llm_response,
        "matched": matched_questions
    })

if __name__ == "__main__":
    app.run(debug=True)
