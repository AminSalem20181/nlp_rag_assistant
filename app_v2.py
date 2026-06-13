# import streamlit as st
# import pickle
# import re
# from sentence_transformers import SentenceTransformer
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# # -----------------------------
# # 1. Page Configuration & CSS
# # -----------------------------
# st.set_page_config(page_title="ByteMind AI", page_icon="🧠", layout="wide")

# st.markdown("""
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
#     [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {
#     display: flex !important;
#     flex-direction: row !important;
#     align-items: center !important;
#     flex-wrap: nowrap !important; /* جلوگیری از رفتن به خط بعد تحت هر شرایطی */
# }

# /* کوچک‌تر کردن دکمه‌های ایموجی‌دار برای جا شدن */
# [data-testid="stSidebar"] button[kind="secondary"] p {
#     font-size: 16px !important;
#     display: block !important;
# }

# /* حذف حاشیه اضافی ستون‌ها */
# [data-testid="stSidebar"] [data-testid="column"] {
#     min-width: unset !important;
#     width: 50% !important;
# }
#     /* فونت کلی برنامه */
#     html, body, [class*="css"], .stMarkdown { 
#         font-family: 'Inter', sans-serif !important; 
#     }

#     /* حذف حاشیه و رنگ پس‌زمینه بلاک‌های کد برای نمایش تمیز متن چت */
#     .stCodeBlock { 
#         background-color: transparent !important; 
#         border: none !important; 
#         padding: 0 !important; 
#         margin-top: -10px !important; 
#     }
#     code { 
#         color: #31333F !important; 
#         background-color: transparent !important; 
#         font-family: 'Inter', sans-serif !important; 
#         font-size: 1.05rem !important; 
#     }

#     /* --- اصلاح دکمه‌های سایدبار --- */
    
#     /* تراز کردن عمودی ستون‌ها در سایدبار */
#     [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {
#         align-items: center !important;
#         gap: 0.5rem !important; /* فاصله بین دکمه‌ها */
#     }

#     /* یکسان‌سازی ارتفاع و استایل همه دکمه‌های سایدبار */
#     [data-testid="stSidebar"] .stButton button {
#         height: 35px !important;
#         padding: 0px 5px !important;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         border-radius: 8px !important;
#         border: 1px solid #f0f2f6 !important;
#         transition: all 0.3s;
#     }

#     /* دکمه‌های آیکون‌دار (ویرایش و حذف) را کمی جمع‌وجورتر کنیم */
#     [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] div:nth-child(2) button,
#     [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] div:nth-child(3) button {
#         font-size: 14px !important;
#         width: 35px !important; /* مربع کردن دکمه‌های آیکون */
#     }

#     /* تغییر رنگ دکمه چت فعال */
#     [data-testid="stSidebar"] .stButton button:active, 
#     [data-testid="stSidebar"] .stButton button:focus {
#         border-color: #ff4b4b !important;
#         color: #ff4b4b !important;
#     }
    
#     </style>
#     """, unsafe_allow_html=True)


# # -----------------------------
# # 2. Model Loading
# # -----------------------------
# @st.cache_resource
# def load_resources():
#     tokenizer = AutoTokenizer.from_pretrained("./flan-t5-base-local")
#     model = AutoModelForSeq2SeqLM.from_pretrained("./flan-t5-base-local")
#     embed_model = SentenceTransformer("all-MiniLM-L6-v2")
#     with open("offline_index.pkl", "rb") as f:
#         index_data = pickle.load(f)
#     return tokenizer, model, embed_model, index_data

# tokenizer, llm_model, embed_model, index_data = load_resources()

# # -----------------------------
# # 3. Session State
# # -----------------------------
# if "chats" not in st.session_state:
#     st.session_state.chats = {"Main Chat": []}
# if "current_chat" not in st.session_state:
#     st.session_state.current_chat = "Main Chat"
# if "rename_mode" not in st.session_state:
#     st.session_state.rename_mode = None

# # -----------------------------
# # 4. Helper Functions (Translation & Greeting)
# # -----------------------------
# def is_persian(text):
#     return bool(re.search('[\u0600-\u06FF]', text))

# def translate_logic(text, target_lang="en"):
#     """استفاده از مدل برای ترجمه با پرامپت اصلاح شده برای جلوگیری از خروجی خالی"""
#     prefix = "translate Persian to English: " if target_lang == "en" else "translate English to Persian: "
#     inputs = tokenizer(prefix + text, return_tensors="pt", truncation=True)
#     outputs = llm_model.generate(**inputs, max_new_tokens=100, num_beams=4)
#     return tokenizer.decode(outputs[0], skip_special_tokens=True)

