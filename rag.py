from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import pickle

from llama_cpp import Llama

# ================================
# LOAD LLM (GGUF)
# ================================
try:
    llm = Llama(
        model_path=r"D:\Gen-AI\qwen\qwen3-1.7b.Q4_K_M.gguf",
        n_ctx=2048,
        n_threads=6,
        verbose=False
    )
    print("LLM loaded successfully")
except Exception as e:
    print("LLM load error:", e)
    llm = None


# ================================
# EMBEDDING MODEL
# ================================
print("Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')


# ================================
# LOAD DOCUMENTS
# ================================
def load_documents():
    if os.path.exists("docs.txt"):
        with open("docs.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    return ["No documents found."]

documents = load_documents()


# ================================
# BUILD INDEX
# ================================
EMBED_FILE = "embeddings.pkl"

def build_or_load_index(documents):
    if os.path.exists(EMBED_FILE):
        print("Loading embeddings...")
        with open(EMBED_FILE, "rb") as f:
            doc_embeddings = pickle.load(f)
    else:
        print("Creating embeddings...")
        doc_embeddings = model.encode(
            documents,
            batch_size=32,
            normalize_embeddings=True
        ).astype("float32")

        with open(EMBED_FILE, "wb") as f:
            pickle.dump(doc_embeddings, f)

    index = faiss.IndexFlatIP(doc_embeddings.shape[1])
    index.add(doc_embeddings)

    return index

index = build_or_load_index(documents)


# ================================
# RETRIEVAL
# ================================
def retrieve(query, k=2):
    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    ).astype("float32")

    scores, indices = index.search(query_embedding, k)

    results = []
    for i, idx in enumerate(indices[0]):
        results.append({
            "text": documents[idx],
            "score": float(scores[0][i])
        })

    return results


# ================================
# CACHE
# ================================
cache = {}


# ================================
# LLM CALL
# ================================
def ask_llm(context, query):
    if llm is None:
        return "Model not loaded"

    try:
        prompt = f"""
Answer only using the context.
If the answer is not present, say: Not found.

Context:
{context[:800]}

Question: {query}
Answer:
"""

        output = llm(
            prompt,
            max_tokens=120,
            temperature=0.3,
            stop=["Question:", "Context:"]
        )

        return output["choices"][0]["text"].strip()

    except Exception as e:
        return f"Error: {str(e)}"


# ================================
# MAIN PIPELINE
# ================================
def rag_pipeline(query):
    if query in cache:
        return cache[query]

    results = retrieve(query)

    context = "\n".join([r["text"] for r in results])
    answer = ask_llm(context, query)

    sources = "\n".join([r["text"] for r in results])

    final = f"{answer}\n\nSources:\n{sources}"

    cache[query] = final
    return final