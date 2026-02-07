# 🧠 RAG-Food: Retrieval-Augmented Generation for Food Knowledge

Ask AI questions about food, cooking, nutrition, and cuisine—powered by your own knowledge base of 782+ food items. Choose between **local** or **cloud-based** deployment.

```
┌─────────────────────────────────────────────────────────────┐
│  Example Questions:                                         │
│  💬 "What is biryani and how is it made?"                  │
│  💬 "What are the nutritional benefits of spinach?"        │
│  💬 "Tell me about Japanese ramen"                         │
│  💬 "Which desserts use chocolate?"                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start: Choose Your Path

### ☁️ **Cloud Version (Recommended for Most Users)**
Uses **Upstash Vector DB** + **Groq LLM API**

```bash
# 1. Get credentials (5 minutes)
# 2. Copy to .env file
# 3. pip install -r cloud-version/requirements.txt
# 4. python upload_foods_to_upstash.py
# 5. python cloud-version/rag_run.py
```

**Best for:**
- ✅ No complex local setup
- ✅ Scalable for many users
- ✅ Production deployments
- ✅ Free tier available
- ⏱️ **Total setup: 10 minutes**

👉 **[Cloud Setup Guide →](CLOUD_SETUP.md)**

---

### 💻 **Local Version (Development/Learning)**
Uses **ChromaDB** + **Ollama**

```bash
# 1. Install Ollama from https://ollama.com
# 2. ollama pull llama3.2 && ollama pull mxbai-embed-large
# 3. pip install chromadb requests
# 4. python rag_run.py
```

**Best for:**
- ✅ Learning & experimentation
- ✅ No internet required
- ✅ Maximum privacy
- ✅ Full control over local models
- ⏱️ **Total setup: 30 minutes**

---

## 📊 Comparison: Local vs Cloud

| Feature | Local | Cloud |
|---------|-------|-------|
| **Vector DB** | ChromaDB | Upstash ☁️ |
| **LLM** | Ollama | Groq ☁️ |
| **Setup Time** | ~30 min | ~10 min |
| **Response Time** | 1-2 sec | 2-4 sec |
| **Scalability** | 1 machine | Unlimited |
| **Cost** | Electricity | Free tier |
| **Privacy** | Full local control | Cloud provider |

👉 **[Full Comparison →](PERFORMANCE_COMPARISON.md)**

---

## 📁 File Structure

```
ragfood/
├── README.md                      # This file
├── foods.json                     # 782+ food items database
│
├── 📍 LOCAL VERSION:
├── rag_run.py                     # Run local RAG app
├── chroma_db/                     # ChromaDB storage
│
├── ☁️ CLOUD VERSION:
├── cloud-version/
│   ├── rag_run.py                # Run cloud RAG app
│   └── requirements.txt           # Cloud dependencies
├── upload_foods_to_upstash.py    # Upload foods to Upstash
├── .env.example                   # Credentials template
│
├── 📚 DOCUMENTATION:
├── CLOUD_SETUP.md                # Cloud setup guide
├── IMPLEMENTATION_SUMMARY.md     # What's new & how it works
└── PERFORMANCE_COMPARISON.md     # Detailed performance report
```

---

## 🎯 How It Works

### The RAG Process

```
User Question: "What is masala dosa?"
       ↓
Search Vector Database (ChromaDB or Upstash)
       ↓
Retrieve Top 3 Relevant Docs
       ↓
Build Prompt with Context
       ↓
Send to LLM (Ollama or Groq)
       ↓
Generate Answer
       ↓
Display with Retrieved Context
```

### The Data

- **782 food items** from around the world
- **Metadata**: Region, type, cooking method, nutritional benefits
- **Enriched embeddings**: Text + metadata combined for better search
- **No external internet required** for retrieval (local version)

---

## 🎓 What's Inside

### Local Version Features
- ✅ Offline operation (no internet needed)
- ✅ Complete privacy (all local)
- ✅ Fully customizable models
- ✅ Learn how RAG works under the hood
- ✅ GUI with editable output

### Cloud Version Features
- ✅ Serverless deployment (no infrastructure)
- ✅ Auto-scaling to 1000s of users
- ✅ Single-command data upload
- ✅ Automatic model updates
- ✅ 99.9% uptime SLA
- ✅ Free tier sufficient for testing

---

## 📝 Usage Examples

### Cloud Version
```bash
python cloud-version/rag_run.py
```
- Opens GUI window
- Type your question about any food
- Get AI answer with relevant context

### Local Version
```bash
python rag_run.py
```
- Opens GUI window (same interface)
- All processing happens locally
- Requires Ollama running in background

---

## 🔐 Security & Privacy

| Concern | Local | Cloud |
|---------|-------|-------|
| **Data Location** | Your machine | Upstash servers |
| **API Keys** | N/A | In `.env` (git-ignored) |
| **Internet** | Not used | Required |
| **Model Access** | Full | Vendor lock-in |

**Cloud privacy note**: Food descriptions are stored in Upstash. No personal data is included.

---

## 📦 Installation

### Both Versions
```bash
# Clone or download this repo
cd ragfood

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install common dependencies
pip install -r requirements.txt
```

### For Local Version Only
```bash
# Install Ollama from https://ollama.com
# Then run these models:
ollama pull llama3.2
ollama pull mxbai-embed-large

