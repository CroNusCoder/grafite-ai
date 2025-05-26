import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, jsonify
from retrieval.search import search_query
from llm.groq_llama import get_llama_response
import numpy as np

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


import numpy as np
import numbers

def to_json_serializable(obj):
    if isinstance(obj, np.generic):
        return obj.item()  # Works for all numpy scalars (int, float, etc.)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: to_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_json_serializable(i) for i in obj]
    else:
        return obj


@app.route("/ask", methods=["POST"])
@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    query = data.get("query", "")

    matched_questions = search_query(query)
    context = "\n\n".join(
        f"Q: {item['question']}\nA: {item['answer']}" for item in matched_questions
    )

    system_prompt = "You're a tutor helping with JEE/NEET questions. Explain step-by-step how to approach the problem."
    final_prompt = f"Question: {query}\n\nRelated Examples:\n{context}\n\nStep-by-step solution:"

    llm_response = get_llama_response(prompt=final_prompt, system_prompt=system_prompt)

    return jsonify(to_json_serializable({
        "response": llm_response,
        "matched": matched_questions
    }))



if __name__ == "__main__":
    app.run(debug=True)