import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import pickle
def build_faiss_index(csv_path="data/questions.csv", index_path="data/faiss_index.pkl"):
    # Load the CSV file
    df = pd.read_csv(csv_path)
    questions = df['questions'].tolist()

    #load the model
    model = SentenceTransformer('distilbert-base-nli-mean-tokens')

    # Create embeddings
    embeddings = np.array(model.encode(questions), dtype=np.float32)

    # Build FAISS index
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    # Save the index to a file
    with open(index_path, 'wb') as f:
        pickle.dump((index, df), f)
    print("Index built and saved")

if __name__ == "__main__":
    build_faiss_index()
    
print("hello world")