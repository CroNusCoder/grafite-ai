import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer, util
from config import INDEX_PATH, TOP_K

# Init model only once
model = SentenceTransformer('distilbert-base-nli-mean-tokens')

def is_similar(q1, q2):
    from difflib import SequenceMatcher
    return SequenceMatcher(None, q1.lower(), q2.lower()).ratio() > 0.92

def deduplicate(results):
    unique = []
    seen = []
    for r in results:
        if any(is_similar(r['question'], q) for q in seen):
            continue
        unique.append(r)
        seen.append(r['question'])
    return unique

def rerank(query, candidates):
    q_emb = model.encode(query, convert_to_tensor=True)
    c_embs = model.encode([c['question'] for c in candidates], convert_to_tensor=True)
    sims = util.cos_sim(q_emb, c_embs)[0]

    for i, sim in enumerate(sims):
        candidates[i]['score'] = float(sim)

    return sorted(candidates, key=lambda x: x['score'], reverse=True)

def search_query(query, top_k=TOP_K, rerank_top_k=5):
    # Load the FAISS index and DataFrame
    with open(INDEX_PATH, 'rb') as f:
        index, df = pickle.load(f)

    # Create the embedding for the query
    query_embedding = np.array([model.encode(query)], dtype=np.float32)

    # Search the index
    distances, indices = index.search(query_embedding, top_k)

    # Filter by distance score if needed (optional)
    results = []
    for dist, idx in zip(distances[0], indices[0]):
        row = df.iloc[idx]
        results.append({
            'question': row['questions'],
            'answer': row.get('answer', 'No answer available'),
            'distance': dist
        })

    # Deduplicate
    results = deduplicate(results)

    # Re-rank by semantic similarity
    results = rerank(query, results)

    return results[:rerank_top_k]
