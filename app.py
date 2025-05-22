from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import streamlit as st

# Load model
model = SentenceTransformer('distilbert-base-nli-mean-tokens')

# Sample JEE/NEET questions
questions = [
    "What is the value of g on the surface of Mars?",
    "Find the derivative of sin(x) + cos(x)",
    "How to find the focal length of a convex lens?",
    "Explain the Bohr model of atom",
    "What is the difference between mitosis and meiosis?"
]

# Create embeddings
embeddings = model.encode(questions)

# Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

# Streamlit UI
st.title("GrafiteAI - JEE/NEET Question Helper")
query = st.text_input("Enter your question:")

if query:
    q_embedding = model.encode([query])
    D, I = index.search(np.array(q_embedding), k=1)
    st.subheader("Most Similar Question Found:")
    st.write(questions[I[0][0]])
