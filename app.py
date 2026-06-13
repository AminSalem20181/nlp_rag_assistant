import os
import json
import uuid
import pickle
import faiss
import torch
import streamlit as st
import numpy as np

from sentence_transformers import SentenceTransformer
from transformers import T5Tokenizer, T5ForConditionalGeneration

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="NLP RAG Assistant",
    page_icon="🧠",
    layout="wide"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #0f1117;
    color: #f5f5f5;
    font-family: 'Segoe UI', sans-serif;
}

.main-title {
    text-align: center;
    color: #f0c674;
    font-size: 2.4rem;
    font-weight: 700;
    margin-bottom: 0.3rem;
}

.sub-title {
    text-align: center;
    color: #bbbbbb;
    font-size: 1rem;
    margin-bottom: 1.5rem;
}

.chat-user {
    background: #1e2a38;
    padding: 14px;
    border-radius: 14px;
    margin: 10px 0;
    border-left: 5px solid #5dade2;
}

.chat-bot {
    background: #1a1f2b;
    padding: 14px;
    border-radius: 14px;
    margin: 10px 0;
    border-left: 5px solid #f0c674;
}

.badge {
    display: inline-block;
    padding: 0.25rem 0.55rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 700;
    margin-top: 0.6rem;
    color: #111;
    background-color: #f0c674;
}

.sidebar-title {
    color: #f0c674;
    font-size: 1.1rem;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Config
# -----------------------------
ONLINE_INDEX_FILE = "faiss_index.bin"
ONLINE_DOCS_FILE = "documents.pkl"

OFFLINE_INDEX_FILE = "offline_faiss_index.bin"
OFFLINE_DOCS_FILE = "offline_documents.pkl"

EMBED_MODEL_NAME = "all-MiniLM-L6-v2"

MODEL_OPTIONS = {
    "FLAN-T5 Base": "google/flan-t5-base",
    "FLAN-T5 Large": "google/flan-t5-large"
}

# -----------------------------
# Cached resources
# -----------------------------
@st.cache_resource
def load_embedder():
    return SentenceTransformer(EMBED_MODEL_NAME)


@st.cache_resource
def load_generator(model_name):
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    return tokenizer, model


@st.cache_resource
def load_online_index_and_docs():
    if not os.path.exists(ONLINE_INDEX_FILE) or not os.path.exists(ONLINE_DOCS_FILE):
        return None, []
    index = faiss.read_index(ONLINE_INDEX_FILE)
    with open(ONLINE_DOCS_FILE, "rb") as f:
        docs = pickle.load(f)
    return index, docs


@st.cache_resource
def load_offline_index_and_docs():
    if not os.path.exists(OFFLINE_INDEX_FILE) or not os.path.exists(OFFLINE_DOCS_FILE):
        return None, []
    index = faiss.read_index(OFFLINE_INDEX_FILE)
    with open(OFFLINE_DOCS_FILE, "rb") as f:
        docs = pickle.load(f)
    return index, docs


# -----------------------------
# Search functions
# -----------------------------
def semantic_search_online(query, embedder, index, docs, top_k=3):
    if index is None or not docs:
        return []

    query_embedding = embedder.encode([query], convert_to_numpy=True).astype("float32")
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for idx in indices[0]:
        if 0 <= idx < len(docs):
            results.append(docs[idx])
    return results


def semantic_search_offline(query, embedder, index, docs, top_k=3):
    if index is None or not docs:
        return []

    query_embedding = embedder.encode([query], convert_to_numpy=True).astype("float32")
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for rank, idx in enumerate(indices[0]):
        if 0 <= idx < len(docs):
            item = docs[idx].copy()
            item["rank"] = rank + 1
            results.append(item)
    return results


# -----------------------------
# Answer generation
# -----------------------------
def build_prompt(context, question):
    return f"""
You are a helpful AI assistant.
Use the context below to answer the question accurately and clearly.

Context:
{context}

Question:
{question}

Answer:
""".strip()


def generate_answer(question, retrieved_docs, tokenizer, model):
    if not retrieved_docs:
        return "I could not find enough relevant online information to answer your question."

    context = "\n\n".join([doc["text"] for doc in retrieved_docs[:3]])
    prompt = build_prompt(context, question)

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=1024
    )

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=220,
            temperature=0.7,
            top_p=0.95,
            do_sample=True
        )

    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer.strip()


# -----------------------------
# Session state
# -----------------------------
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat_id" not in st.session_state:
    new_id = str(uuid.uuid4())
    st.session_state.chats[new_id] = {
        "title": "New Chat",
        "messages": []
    }
    st.session_state.current_chat_id = new_id


def create_new_chat():
    new_id = str(uuid.uuid4())
    st.session_state.chats[new_id] = {
        "title": "New Chat",
        "messages": []
    }
    st.session_state.current_chat_id = new_id


def delete_chat(chat_id):
    if chat_id in st.session_state.chats:
        del st.session_state.chats[chat_id]

        if not st.session_state.chats:
            create_new_chat()
        else:
            st.session_state.current_chat_id = next(iter(st.session_state.chats.keys()))


