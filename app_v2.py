import streamlit as st
import pickle
import re
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# -----------------------------
# 1. Page Configuration & CSS
# -----------------------------
st.set_page_config(page_title="ByteMind AI", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    flex-wrap: nowrap !important;
}

[data-testid="stSidebar"] button[kind="secondary"] p {
    font-size: 16px !important;
    display: block !important;
}

[data-testid="stSidebar"] [data-testid="column"] {
    min-width: unset !important;
    width: 50% !important;
}

html, body, [class*="css"], .stMarkdown { 
        font-family: 'Inter', sans-serif !important; 
    }

    .stCodeBlock { 
        background-color: transparent !important; 
        border: none !important; 
        padding: 0 !important; 
        margin-top: -10px !important; 
    }
    code { 
        color: #31333F !important; 
        background-color: transparent !important; 
        font-family: 'Inter', sans-serif !important; 
        font-size: 1.05rem !important; 
    }

    [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {
        align-items: center !important;
        gap: 0.5rem !important;
    }

    [data-testid="stSidebar"] .stButton button {
        height: 35px !important;
        padding: 0px 5px !important;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 8px !important;
        border: 1px solid #f0f2f6 !important;
        transition: all 0.3s;
    }

    [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] div:nth-child(2) button,
    [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] div:nth-child(3) button {
        font-size: 14px !important;
        width: 35px !important;
    }

    [data-testid="stSidebar"] .stButton button:active, 
    [data-testid="stSidebar"] .stButton button:focus {
        border-color: #ff4b4b !important;
        color: #ff4b4b !important;
    }
    
    </style>
    """, unsafe_allow_html=True)



# -----------------------------
# 2. Model Loading (Optimized for Space & Speed)
# -----------------------------
@st.cache_resource
def load_resources():

    model_id = "google/flan-t5-base" 
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

    embed_model = SentenceTransformer("all-MiniLM-L6-v2")

    with open("offline_index.pkl", "rb") as f:
        index_data = pickle.load(f)
        
    return tokenizer, model, embed_model, index_data

tokenizer, llm_model, embed_model, index_data = load_resources()

# -----------------------------
# 3. Session State
# -----------------------------
if "chats" not in st.session_state:
    st.session_state.chats = {"Main Chat": []}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Main Chat"
if "rename_mode" not in st.session_state:
    st.session_state.rename_mode = None

# -----------------------------
# 4. Helper Functions
# -----------------------------
def is_persian(text):
    return bool(re.search('[\u0600-\u06FF]', text))

def translate_logic(text, target_lang="en"):
    prefix = "translate Persian to English: " if target_lang == "en" else "translate English to Persian: "
    inputs = tokenizer(prefix + text, return_tensors="pt", truncation=True)
    outputs = llm_model.generate(**inputs, max_new_tokens=150, num_beams=4)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def get_greeting(text):
    greetings = ["سلام", "درود", "hi", "hello", "hey"]
    if any(word in text.lower() for word in greetings):
        return "سلام! خوشحالم که می‌بینمت. چطور می‌تونم کمکت کنم؟" if is_persian(text) else "Hello! I'm glad to see you. How can I help you today?"
    return None

# -----------------------------
# 5. Core RAG Logic
# -----------------------------
# -----------------------------
# Core RAG Logic (Updated for Strict Offline Mode)
# -----------------------------
def get_response(user_input):
    greeting = get_greeting(user_input)
    if greeting:
        return greeting, []

    is_fa = is_persian(user_input)
    working_query = translate_logic(user_input, "en") if is_fa else user_input
    sources = []

    if app_mode == "Computer Knowledge":
        query_emb = embed_model.encode([working_query])
        dist, idxs = index_data["nn"].kneighbors(query_emb, n_neighbors=1)

        if dist[0][0] > 0.75:
            msg = "Sorry, this topic is not in my computer database. Please try General Mode."
            return (translate_logic(msg, "fa") if is_fa else msg), []

        sources = []
        for i in idxs[0]:
            raw_text = index_data["documents"][i]
            clean_text = raw_text.replace("Answer:", "\n**Answer :**")
            sources.append(clean_text)

        context = index_data["documents"][idxs[0][0]]
        match = re.search(r"Answer\s*:?\s*(.*)", context, re.IGNORECASE | re.DOTALL)
        answer = match.group(1).strip() if match else context

    elif app_mode == "Hybrid Mode":
        query_emb = embed_model.encode([working_query])
        dist, idxs = index_data["nn"].kneighbors(query_emb, n_neighbors=2)
        context = "\n\n".join([index_data["documents"][i] for i in idxs[0]])
        sources = [index_data["documents"][i] for i in idxs[0]]

        prompt = f"""
                    You are a helpful AI assistant specialized in computer science and networking.

                    Use the context below to answer the question in a detailed, clear, and structured way.
                    Explain step by step whenever possible.
                    Include examples if they help understanding.
                    Do not give a short answer.

                    Context:
                    {context}

                    Question:
                    {working_query}

                    Detailed Answer:
                    """

        answer = generate_long_answer(prompt)

    else:  # General Knowledge
        prompt = f"""
                    You are a helpful AI assistant.

                    Answer the following question in a detailed, clear, and well-structured way.
                    Explain the topic step by step and provide examples where useful.
                    Do not give a short answer.

                    Question:
                    {working_query}

                    Detailed Answer:
                    """

        answer = generate_long_answer(prompt)

    if is_fa:
        answer = translate_logic(answer, "fa")

    return answer, sources

        
def generate_long_answer(prompt, max_new_tokens=300, min_new_tokens=80):
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    outputs = llm_model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        min_new_tokens=min_new_tokens,
        num_beams=4,
        length_penalty=1.2,
        no_repeat_ngram_size=3,
        early_stopping=True
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


# -----------------------------
# 6. Sidebar (Chat Management)
# -----------------------------
with st.sidebar:
    st.title("🧠 ByteMind")
    
    st.subheader("Settings")
    app_mode = st.radio("Select Mode", ["Computer Knowledge", "General Knowledge", "Hybrid Mode"])
    
    st.divider()

    st.subheader("New Chat")
    col_input, col_btn = st.columns([3, 1])
    with col_input:
        new_chat_name = st.text_input("Name", label_visibility="collapsed", key="new_chat_input", placeholder="New Chat...")
    with col_btn:
        if st.button("➕", use_container_width=True):
            if new_chat_name and new_chat_name not in st.session_state.chats:
                st.session_state.chats[new_chat_name] = []
                st.session_state.current_chat = new_chat_name
                st.rerun()

    st.subheader("Your History")
    
    chat_container = st.container()
    with chat_container:
        for chat_name in list(st.session_state.chats.keys()):
            col_name, col_edit, col_del = st.columns([4, 1, 1])
            
            with col_name:
                is_current = (chat_name == st.session_state.current_chat)
                button_label = f"💬 {chat_name}" if is_current else chat_name
                if st.button(button_label, key=f"select_{chat_name}", use_container_width=True):
                    st.session_state.current_chat = chat_name
                    st.rerun()
            
            with col_edit:
                if st.button("✏️", key=f"edit_{chat_name}"):
                    st.session_state.rename_mode = chat_name
            
            with col_del:
                if st.button("🗑️", key=f"del_{chat_name}"):
                    if len(st.session_state.chats) > 1:
                        del st.session_state.chats[chat_name]
                        st.session_state.current_chat = list(st.session_state.chats.keys())[0]
                    else:
                        st.session_state.chats = {"Main Chat": []}
                        st.session_state.current_chat = "Main Chat"
                    st.rerun()

    if st.session_state.rename_mode:
        st.info(f"Renaming: {st.session_state.rename_mode}")
        new_name = st.text_input("Enter new name:", key="rename_input")
        
        col_conf, col_canc = st.columns(2)
        with col_canc:
            # فقط ایموجی برای اشغال فضای کمتر
            if st.button("❌", use_container_width=True, help="Cancel"):
                st.session_state.rename_mode = None
                st.rerun()

# -----------------------------
# 7. Main Chat UI
# -----------------------------
st.title(f"💬 {st.session_state.current_chat}")

for msg in st.session_state.chats[st.session_state.current_chat]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask ByteMind..."):
    st.session_state.chats[st.session_state.current_chat].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            ans, srcs, tag = get_response(prompt)
            st.markdown(ans)
            st.caption(f"Response generated via: {tag}")

            if srcs:
                with st.expander("Reference Documents"):
                    for s in srcs: st.write(s)
            
            st.session_state.chats[st.session_state.current_chat].append({
                "role": "assistant", "content": ans, "sources": srcs, "tag": tag
            })