# def get_greeting(text):
#     greetings = ["سلام", "درود", "hi", "hello", "hey"]
#     if any(word in text.lower() for word in greetings):
#         return "سلام! خوشحالم که می‌بینمت. چطور می‌تونم کمکت کنم؟" if is_persian(text) else "Hello! I'm glad to see you. How can I help you today?"
#     return None

# # -----------------------------
# # 5. Core RAG Logic
# # -----------------------------
# # -----------------------------
# # Core RAG Logic (Updated for Strict Offline Mode)
# # -----------------------------

        
# def get_response(user_input):
#     greeting = get_greeting(user_input)
#     if greeting: return greeting, []

#     is_fa = is_persian(user_input)
#     working_query = translate_logic(user_input, "en") if is_fa else user_input

#     sources = []
    
#     if app_mode == "Computer Knowledge":
#         query_emb = embed_model.encode([working_query])
#         dist, idxs = index_data["nn"].kneighbors(query_emb, n_neighbors=1) # فقط نزدیک‌ترین سند
        
#         if dist[0][0] > 0.75: # عدد را کمی کمتر کردیم تا حساس‌تر شود
#             msg = "Sorry, this topic is not in my computer database. Please try General Mode."
#             return (translate_logic(msg, "fa") if is_fa else msg), []
        

#         sources = []
#         for i in idxs[0]:
#             raw_text = index_data["documents"][i]
#             clean_text = raw_text.replace("Answer:", "\n**Answer :**")
#             sources.append(clean_text)
        
        
#         context = index_data["documents"][idxs[0][0]]

#         match = re.search(r"Answer\s*:?\s*(.*)", context, re.IGNORECASE | re.DOTALL)

#         if match:
#             answer = match.group(1).strip()
#         else:
#             msg = "I couldn't find a clear answer in the database."
#             return (translate_logic(msg, "fa") if is_fa else msg), []

#         if "NOT_FOUND" in answer or len(answer) < 5:
#             msg = "I couldn't find a clear answer in the database."
#             return (translate_logic(msg, "fa") if is_fa else msg), []

#     elif app_mode == "Hybrid Mode":
#         # ترکیبی (مثل قبل)
#         query_emb = embed_model.encode([working_query])
#         dist, idxs = index_data["nn"].kneighbors(query_emb, n_neighbors=2)
#         context = "\n".join([index_data["documents"][i] for i in idxs[0]])
#         sources = [index_data["documents"][i] for i in idxs[0]]
#         prompt = f"Context: {context}\nQuestion: {working_query}\nAnswer:"
#         inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
#         outputs = llm_model.generate(**inputs, max_new_tokens=250)
#         answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
#     else: # General Mode
#         prompt = f"Answer this question: {working_query}"
#         inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
#         outputs = llm_model.generate(**inputs, max_new_tokens=250)
#         answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

#     if is_fa:
#         answer = translate_logic(answer, "fa")
    
#     return answer, sources


# # -----------------------------
# # 6. Sidebar (Chat Management)
# # -----------------------------
# # -----------------------------
# # 6. Sidebar (Chat Management & Settings)
# # -----------------------------
# with st.sidebar:
#     st.title("🧠 ByteMind")
    
#     # --- بخش تنظیمات (همیشه بالا می‌ماند) ---
#     st.subheader("Settings")
#     app_mode = st.radio("Select Mode", ["Computer Knowledge", "General Knowledge", "Hybrid Mode"])
    
#     st.divider()

#     # --- بخش ایجاد چت جدید ---
#     st.subheader("New Chat")
#     col_input, col_btn = st.columns([3, 1])
    
#     with col_input:
#         new_chat_name = st.text_input("Name", label_visibility="collapsed", key="new_chat_input", placeholder="Chat Name...")
    
#     with col_btn:
#         if st.button("➕", key="create_btn", use_container_width=True):
#             if new_chat_name and new_chat_name not in st.session_state.chats:
#                 st.session_state.chats[new_chat_name] = []
#                 st.session_state.current_chat = new_chat_name
#                 st.rerun()

#     # --- بخش لیست چت‌ها (این بخش می‌تواند طولانی شود و اسکرول بخورد) ---
#     st.subheader("Your History")
    
#     # برای زیباتر شدن، لیست چت‌ها را در یک کانتینر قرار می‌دهیم
#     chat_container = st.container()
#     with chat_container:
#         for chat_name in list(st.session_state.chats.keys()):
#             col_name, col_edit, col_del = st.columns([4, 1, 1])
            