current_chat = st.session_state.chats[st.session_state.current_chat_id]

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-title">⚙️ Control Panel</div>', unsafe_allow_html=True)

    selected_model_label = st.selectbox(
        "Choose generation model",
        list(MODEL_OPTIONS.keys())
    )
    selected_model_name = MODEL_OPTIONS[selected_model_label]

    st.markdown("---")
    st.markdown('<div class="sidebar-title">💬 Chat Sessions</div>', unsafe_allow_html=True)

    if st.button("➕ New Chat"):
        create_new_chat()
        st.rerun()

    for chat_id, chat_data in list(st.session_state.chats.items()):
        col1, col2 = st.columns([4, 1])

        with col1:
            if st.button(chat_data["title"], key=f"chat_{chat_id}"):
                st.session_state.current_chat_id = chat_id
                st.rerun()

        with col2:
            if st.button("🗑️", key=f"delete_{chat_id}"):
                delete_chat(chat_id)
                st.rerun()

# -----------------------------
# Load resources
# -----------------------------
embedder = load_embedder()
tokenizer, model = load_generator(selected_model_name)

online_index, online_docs = load_online_index_and_docs()
offline_index, offline_docs = load_offline_index_and_docs()

# -----------------------------
# Header
# -----------------------------
st.markdown('<div class="main-title">🧠 NLP RAG Assistant</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Online + Offline Retrieval | Multi-Model | Chat Sessions</div>',
    unsafe_allow_html=True
)

# -----------------------------
# Display old messages
# -----------------------------
for msg in current_chat["messages"]:
    if msg["role"] == "user":
        st.markdown(
            f'<div class="chat-user"><b>👤 You:</b><br>{msg["content"]}</div>',
            unsafe_allow_html=True
        )
    else:
        badge = msg.get("model_used", "Unknown Source")
        st.markdown(
            f'<div class="chat-bot"><b>🤖 Assistant:</b><br>{msg["content"]}<br>'
            f'<span class="badge">{badge}</span></div>',
            unsafe_allow_html=True
        )

# -----------------------------
# User input
# -----------------------------
query = st.chat_input("Ask me anything about NLP, ML, networking, databases, OS, security...")

if query:
    if current_chat["title"] == "New Chat":
        current_chat["title"] = query[:30] + ("..." if len(query) > 30 else "")

    current_chat["messages"].append({
        "role": "user",
        "content": query
    })

    st.markdown(
        f'<div class="chat-user"><b>👤 You:</b><br>{query}</div>',
        unsafe_allow_html=True
    )

    with st.spinner("Accessing knowledge sources..."):
        try:
            # Online retrieval
            online_results = semantic_search_online(
                query, embedder, online_index, online_docs, top_k=3
            )
            online_answer = generate_answer(
                query, online_results, tokenizer, model
            )

            # Offline retrieval
            offline_results = semantic_search_offline(
                query, embedder, offline_index, offline_docs, top_k=3
            )

            has_online = len(online_results) > 0
            has_offline = len(offline_results) > 0

            if has_online and has_offline:
                st.info("Two answer sources are available. Choose which answer to save in chat history.")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("### 🌐 Online Model Answer")
                    st.write(online_answer)
                    st.caption(f"Model: {selected_model_label}")

                    if st.button("Use Online Answer", key=f"use_online_{len(current_chat['messages'])}"):
                        current_chat["messages"].append({
                            "role": "assistant",
                            "content": online_answer,
                            "model_used": selected_model_label
                        })
                        st.rerun()

                with col2:
                    best_offline = offline_results[0]
                    st.markdown("### 💾 Offline Knowledge Answer")
                    st.write(best_offline["answer"])
                    st.caption(
                        f"Topic: {best_offline['topic']} | "
                        f"Concept: {best_offline['concept']} | "
                        f"Difficulty: {best_offline['difficulty']}"
                    )

                    if st.button("Use Offline Answer", key=f"use_offline_{len(current_chat['messages'])}"):
                        current_chat["messages"].append({
                            "role": "assistant",
                            "content": best_offline["answer"],
                            "model_used": f"Offline DB | {best_offline['topic']} | {best_offline['concept']}"
                        })
                        st.rerun()

                with st.expander("Show Offline Matches"):
                    for i, item in enumerate(offline_results, 1):
                        st.markdown(f"**Match {i}**")
                        st.write(f"**Question:** {item['question']}")
                        st.write(f"**Answer:** {item['answer']}")
                        st.write(f"**Topic:** {item['topic']}")
                        st.write(f"**Concept:** {item['concept']}")
                        st.write(f"**Difficulty:** {item['difficulty']}")
                        st.write(f"**Tags:** {', '.join(item['tags'])}")
                        st.write(f"**Source:** {item['source']}")
                        st.write("---")

                with st.expander("Show Online Context"):
                    for i, doc in enumerate(online_results, 1):
                        st.markdown(f"**Document {i}**")
                        st.write(f"**Topic:** {doc.get('topic', 'unknown')}")
                        st.write(doc.get("text", ""))
                        st.write("---")

            elif has_offline:
                best_offline = offline_results[0]
                answer = best_offline["answer"]

                current_chat["messages"].append({
                    "role": "assistant",
                    "content": answer,
                    "model_used": f"Offline DB | {best_offline['topic']} | {best_offline['concept']}"
                })
                st.rerun()

            elif has_online:
                current_chat["messages"].append({
                    "role": "assistant",
                    "content": online_answer,
                    "model_used": selected_model_label
                })
                st.rerun()

            else:
                fallback = "I could not find a relevant answer in either the online or offline knowledge base."
                current_chat["messages"].append({
                    "role": "assistant",
                    "content": fallback,
                    "model_used": "No Source"
                })
                st.rerun()

        except Exception as e:
            st.error(f"SYSTEM_EXCEPTION: {str(e)}")
