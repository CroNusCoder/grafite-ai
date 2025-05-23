import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# sahi path set karo yahan
INDEX_PATH = os.path.join(BASE_DIR, "data", "faiss_index.pkl")
CSV_PATH = os.path.join(BASE_DIR, "data", "questions.csv")

TOP_K = 3
