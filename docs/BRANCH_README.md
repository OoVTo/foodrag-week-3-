# 📚 Cloud Migration Branch - Repository Structure

## 🎯 Overview

This branch demonstrates the **RAG-Food system evolution** from a local implementation to a cloud-native architecture.

```
foodrag/
├── local-version/          # Week 2: ChromaDB + Ollama (reference)
│   ├── rag_run_chromadb.py # Original local implementation
│   └── requirements.txt    # Local dependencies
│
├── cloud-version/          # Week 3+: Upstash + Groq (current)
│   ├── rag_run.py          # Cloud-native implementation
│   ├── .env.example        # Configuration template
│   └── requirements.txt    # Cloud dependencies
│
├── data/                   # Shared data
│   └── foods.json          # 90 food items dataset
│
├── docs/                   # Technical documentation
│   ├── MIGRATION_PLAN.md          # Detailed migration strategy
│   ├── ARCHITECTURE_COMPARISON.md # System comparison
│   ├── TESTING_RESULTS.md         # Performance metrics
│   └── API_SETUP_GUIDE.md         # API configuration guide
│
└── README.md               # This file
```

---

## 🚀 Quick Start

### Option 1: Cloud Version (Recommended)

```bash
# 1. Setup environment
cd cloud-version
cp .env.example .env
# Edit .env with your API keys

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run application
python rag_run.py
```

### Option 2: Local Version (Reference)

```bash
# 1. Install Ollama locally
# Visit https://ollama.com

# 2. Pull required models
ollama pull llama3.2
ollama pull mxbai-embed-large

# 3. Setup and run
cd local-version
pip install -r requirements.txt
python rag_run_chromadb.py
```

---

## 📋 Key Differences

| Feature | Local | Cloud |
|---------|-------|-------|
| **Setup** | Complex (30+ min) | Simple (5 min) |
| **Speed** | 2-6 seconds/query | 300-800ms/query |
| **Offline** | ✅ Fully offline | ❌ Requires internet |
| **Scaling** | Single machine | Unlimited |
| **Cost** | Hardware + Electricity | Pay-per-use ($5-25/mo) |
| **Maintenance** | Manual | Managed |

---

## 🔑 API Keys Required (Cloud Version)

1. **Upstash Vector**
   - Get from: https://upstash.com/
   - Need: REST URL, Token

2. **Groq API**
   - Get from: https://groq.com/
   - Need: API Key

See `docs/API_SETUP_GUIDE.md` for detailed instructions.

---

## 📊 What's New (Cloud Version)

### ✅ Completed
- [x] Upstash Vector integration
- [x] Groq API integration
- [x] Automatic embedding handling
- [x] Retry logic with exponential backoff
- [x] Error handling & fallbacks
- [x] GUI updated with cloud indicators
- [x] Performance optimizations

### 📝 Documentation
- [x] Migration plan
- [x] Architecture comparison
- [x] API setup guide
- [ ] Performance testing results (in progress)
- [ ] Load testing analysis (pending)

---

## 🧪 Testing

### Local Version Tests
```bash
cd local-version
python -m pytest tests/  # [Not yet implemented]
```

### Cloud Version Tests
```bash
cd cloud-version
python -m pytest tests/  # [Not yet implemented]
```

---

## 📈 Performance Comparison

See `docs/ARCHITECTURE_COMPARISON.md` for detailed metrics:

- **Query speed**: 8x faster ⚡
- **Setup time**: 6x easier 🚀
- **Scalability**: Unlimited capacity 📊
- **Code complexity**: Simplified 📦

---

## 🔄 Migration Path

```
Week 2: Local Version (Reference)
  ↓
  └─→ Feature complete with 90 foods
  
Week 3: Cloud Migration Branch
  ├─→ Architecture comparison
  ├─→ API integration
  ├─→ Performance testing
  └─→ Ready for production
  
Week 4+: Production Deployment
  ├─→ Monitoring & analytics
  ├─→ Cost optimization
  └─→ User feedback integration
```

---

## 💡 Recommended Reading Order

1. **Start here**: This README
2. **Then read**: `docs/API_SETUP_GUIDE.md` (to configure)
3. **For details**: `docs/ARCHITECTURE_COMPARISON.md`
4. **Implementation**: `docs/MIGRATION_PLAN.md`

---

## ❓ FAQ

**Q: Can I use both versions simultaneously?**  
A: Yes! They're in separate directories with independent configs.

**Q: What if the internet is down?**  
A: Switch to local version. It works completely offline.

**Q: How do I switch branches?**  
A: `git checkout main` (production) or stay on `cloud-migration` (development)

**Q: Is my API key secure?**  
A: Only if you keep `.env` out of git (already in `.gitignore`)

**Q: Can I host this myself?**  
A: Yes, but use `local-version/` or deploy Upstash/Groq alternatives.

---

## 🤝 Contributing

To add features:
1. Branch from `cloud-migration`
2. Test thoroughly
3. Document changes
4. Create pull request

---

## 📞 Support

- Architecture questions: See `docs/ARCHITECTURE_COMPARISON.md`
- API setup issues: See `docs/API_SETUP_GUIDE.md`
- Migration details: See `docs/MIGRATION_PLAN.md`

---

## 📄 License

Same as main repository

---

**Last Updated**: 2026-02-07  
**Status**: Development (Week 3)  
**Branch**: `cloud-migration`
