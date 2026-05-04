import os
import pickle
import numpy as np
import pandas as pd
import ollama
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

EXCEL_FILES = [
    os.path.join("Files", "General_Security_Practices.xlsx"),
    os.path.join("Files", "Device_Configuration.xlsx"),
    os.path.join("Files", "Permissions_Risk_Data.xlsx"),
    os.path.join("Files", "Social_Media_Security.xlsx"),
    os.path.join("Files", "step_by_step_fix.xlsx"),
]

EMBED_MODEL = "mxbai-embed-large"
LLM_MODEL = "gemma3:4b"
TOP_K = 5
VECTOR_STORE_FILE = "vector_store.pkl"

documents = []
embeddings = []


def load_data():
    print("Loading data...")
    rows = []
    script_dir = os.path.dirname(os.path.abspath(__file__))
    for fname in EXCEL_FILES:
        fpath = os.path.join(script_dir, fname)
        if not os.path.exists(fpath):
            print(f"  [WARNING] File not found, skipping: {fpath}")
            continue
        try:
            df = pd.read_excel(fpath, dtype=str)
            df.fillna("", inplace=True)
            source = os.path.splitext(fname)[0]
            for _, row in df.iterrows():
                parts = []
                for col in df.columns:
                    val = str(row[col]).strip()
                    if val:
                        parts.append(f"{col}: {val}")
                if parts:
                    text = f"[Source: {source}] " + " | ".join(parts)
                    rows.append(text)
            print(f"  Loaded {len(df)} rows from {fname}")
        except Exception as e:
            print(f"  [ERROR] Could not read {fname}: {e}")
    return rows


def get_embedding(text: str) -> np.ndarray:
    response = ollama.embeddings(model=EMBED_MODEL, prompt=text)
    return np.array(response["embedding"], dtype=np.float32)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def retrieve(query: str, top_k: int = TOP_K):
    query_emb = get_embedding(query)
    scores = [cosine_similarity(query_emb, emb) for emb in embeddings]
    top_indices = np.argsort(scores)[::-1][:top_k]
    return [documents[i] for i in top_indices]


def generate_answer(query: str, context_docs: list) -> str:
    if query.lower().strip() in ["hi", "hello", "hey"]:
        return "Hello"

    context = "\n".join(f"- {doc}" for doc in context_docs)
    prompt = f"""You are a helpful mobile security AI.
Using ONLY the context below, answer the user's question.

CORE BEHAVIOR RULES:
1. Be polite, clear, and explain concepts in a nice, easy-to-understand way IF the user asks for an explanation.
2. If asked "how to fix" or "what to do", provide accurate step-by-step actions based on the context (e.g., "Go to Settings > ..."). If the user specifies an app like WhatsApp, apply the specific steps for that app.
3. If asked "is this risky?", reply directly with "Yes, High risk", "Medium risk", or "Low risk", and give a brief reason.
4. Keep answers concise (3-5 lines) UNLESS the user explicitly asks for a detailed explanation.
5. Prioritize HIGH risk issues from the dataset and focus on practical fixes.
6. NEVER output markdown code blocks.

Context:
{context}

User Question: {query}

Answer:"""

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response["message"]["content"].strip()


def load_vector_store():
    if os.path.exists(VECTOR_STORE_FILE):
        print(f"Loading vector store from {VECTOR_STORE_FILE}...")
        try:
            with open(VECTOR_STORE_FILE, "rb") as f:
                data = pickle.load(f)
            return data["documents"], data["embeddings"]
        except Exception as e:
            print(f"  [ERROR] Failed to load vector store: {e}")
    return None, None


def save_vector_store(docs, embs):
    print(f"Saving vector store to {VECTOR_STORE_FILE}...")
    try:
        with open(VECTOR_STORE_FILE, "wb") as f:
            pickle.dump({"documents": docs, "embeddings": embs}, f)
        print("  Saved successfully.")
    except Exception as e:
        print(f"  [ERROR] Failed to save vector store: {e}")


