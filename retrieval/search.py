import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
from config import INDEX_PATH, TOP_K

def search_query(query, top_k=TOP_K):
    # Load the FAISS index and DataFrame
    with open(INDEX_PATH, 'rb') as f:
        index, df = pickle.load(f)

    # Load the model
    model = SentenceTransformer('distilbert-base-nli-mean-tokens')

    # Create the embedding for the query
    query_embedding = np.array([model.encode(query)], dtype=np.float32)

    # Search the index
    distances, indices = index.search(query_embedding, top_k)

    #Fetch matching ques and show
    results = []
    for idx in indices[0]:
        row = df.iloc[idx]
        results.append({
            'question': row['questions'],
            'answer': row.get('answer', 'No answer available')
        })
    
    return results
if __name__ == "__main__":
    query = input("Enter your JEE/NEET question: ")
    matches = search_query(query)
    for i, match in enumerate(matches, 1):
        print(f"\nTop {i} result:")
        print(f"Question: {match['question']}")
        print(f"Answer: {match['answer']}")