# Ensure Ollama is running
ollama serve
```

### For Cloud Version Only
```bash
pip install -r cloud-version/requirements.txt
# Then follow CLOUD_SETUP.md
```

---

## 🆘 Troubleshooting

### "ModuleNotFoundError"
```bash
pip install chromadb requests  # For local
# OR
pip install -r cloud-version/requirements.txt  # For cloud
```

### "Cannot connect to Ollama"
```bash
# Make sure Ollama is running:
ollama serve
# In another terminal, test:
ollama run llama3.2
```

### "Missing UPSTASH_VECTOR_REST_URL"
```bash
# Create .env file in project root:
UPSTASH_VECTOR_REST_URL=https://...
UPSTASH_VECTOR_REST_TOKEN=...
GROQ_API_KEY=...
# Then retry
```

**[More help in CLOUD_SETUP.md →](CLOUD_SETUP.md)**

---

## 📈 Recent Updates (Feb 2026)

- ☁️ **Cloud Deployment**: Full Upstash Vector + Groq integration
- 🚀 **Upload Automation**: One-command database sync script
- 📚 **Comprehensive Docs**: Setup guides, performance reports, troubleshooting
- 🔐 **Security**: Environment variable protection, .gitignore updates
- 📊 **Performance Analysis**: Local vs cloud detailed comparison
- 🎯 **Production Ready**: Error handling, retries, model fallbacks

---

## 🌟 Features

- 🧠 **Semantic Search**: Find relevant foods by meaning, not just keywords
- 🤖 **AI-Powered**: Groq or Ollama generate context-aware answers
- 🔄 **Dual Deployment**: Choose local OR cloud (or both!)
- 📝 **Editable GUI**: Edit answers before saving
- 💾 **Export Results**: Save Q&A to text files
- 🌍 **782+ Foods**: Global cuisine coverage
- ⚡ **Fast**: Sub-second vector search
- 💰 **Free Tier**: Both cloud services offer free usage

---

## 🚀 Next Steps

1. **Decide**: Local or cloud? (see comparison above)
2. **Setup**: Follow the appropriate guide
3. **Upload**: Add your foods to the database
4. **Ask**: Start querying your knowledge base!

---

## 📖 Documentation

| Document | Purpose |
|----------|---------|
| [CLOUD_SETUP.md](CLOUD_SETUP.md) | Step-by-step cloud deployment |
| [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) | What's new and how it works |
| [PERFORMANCE_COMPARISON.md](PERFORMANCE_COMPARISON.md) | Detailed performance metrics |
| [.env.example](.env.example) | Credentials template |

---

## 💡 Use Cases

- 📚 **Personal Knowledge Base**: Index and query your own documents
- 🍽️ **Recipe Assistant**: Get cooking suggestions based on available ingredients
- 🎓 **Educational**: Learn how RAG, embeddings, and LLMs work
- 🏢 **Enterprise**: Q&A system for internal documentation
- 🌐 **Web Service**: Deploy cloud version for public access

---

## 🏆 Tech Stack

### Local
- **Python 3.8+**
- **ChromaDB** - Vector database
- **Ollama** - Local LLM + embeddings
- **Tkinter** - GUI

### Cloud
- **Python 3.8+**
- **Upstash Vector** - Serverless vector database
- **Groq API** - High-speed LLM API
- **Tkinter** - GUI

---

## 📞 Support

For issues or improvements:
1. Check [CLOUD_SETUP.md](CLOUD_SETUP.md) troubleshooting section
2. Review [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
3. Check logs for error messages
4. Verify credentials in `.env` file

---

## 📄 License

This project is open source. Feel free to modify and redistribute.

---

**Version**: 2.0 (Cloud-Ready)  
**Last Updated**: February 7, 2026  
**Status**: ✅ Production Ready

