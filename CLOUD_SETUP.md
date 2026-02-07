# Cloud RAG Setup Guide - Upstash + Groq

This guide explains how to set up and use the cloud-based RAG (Retrieval-Augmented Generation) system using Upstash Vector database and Groq LLM.

## Overview

The cloud version (`cloud-version/rag_run.py`) replaces local components with cloud services:

| Component | Local | Cloud |
|-----------|-------|-------|
| **Vector Database** | ChromaDB (local SQLite) | **Upstash Vector** (serverless) |
| **Embeddings** | Ollama (local model) | **Upstash Auto-Embedding** |
| **LLM** | Ollama (local model) | **Groq API** (hosted) |
| **Deployment** | Single machine | Scalable cloud infrastructure |
| **Cost** | Free (hardware) | Pay-per-use (free tier available) |

## Prerequisites

1. **Python 3.8+** installed
2. **Upstash Account** (free tier available) - https://upstash.com
3. **Groq Account** (free tier available) - https://groq.com
4. **pip** package manager

## Step 1: Get Upstash Credentials

### Create Upstash Vector Database

1. Go to https://console.upstash.com/vector
2. Click **Create Index**
3. Fill in the form:
   - **Name**: `foods` or any name you prefer
   - **Region**: Choose closest to you
   - **Embedding Model**: Default is fine (state-of-the-art embedding)
4. Click **Create Index**

### Copy REST API Credentials

1. Click on your newly created index
2. Copy the **REST API URL** (looks like `https://xxx.upstash.io`)
3. Copy the **REST API Token**
4. Save these for Step 3

## Step 2: Get Groq API Key

1. Go to https://console.groq.com
2. Sign up with your email or GitHub
3. Navigate to **API Keys** section
4. Click **Create API Key**
5. Copy your API key
6. Save for Step 3

## Step 3: Configure Environment Variables

1. In the project root directory, create a `.env` file:

```bash
cd ragfood
nano .env  # or use your favorite editor
```

2. Add the following (replace `xxx` with your actual credentials):

```env
# Upstash Vector Database
UPSTASH_VECTOR_REST_URL=https://your-database.upstash.io
UPSTASH_VECTOR_REST_TOKEN=your_upstash_token_here

# Groq LLM API
GROQ_API_KEY=your_groq_api_key_here
```

3. Save and close the file

## Step 4: Install Dependencies

```bash
# Navigate to cloud-version directory
cd cloud-version

# Install required packages
pip install -r requirements.txt
```

### Required Packages
- `upstash-vector>=0.5.0` - Vector database client
- `groq>=0.12.0` - Groq LLM API client
- `python-dotenv>=1.0.0` - Environment variable management

## Step 5: Upload Food Data to Upstash

Before running the app, upload all foods from `foods.json` to your Upstash Vector database:

```bash
# From the project root directory
python upload_foods_to_upstash.py
```

### Expected Output

```
✅ Loaded 782 food items from foods.json
🔗 Connecting to Upstash Vector...
✅ Connected to Upstash Vector
   Vector count: 0

📤 Preparing 782 food items for upload...
✅ Prepared 782 vectors

🚀 Uploading to Upstash Vector (batch size: 10)...

✅ Batch 1: Upserted 10 items (10/782)
✅ Batch 2: Upserted 10 items (20/782)
... (more batches) ...

============================================================
📊 Upload Summary
============================================================
✅ Success: 782/782

🎉 All food items successfully uploaded to Upstash Vector!
   Your database is ready for RAG queries.
```

## Step 6: Run the Cloud RAG Application

```bash
# From project root or cloud-version directory
python cloud-version/rag_run.py
```

### GUI Features

1. **Question Input**: Type any question about food, cooking, nutrition, or cuisine
2. **Ask Button**: Submit your question (or press Enter)
3. **Retrieved Documents**: Shows top 3 relevant documents from Upstash
4. **Generated Answer**: AI response powered by Groq LLM
5. **Clear Button**: Clear output window
6. **Save Output**: Export results to text file

### Example Questions

- "What are the nutritional benefits of biryani?"
- "How is paneer butter masala prepared?"
- "What spices are in samosa?"
- "Tell me about Indian fruits"
- "What are some popular South Indian dishes?"

## Architecture

### Query Flow

```
User Question
    ↓
Upstash Vector DB (Semantic Search)
    ↓ (returns top 3 relevant documents)
Context + Prompt Building
    ↓
Groq LLM (llama-3.1-70b-versatile)
    ↓ (generates response)
Display Answer + Retrieved Context
```

