# 📍 Local Version: ChromaDB + Ollama (Reference)

## Status

This is the **Week 2 original implementation** preserved for reference and as a fallback option.

⚠️ **Note**: For new projects, use the cloud version in `../cloud-version/`

---

## Quick Start

### Prerequisites

1. **Ollama** installed on your system
   - Download from https://ollama.com/
   - Install and start the service: `ollama serve`

2. **Python 3.8+**

### Setup

```bash
# 1. Start Ollama (in separate terminal)
ollama serve

# 2. Pull required models (first time only)
ollama pull llama3.2
ollama pull mxbai-embed-large

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run application
python rag_run_chromadb.py
```

---

## What's Included

### `rag_run_chromadb.py`
The original Week 2 implementation:
- ChromaDB for vector storage
- Ollama for LLM & embedding
- Tkinter GUI
- Local persistence
- Fully self-contained

### `requirements.txt`
Minimal dependencies:
```
chromadb==0.4.24
requests==2.31.0
```

---

## Architecture

### Data Storage

```
Local File System
├── chroma_db/                  # Vector database
│   └── chroma.sqlite3
│       └── [embeddings & data]
└── ../data/foods.json          # Food knowledge base (90 items)
```

### Processing Pipeline

```
User Question
     ↓
Ollama (Local)
├─→ mxbai-embed-large (embedding)
└─→ Similarity search in ChromaDB
     ↓
Top 3 matches retrieved
     ↓
Ollama (Local)
└─→ llama3.2 (answer generation)
     ↓
Display result
```

---

## System Requirements

### Minimum

- **CPU**: 4+ cores
- **RAM**: 8GB+
- **Storage**: 5-10GB (for Ollama models)
- **Disk Speed**: SSD recommended

### Recommended

- **CPU**: 8+ cores
- **RAM**: 16GB+
- **GPU**: NVIDIA (optional but faster)
- **Storage**: 50GB+ free space

---

## Performance

### Query Speed

- Vector search: 5-10ms (local)
- Embedding: 500-1000ms (Ollama)
- LLM inference: 2-5 seconds (llama3.2)
- **Total**: 2.5-6 seconds per query

### Scalability

- **Concurrent users**: 1-2 (limited by local resources)
- **Data size**: Limited by available RAM
- **Maximum questions**: Depends on hardware

---

## Usage

### Launch Application

```bash
python rag_run_chromadb.py
```

Expected output:
```
🆕 Adding 90 new documents to Chroma...
✓ Processed item 1...
✓ Processed item 2...
...
✅ All documents processed
[Tkinter GUI opens]
```

### Ask Questions

Type natural language queries:

- "What are the ingredients in samosa?"
- "Tell me about Japanese ramen"
- "Which foods are good for health?"

### First Launch

On first run, the system will:
1. Create `chroma_db/` directory
2. Process and embed all 90 food items
3. Build local vector database
4. Store in SQLite for persistence

**Time**: 5-15 minutes depending on your hardware

---

## Local Storage

### Files Created

```
local-version/
├── chroma_db/                    # Vector database directory
│   ├── chroma.sqlite3
│   └── 114ea0a2-bdcf-...        # Collection metadata
└── rag_run_chromadb.py
```

### Database Size

- Empty: ~1MB
- With 90 foods: ~10-50MB (depends on embedding size)

### Cleanup

To reset the database:

```bash
# Backup first (optional)
cp -r chroma_db chroma_db.backup

# Remove database
rm -rf chroma_db

# Next run will recreate from scratch
```

---

## Advantages

✅ **Benefits of Local Version**

- Fully offline capable
- No external API dependencies
- No ongoing costs
- Data stays on your machine
- Full control over resources
- No rate limiting
- Can run 24/7 without worrying about API costs
- Educational value (see how embeddings work)

---

## Limitations

❌ **Challenges of Local Version**

- Requires powerful hardware
- Slow query response (2-6 seconds)
- Limited scalability
- Manual maintenance (updates, backups)
- Takes up significant disk space
- Limited by local CPU/GPU
- Cannot scale to multiple users easily
- Electricity costs

---

## Troubleshooting

### Ollama Not Running

```
❌ Error: Cannot connect to Ollama at http://localhost:11434
```

**Solution**:
```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Run application
python rag_run_chromadb.py
```

### Models Not Installed

```
❌ model not found
```

**Solution**:
```bash
ollama pull llama3.2
ollama pull mxbai-embed-large
```

### Slow Performance

**Causes**:
- Limited CPU resources
- Other programs using CPU
- Hard disk (not SSD)
- System swap memory

**Solutions**:
- Close other applications
- Use SSD for better performance
- Upgrade RAM
- Use GPU acceleration (if available)

### Database Corruption

```
❌ database is locked
```

**Solution**:
```bash
# Stop the application
# Delete corrupted database
rm -rf chroma_db

# Restart - will rebuild from scratch
```

---

## API Comparison

### vs Cloud Version

| Feature | Local | Cloud |
|---------|-------|-------|
| Setup time | 30+ min | 5 min |
| Query speed | 2-6s | 0.3-0.8s |
| Cost | Hardware + electricity | $5-25/mo |
| Offline | ✅ Yes | ❌ No |
| Scalability | Limited | Unlimited |
| Maintenance | Manual | Managed |

**Recommendation**: Use local for development/reference, cloud for production.

---

## Migration Path

If you want to migrate to cloud version:

1. Stop the application
2. Navigate to `../cloud-version/`
3. Follow setup in `cloud-version/README.md`
4. Your data (`foods.json`) already works with cloud version

---

## Development

### Extending with Custom Data

To add your own food items:

1. Edit `../data/foods.json`
2. Add entries with `id`, `text`, `region`, `type`
3. Delete `chroma_db/` to rebuild
4. Run application

### Debugging

Check the console output for:
- Embedding progress
- Database operations
- Query results
- Any errors

---

## Resources

- **Ollama Docs**: https://ollama.com/docs
- **ChromaDB Docs**: https://docs.trychroma.com/
- **Comparison**: `../docs/ARCHITECTURE_COMPARISON.md`

---

## When to Use This Version

✅ **Choose Local Version if**:
- You need offline capability
- Privacy is paramount
- Network unreliable
- Learning/educational purpose
- You have powerful hardware

❌ **Don't use if**:
- You need fast response times
- Multiple concurrent users
- Scalability required
- Prefer managed services
- Want minimal infrastructure

---

## Next Steps

1. ✅ Install Ollama
2. ✅ Pull models
3. ✅ Run application
4. 👉 Try asking questions
5. 👉 Read `../docs/ARCHITECTURE_COMPARISON.md`
6. 👉 Consider cloud version for production

---

**Version**: 1.0 (Local Reference)  
**Status**: Maintenance Mode  
**Last Updated**: 2026-02-07
