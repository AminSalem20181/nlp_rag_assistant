import json
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors

DATA_PATH = "offline_data.json"
INDEX_PATH = "offline_index.pkl"

print("Loading data...")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

documents = []
topics = []
metadata = []

for item in data:
    question = item.get("question", "")
    answer = item.get("answer", "")
    topic = item.get("topic", "general")

    # ساخت متن ترکیبی برای embedding
    combined_text = f"Question: {question}\nAnswer: {answer}"

    documents.append(combined_text)
    topics.append(topic)
    metadata.append(item)

print("Documents found:", len(documents))

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Generating embeddings...")
embeddings = model.encode(documents, show_progress_bar=True)
embeddings = np.array(embeddings)

print("Building semantic index...")
nn = NearestNeighbors(n_neighbors=5, metric="cosine")
nn.fit(embeddings)

print("Saving index...")

with open(INDEX_PATH, "wb") as f:
    pickle.dump({
        "nn": nn,
        "documents": documents,
        "topics": topics,
        "metadata": metadata
    }, f)

print("✅ Index built successfully")