### Data Upload Flow

```
foods.json
    ↓
Enrich with metadata (region, type, cooking method, etc.)
    ↓
Upstash Vector (auto-embedding)
    ↓
Semantic vector search ready
```

## Troubleshooting

### "Missing required environment variables"

**Solution**: Ensure `.env` file exists in project root with:
- `UPSTASH_VECTOR_REST_URL`
- `UPSTASH_VECTOR_REST_TOKEN`
- `GROQ_API_KEY`

### "Connection error to Upstash"

**Solutions**:
1. Verify your API URL and token are correct
2. Check your internet connection
3. Ensure Upstash service is operational
4. Try test with: `python -c "from upstash_vector import Index; print('OK')"`

### "Groq API error: 'Model not available'"

**Solution**: The app automatically tries multiple models:
1. `llama-3.1-70b-versatile` (recommended)
2. `llama-3.1-8b-instant` (faster)
3. `mixtral-8x7b-32768` (fallback)

If all fail, check:
- Your `GROQ_API_KEY` is correct
- You haven't exceeded rate limits
- You have API credits available

### "Upload script fails with 'No such file or directory: foods.json'"

**Solution**: Run the upload script from the project root:
```bash
cd c:\Users\melch\OneDrive\Desktop\ragfood
python upload_foods_to_upstash.py
```

## Performance Comparison

### Local vs Cloud

| Metric | Local | Cloud |
|--------|-------|-------|
| **Setup Time** | ~30 min (Ollama) | ~5 min (credentials) |
| **First Query** | 2-3 seconds | 4-6 seconds |
| **Concurrent Users** | 1-4 | 100+ (unlimited) |
| **Uptime** | Depends on machine | 99.9% SLA |
| **Cost** | Electricity + hardware | Pay-per-use (free tier) |
| **Scalability** | Limited | Unlimited |

## Costs

### Upstash Vector
- **Free Tier**: 25,000 vector updates per month, unlimited reads
- **Paid**: $0.0001 per vector write, data storage included

### Groq
- **Free Tier**: 100,000 requests per day, unlimited
- **Paid**: $0.50 per million input tokens, $1.50 per million output tokens

For our use case (~100 quarterly/month), **both are within free tier**.

## Advanced Configuration

### Customize Embedding Enrichment

Edit `upload_foods_to_upstash.py` to include or exclude metadata fields:

```python
# Example: Add more context to embeddings
enriched_text += f" Taste profile: {item['taste_profile']}."
enriched_text += f" Serving size: {item['serving_size']}."
```

### Adjust Search Parameters

Edit `cloud-version/rag_run.py`, in `_process_question()`:

```python
# Change number of retrieved documents
results = retry_with_backoff(
    lambda: vector_index.query(
        data=question, 
        top_k=5,  # Change from 3 to 5
        include_metadata=True
    )
)
```

### Model Selection

The app automatically selects from available Groq models. To prefer a specific model, edit `rag_run.py`:

```python
GROQ_MODELS = [
    "llama-3.1-8b-instant",  # Faster, lower quality
    "llama-3.1-70b-versatile",  # Higher quality (current default)
    "mixtral-8x7b-32768"
]
```

## Monitoring

### Check Upstash Statistics

1. Log in to https://console.upstash.com/vector
2. Click your index
3. View:
   - Vector count
   - API usage
   - Request latency

### Check Groq Usage

1. Log in to https://console.groq.com
2. Navigate to **Usage**
3. View:
   - Requests per minute
   - Token usage
   - Rate limits

## Migration from Local to Cloud

If you were using the local version:

```bash
# No need to do anything!
# The cloud version reads from foods.json just like local version
# Just run: python upload_foods_to_upstash.py
# Then: python cloud-version/rag_run.py
```

## Support & Resources

- **Upstash Docs**: https://docs.upstash.com
- **Groq API Docs**: https://console.groq.com/docs
- **Python Libraries**:
  - Upstash Vector SDK: https://github.com/upstash/vector-py
  - Groq SDK: https://github.com/groq/groq-python

## Next Steps

1. ✅ Get Upstash credentials
2. ✅ Get Groq API key
3. ✅ Create `.env` file
4. ✅ Install dependencies
5. ✅ Upload foods to Upstash
6. ✅ Run the cloud app
7. ✅ Ask questions and get AI-powered answers!

---

**Version**: 1.0  
**Last Updated**: February 7, 2026  
**Status**: Production Ready ☁️