def main():
    global documents, embeddings

    loaded_docs, loaded_embs = load_vector_store()
    if loaded_docs is not None and loaded_embs is not None:
        documents = loaded_docs
        embeddings = loaded_embs
        print(f"  Loaded {len(documents)} documents from vector store.")
    else:
        documents = load_data()
        if not documents:
            print("[ERROR] No documents loaded. Please ensure Excel files are in the same folder.")
            return

        print(f"Creating embeddings for {len(documents)} documents...")
        embeddings = []
        for i, doc in enumerate(documents):
            try:
                emb = get_embedding(doc)
                embeddings.append(emb)
                if (i + 1) % 10 == 0 or (i + 1) == len(documents):
                    print(f"  Embedded {i + 1}/{len(documents)}", end="\r")
            except Exception as e:
                print(f"\n  [ERROR] Failed to embed document {i}: {e}")
                embeddings.append(np.zeros(1024, dtype=np.float32))
        
        print()
        save_vector_store(documents, embeddings)

    print(f"\nChatbot ready. Type 'exit' to quit.\n")

    while True:
        try:
            query = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not query:
            print("Bot: Please enter a question.\n")
            continue

        if query.lower() == "exit":
            print("Goodbye!")
            break

        try:
            if query.lower() in ["hi", "hello", "hey"]:
                print(f"\nBot: Hello\n")
                continue

            relevant_docs = retrieve(query)
            answer = generate_answer(query, relevant_docs)
            print(f"\nBot: {answer}\n")
        except Exception as e:
            print(f"Bot: [ERROR] Something went wrong: {e}\n")


# ==========================================
# DASHBOARD-AWARE API INTEGRATION
# ==========================================

app = FastAPI()

class ChatRequest(BaseModel):
    query: str
    dashboard_context: dict

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    global documents, embeddings
    
    # Auto-load the vector store quietly if the API boots before terminal
    if not documents:
        loaded_docs, loaded_embs = load_vector_store()
        if loaded_docs is not None and loaded_embs is not None:
            documents = loaded_docs
            embeddings = loaded_embs

    user_query = request.query
    context = request.dashboard_context
    risk_level = context.get('risk_level', 'Unknown')
    total_score = context.get('total_score', 0)
    category_scores = context.get('category_scores', {})
    
    # 1. Retrieve classic RAG context
    if documents:
        relevant_docs = retrieve(user_query)
    else:
        relevant_docs = []
        
    rag_context = "\n".join(f"- {doc}" for doc in relevant_docs)
    
    # 2. Strict RAG System Prompt injecting live state
    prompt = f"""You are a helpful mobile privacy AI Assistant.
Using ONLY the RAG Context Data below, answer the user's question directly.

CURRENT USER DASHBOARD RISK PROFILE:
- Risk Level: {risk_level}
- Risk Score: {total_score}/60
- Category Breakdown: {category_scores}

CORE BEHAVIOR RULES:
1. Using ONLY the RAG Context below, answer the user's question. DO NOT invent information.
2. If asked "how to fix" or "what to do", provide accurate step-by-step actions strictly based on the RAG context.
3. You MUST provide detailed reasoning and specific data from the Context when answering.
4. If asked "is this risky?", reply directly and give a reason based on the context.
5. Mention the user's highest risk category from their Dashboard Profile briefly in your response.
6. NEVER output markdown code blocks.
7. If the answer is not in the context, say "I don't have enough data on that in my knowledge base."

RAG Context Data (Extracted from Excel logs):
{rag_context}

User Question: {user_query}

Answer:"""

    try:
        response = ollama.chat(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        return {"response": response["message"]["content"].strip()}
    except Exception as e:
        return {"response": f"⚠️ Privacy AI Offline: Cannot connect to Ollama engine. Please ensure the Ollama app is actively running on your PC. (Error: {str(e)})"}


if __name__ == "__main__":
    import sys
    print("Welcome to Privacy Sentinel AI Core!")
    print("Run `python rag_file.py --terminal` for local CLI chat.")
    print("Booting Dashboard API Server by default...")
    
    if len(sys.argv) > 1 and sys.argv[1] == "--terminal":
        main()
    else:
        # Pre-load memory before boot
        documents, embeddings = load_vector_store()
        uvicorn.run(app, host="0.0.0.0", port=8000)