#             with col_name:
#                 # هایلایت کردن چت فعلی با استفاده از استایل دکمه
#                 is_current = (chat_name == st.session_state.current_chat)
#                 button_label = f"💬 {chat_name}" if is_current else chat_name
#                 if st.button(button_label, key=f"select_{chat_name}", use_container_width=True):
#                     st.session_state.current_chat = chat_name
#                     st.rerun()
            
#             with col_edit:
#                 if st.button("✏️", key=f"edit_{chat_name}"):
#                     st.session_state.rename_mode = chat_name
            
#             with col_del:
#                 if st.button("🗑️", key=f"del_{chat_name}"):
#                     if len(st.session_state.chats) > 1:
#                         del st.session_state.chats[chat_name]
#                         st.session_state.current_chat = list(st.session_state.chats.keys())[0]
#                     else:
#                         st.session_state.chats = {"Main Chat": []}
#                         st.session_state.current_chat = "Main Chat"
#                     st.rerun()

#     # --- بخش تغییر نام (فقط وقتی فعال شود ظاهر می‌شود) ---
#     if st.session_state.rename_mode:
#         st.info(f"Renaming: {st.session_state.rename_mode}")
#         new_name = st.text_input("Enter new name:", key="rename_input")
        
#         # استفاده از ستون‌های برابر برای فضای کافی
#         col_conf, col_canc = st.columns(2)
#         with col_canc:
#             # فقط ایموجی برای اشغال فضای کمتر
#             if st.button("❌", use_container_width=True, help="Cancel"):
#                 st.session_state.rename_mode = None
#                 st.rerun()

#         with col_conf:
#             if st.button("✅", use_container_width=True, help="Confirm"):
#                 if new_name and new_name not in st.session_state.chats:
#                     st.session_state.chats[new_name] = st.session_state.chats.pop(st.session_state.rename_mode)
#                     st.session_state.current_chat = new_name
#                     st.session_state.rename_mode = None
#                     st.rerun()

        
# # -----------------------------
# # 7. Main Chat UI
# # -----------------------------
# st.title(f"💬 {st.session_state.current_chat}")

# # Display History
# for msg in st.session_state.chats[st.session_state.current_chat]:
#     with st.chat_message(msg["role"]):
#         st.code(msg["content"], language=None)

# # Chat Input
# if prompt := st.chat_input("Ask me anything..."):
#     st.session_state.chats[st.session_state.current_chat].append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.code(prompt, language=None)

#     with st.chat_message("assistant"):
#         with st.spinner("Processing..."):
#             ans, srcs = get_response(prompt)
#             st.write(ans)

#             if app_mode == "Computer Knowledge" and srcs:
#                 with st.expander("Sources"):
#                     for s in srcs: st.write(s)
            
#             st.session_state.chats[st.session_state.current_chat].append({
#                 "role": "assistant", "content": ans, "sources": srcs
#             })


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
    flex-wrap: nowrap !important; /* جلوگیری از رفتن به خط بعد تحت هر شرایطی */
}

/* کوچک‌تر کردن دکمه‌های ایموجی‌دار برای جا شدن */
[data-testid="stSidebar"] button[kind="secondary"] p {
    font-size: 16px !important;
    display: block !important;
}

