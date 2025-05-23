import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import pickle
from config import CSV_PATH, INDEX_PATH
def build_faiss_index():
    # Load the CSV file
    df = pd.read_csv(CSV_PATH)
    questions = df['questions'].tolist()

    #load the model
    model = SentenceTransformer('distilbert-base-nli-mean-tokens')

    # Create embeddings
    embeddings = np.array(model.encode(questions), dtype=np.float32)

    # Build FAISS index
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings) #type: ignore

    # Save the index to a file
    with open(INDEX_PATH, 'wb') as f:
        pickle.dump((index, df), f)
    print("Index built and saved")

if __name__ == "__main__":
    build_faiss_index() #type: ignore
    
print("hello world")