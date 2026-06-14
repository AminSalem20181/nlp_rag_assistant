# 🧠 ByteMind AI: Hybrid RAG-Based Intelligent Assistant

ByteMind is a smart, localized AI assistant designed to deliver accurate, context-aware technical answers in Computer Science and Networking while maintaining strong general conversational capabilities. It combines **Retrieval-Augmented Generation (RAG)** with a lightweight Large Language Model (**Flan-T5**) to ensure both precision and flexibility.

---

## 🚀 Key Features

* 🔍 **Computer Knowledge Mode (Strict RAG):** Retrieves verified answers directly from a local technical database using strict similarity thresholds.
* 🌐 **General Knowledge Mode (LLM-Based):** Uses Google's Flan-T5 for open-domain question answering.
* 🔄 **Hybrid Mode:** Combines vector retrieval with LLM generation for contextual technical responses.
* 🏷️ **Source Tagging:** Each answer displays its response source mode (e.g., Computer Knowledge, General) for transparency.
* 🌍 **Bilingual Support (English / Persian):** Automatic language detection and translation pipeline for seamless interaction.
* 💬 **Multi-Chat Management:** Create, rename, and manage multiple chat sessions with an intuitive UI.
* ⚡ **Optimized Performance**

  * Cached model loading using `@st.cache_resource`
  * Lightweight embeddings via `Sentence-Transformers`
  * Efficient vector search with Scikit-learn
  * Optimized disk usage (no redundant local model storage)

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/bytemind-ai.git
cd bytemind-ai
```

> **Note:** Replace `your-username` with your actual GitHub username.

### 2️⃣ Create a Virtual Environment

Using a virtual environment is strongly recommended.

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python3 -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Requirements

Install the necessary dependencies:

```bash
pip install -r requirements.txt
```

---

## 📂 Data Preparation & Indexing

Before running the application, generate the offline dataset and build the vector index.

### 4️⃣ Generate Offline Data

This script creates the specialized networking knowledge dataset:

```bash
python generate_offline_data.py
```

### 5️⃣ Build the Vector Index

This script processes the generated data and creates the vector database (`offline_index.pkl`):

```bash
python build_index.py
```

---

## ▶️ Run the Application

### 6️⃣ Start the Streamlit Dashboard

```bash
streamlit run app_v2.py
```

The application will automatically open in your browser.

> **Note:** The first run may take several minutes because the Flan-T5 model needs to be downloaded and cached locally.

---

## 🧩 Technical Architecture & Logic

### Computer Knowledge Mode Workflow

In **Computer Knowledge Mode**, the system follows a deterministic retrieval pipeline to ensure high factual reliability.

#### 1. Embedding

The user query is converted into a dense vector representation using Sentence Transformers.

#### 2. Retrieval

The vector is searched against the local knowledge index using nearest-neighbor search (`n_neighbors=1`).

#### 3. Thresholding

A strict similarity threshold (`> 0.85`) is applied to avoid returning irrelevant results.

#### 4. Extraction

Instead of generating an answer with the language model, the system uses regex-based extraction to retrieve the exact answer section from the matched document.

This approach minimizes hallucinations and improves reliability for networking and computer science concepts.

### Supported Technical Topics

* TCP / UDP
* OSI Model Layers
* Routing & Switching
* DNS
* IP Addressing
* Subnetting
* Network Protocols
* Computer Fundamentals

---

## ⚡ Performance Optimizations

### ✅ Memory Management

Uses:

```python
@st.cache_resource
```

to prevent model reloading on every interaction.

### ✅ Storage Optimization

Models are loaded directly from Hugging Face rather than stored permanently on disk, reducing storage requirements and preventing:

```text
No space left on device
```

errors.

### ✅ Improved User Experience

* Better text rendering using `st.markdown`
* Improved readability and automatic text wrapping
* Cleaner chat interface and conversation management

---

## 📁 Project Structure

```text
bytemind-ai/
│
├── app_v2.py                 # Main Streamlit application
├── generate_offline_data.py  # Generates networking knowledge dataset
├── build_index.py            # Builds vector search index
├── requirements.txt          # Project dependencies
├── offline_index.pkl         # Generated vector database
└── README.md                 # Project documentation
```

---

## 🛠️ Core Technologies

* Python
* Streamlit
* Sentence Transformers
* Scikit-learn
* Hugging Face Transformers
* Google Flan-T5
* Retrieval-Augmented Generation (RAG)

---

## 📜 License

This project was developed for educational and research purposes in:

* Natural Language Processing (NLP)
* Retrieval-Augmented Generation (RAG)
* Conversational AI Systems

Feel free to use, modify, and extend it for academic or personal projects.

---

## 👨‍💻 Author

**Fateme Rostamnejad**

AI Engineering & RAG System Implementation Project

---

## ⭐ Support the Project

If you found this project useful, please consider giving it a ⭐ on GitHub.

Your support helps improve and maintain the project.