/* حذف حاشیه اضافی ستون‌ها */
[data-testid="stSidebar"] [data-testid="column"] {
    min-width: unset !important;
    width: 50% !important;
}
    /* فونت کلی برنامه */
    html, body, [class*="css"], .stMarkdown { 
        font-family: 'Inter', sans-serif !important; 
    }

    /* حذف حاشیه و رنگ پس‌زمینه بلاک‌های کد برای نمایش تمیز متن چت */
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

    /* --- اصلاح دکمه‌های سایدبار --- */
    
    /* تراز کردن عمودی ستون‌ها در سایدبار */
    [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {
        align-items: center !important;
        gap: 0.5rem !important; /* فاصله بین دکمه‌ها */
    }

    /* یکسان‌سازی ارتفاع و استایل همه دکمه‌های سایدبار */
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

    /* دکمه‌های آیکون‌دار (ویرایش و حذف) را کمی جمع‌وجورتر کنیم */
    [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] div:nth-child(2) button,
    [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] div:nth-child(3) button {
        font-size: 14px !important;
        width: 35px !important; /* مربع کردن دکمه‌های آیکون */
    }

    /* تغییر رنگ دکمه چت فعال */
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
    # استفاده از مدل آنلاین (کش شده) برای جلوگیری از اشغال فضای دوبرابری
    # اگر سیستمت ضعیف است فلان-تی5-اسمال بگذار، اگر اوکی هست بیس بماند
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
def get_response(user_input):
    greeting = get_greeting(user_input)
    if greeting: return greeting, [], "Greeting"

    is_fa = is_persian(user_input)
    working_query = translate_logic(user_input, "en") if is_fa else user_input
    sources = []
    source_tag = app_mode

    if app_mode == "Computer Knowledge":
        query_emb = embed_model.encode([working_query])
        # افزایش n_neighbors برای دقت بیشتر طبق لاگ‌های قبلی
        dist, idxs = index_data["nn"].kneighbors(query_emb, n_neighbors=1)
        
        if dist[0][0] > 0.85: 
            msg = "Sorry, this topic is not in my specialized database. Try General Mode."
            return (translate_logic(msg, "fa") if is_fa else msg), [], "Not Found"

        sources = []
        for i in idxs[0]:
            raw_text = index_data["documents"][i]
            clean_text = raw_text.replace("Answer:", "\n**Answer :**")
            sources.append(clean_text)
        context = index_data["documents"][idxs[0][0]]
        
        # استخراج مستقیم پاسخ با Regex برای جلوگیری از هذیان مدل
        match = re.search(r"Answer\s*:?\s*(.*)", context, re.IGNORECASE | re.DOTALL)
        answer = match.group(1).strip() if match else context

    elif app_mode == "Hybrid Mode":
        query_emb = embed_model.encode([working_query])
        dist, idxs = index_data["nn"].kneighbors(query_emb, n_neighbors=2)
        context = "\n".join([index_data["documents"][i] for i in idxs[0]])
        sources = [index_data["documents"][i] for i in idxs[0]]
        
        prompt = f"Context: {context}\nQuestion: {working_query}\nAnswer:"
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
        outputs = llm_model.generate(**inputs, max_new_tokens=250)
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    else: # General Mode
        prompt = f"Provide a detailed answer to: {working_query}"
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
        outputs = llm_model.generate(**inputs, max_new_tokens=250)
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    if is_fa:
        answer = translate_logic(answer, "fa")
    
    return answer, sources, source_tag

# -----------------------------
# 6. Sidebar (Chat Management)
# -----------------------------
with st.sidebar:
    st.title("🧠 ByteMind")
    
    app_mode = st.radio("Search Mode", ["Computer Knowledge", "General Knowledge", "Hybrid Mode"])
    st.divider()

    # New Chat
    col_input, col_btn = st.columns([3, 1])
    with col_input:
        new_chat_name = st.text_input("Name", label_visibility="collapsed", key="new_chat_input", placeholder="New Chat...")
    with col_btn:
        if st.button("➕", use_container_width=True):
            if new_chat_name and new_chat_name not in st.session_state.chats:
                st.session_state.chats[new_chat_name] = []
                st.session_state.current_chat = new_chat_name
                st.rerun()

    st.subheader("History")
    for chat_name in list(st.session_state.chats.keys()):
        c1, c2, c3 = st.columns([4, 1, 1])
        with c1:
            label = f"💬 {chat_name}" if chat_name == st.session_state.current_chat else chat_name
            if st.button(label, key=f"sel_{chat_name}", use_container_width=True):
                st.session_state.current_chat = chat_name
                st.rerun()
        with c2:
            if st.button("✏️", key=f"ed_{chat_name}"):
                st.session_state.rename_mode = chat_name
        with c3:
            if st.button("🗑️", key=f"dl_{chat_name}"):
                if len(st.session_state.chats) > 1:
                    del st.session_state.chats[chat_name]
                    st.session_state.current_chat = list(st.session_state.chats.keys())[0]
                else:
                    st.session_state.chats = {"Main Chat": []}
                st.rerun()

    if st.session_state.rename_mode:
        new_name = st.text_input("New name for " + st.session_state.rename_mode)
        if st.button("Confirm Rename"):
            if new_name:
                st.session_state.chats[new_name] = st.session_state.chats.pop(st.session_state.rename_mode)
                st.session_state.current_chat = new_name
                st.session_state.rename_mode = None
                st.rerun()

# -----------------------------
# 7. Main Chat UI
# -----------------------------
st.title(f"💬 {st.session_state.current_chat}")

# نمایش تاریخچه چت با Markdown (بسیار تمیزتر از کد بلاک)
for msg in st.session_state.chats[st.session_state.current_chat]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "tag" in msg and msg["tag"]:
            st.caption(f"Source Mode: {msg['tag']}")

# ورودی چت
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