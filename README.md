Here’s a clear, beginner-friendly `README.md` for your RAG project, designed to explain what it does, how it works, and how someone can run it from scratch.

---

## 📄 `README.md`

````markdown
# 🧠 RAG-Food: Cloud-Powered Retrieval-Augmented Generation

This is a **cloud-native RAG (Retrieval-Augmented Generation)** demo using:

- ☁️ **[Upstash Vector](https://upstash.com/)** - Serverless vector database with automatic embeddings
- ⚡ **[Groq API](https://groq.com/)** - High-speed LLM inference (Mixtral 8x7B)
- ✅ A comprehensive food dataset in JSON (90 global cuisine items)
- 🚀 No local ML setup required - fully cloud-powered

---

## 🎯 What This Does

This app allows you to ask questions like:

- “Which Indian dish uses chickpeas?”
- “What dessert is made from milk and soaked in syrup?”
- “What is masala dosa made of?”
- "Tell me about healthy foods high in omega-3s"

It **leverages cloud APIs for vector search and LLM inference**:

1. **Automatic embeddings** - Upstash Vector handles embedding automatically
2. Stores embeddings in **Upstash Vector** (serverless)
3. For any question, it:
   - Queries Upstash Vector for relevant context
   - Finds the top 3 most similar food items
   - Passes context + question to **Groq API** (fast LLM)
4. Returns a natural-language answer grounded in your data.

---

## 📦 Requirements

### ✅ Software

- Python 3.8+
- pip (Python package manager)

### ✅ API Keys Required

You'll need credentials for:

1. **Upstash Vector** - Get from [upstash.com](https://upstash.com/)
   - `UPSTASH_VECTOR_REST_URL`
   - `UPSTASH_VECTOR_REST_TOKEN`

2. **Groq API** - Get from [groq.com](https://groq.com/)
   - `GROQ_API_KEY`

---

## 🛠️ Installation & Setup

### 1. Clone or download this repo

```bash
git clone https://github.com/OoVTo/foodrag
cd foodrag
```

### 2. Create a `.env` file with your API keys

Create a file named `.env` in the project root:

```bash
# .env file
UPSTASH_VECTOR_REST_URL=https://your-upstash-url.upstash.io
UPSTASH_VECTOR_REST_TOKEN=your_upstash_token
GROQ_API_KEY=your_groq_api_key
LLM_MODEL=mixtral-8x7b-32768
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install upstash-vector groq python-dotenv
```

### 4. Run the RAG app

```bash
python rag_run.py
```

**First run:**
- ✅ Connects to Upstash Vector Database
- ✅ Connects to Groq API
- ✅ Upserts food items to vector database (automatic embedding)
- ✅ Launches interactive GUI

---

## 📁 File Structure

```
foodrag/
├── rag_run.py            # Main app script (cloud-powered)
├── foods.json            # Food knowledge base (90 items)
├── .env                  # API credentials (keep secret!)
├── requirements.txt      # Python dependencies
└── README.md             # This file
```## 🧠 How It Works (Step-by-Step)

### Architecture: Cloud-Native RAG

1. **Data Loading** - Food items loaded from `foods.json`
2. **Vector Indexing** - Upstash Vector automatically embeds and indexes each food item
3. **Serverless Storage** - Embeddings stored in Upstash Vector (no local DB needed)
4. **Query Processing**:
   - User question sent to Upstash Vector
   - Vector database performs semantic similarity search
   - Top 3 most relevant food items retrieved
5. **LLM Generation**:
   - Retrieved context + user question sent to Groq API
   - Groq's Mixtral model generates answer
   - Response returned with source attribution

### Key Benefits

- ⚡ **No Local Setup** - No Ollama, no ChromaDB directory
- 🚀 **Fast Inference** - Groq API provides sub-100ms LLM responses
- 📊 **Automatic Embeddings** - Upstash handles all embedding complexity
- 🔄 **Retry Logic** - Built-in exponential backoff for cloud reliability
- 💾 **Serverless** - Pay only for what you use

---

## 🔍 Try Custom Questions

You can update `rag_run.py` to include your own questions like:

```python
print(rag_query("What is tandoori chicken?"))
print(rag_query("Which foods are spicy and vegetarian?"))
```

---

## � Recent Updates (by Gab)

- ✨ **Technical Migration** - Migrated from local (ChromaDB + Ollama) to cloud (Upstash + Groq)
- ☁️ **Cloud-Native Architecture** - Serverless vector database and LLM inference
- ⚡ **Performance Improvements** - Sub-100ms Groq API responses
- 🤝 **Retry & Error Handling** - Exponential backoff for network resilience
- 📦 **Extended food database** - 90 diverse food items from global cuisines
- 🌏 **Japanese & Middle Eastern cuisine** - Comprehensive global coverage
- 🏷️ **Region tagging** - Each food item includes region and type metadata
- 🧠 **Reasoning context** - Enhanced embeddings for improved similarity matching
- 📊 **Structured data** - Better organization with food type categories

---

## �🚀 Next Ideas

* Swap in larger datasets (Wikipedia articles, recipes, PDFs)
* Add a web UI with Gradio or Flask
* Cache embeddings to avoid reprocessing on every run

---

## 👨‍🍳 Credits

Made by Callum using:

* [Ollama](https://ollama.com)
* [ChromaDB](https://www.trychroma.com)
* [mxbai-embed-large](https://ollama.com/library/mxbai-embed-large)
* Indian food inspiration 🍛

