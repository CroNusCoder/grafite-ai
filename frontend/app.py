import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from retrieval.search import search_query  # <- Tumhara function import
from config import TOP_K

st.title("Grafite AI v2.0 — JEE/NEET Question Search")

# User query input
query = st.text_input("Enter your JEE/NEET question")

if query:
    st.write("Searching similar questions...")
    results = search_query(query, top_k=TOP_K)

    st.subheader("Top Results:")
    for i, match in enumerate(results, 1):
        st.markdown(f"**Top {i} Result:**")
        st.markdown(f"**Question:** {match['question']}")
        st.markdown(f"**Answer:** {match['answer'] if match['answer'] else 'No answer available'}")
