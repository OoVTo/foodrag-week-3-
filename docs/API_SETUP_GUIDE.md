# 🔑 API Setup Guide for Cloud Version

## Prerequisites

- Python 3.8+
- Valid email address
- Internet connection

---

## Step 1: Upstash Vector Setup

### 1.1 Create Upstash Account

1. Visit https://upstash.com/
2. Click "Sign Up"
3. Choose your preferred signup method (Google, GitHub, or email)
4. Verify your email

### 1.2 Create Vector Database

1. Go to **Vector Databases** section
2. Click **Create Database**
3. Configure:
   - **Name**: `food-rag` (or your preference)
   - **Region**: `us-east-1` (recommended for latency)
   - **Dimension**: `1024` (default for embeddings)
4. Click **Create**

### 1.3 Get Your Credentials

1. Click on your database
2. Copy these values:
   - **REST URL**: `https://your-db-name-us1-vector.upstash.io`
   - **REST Token**: `ABgXXXXXX...` (keep this SECRET!)

```
These go in your .env as:
UPSTASH_VECTOR_REST_URL=https://your-db-name-us1-vector.upstash.io
UPSTASH_VECTOR_REST_TOKEN=ABgXXXXXX...
```

---

## Step 2: Groq API Setup

### 2.1 Create Groq Account

1. Visit https://groq.com/
2. Click **Create Account** or **Sign In with GitHub/Google**
3. Complete email verification

### 2.2 Generate API Key

1. Go to **API Keys** (usually in settings/console)
2. Click **Create API Key**
3. Name it: `foodrag-production`
4. Copy the API key: `gsk_XXXXXXXX...`
5. ⚠️ **SAVE IT SOMEWHERE SAFE** - You won't see it again!

```
This goes in your .env as:
GROQ_API_KEY=gsk_XXXXXXXX...
```

### 2.3 Verify Models Available

Groq offers several fast models. Default is `mixtral-8x7b-32768`:

- `mixtral-8x7b-32768` - Fast, powerful (recommended)
- `llama2-70b-4096` - Large model option
- `neural-chat-7b` - Smaller, faster

---

## Step 3: Local Configuration

### 3.1 Create `.env` File

In `cloud-version/` directory, create `.env`:

```bash
# Upstash Vector Configuration
UPSTASH_VECTOR_REST_URL=https://your-db-name-us1-vector.upstash.io
UPSTASH_VECTOR_REST_TOKEN=ABgXXXXXX...

# Groq API Configuration
GROQ_API_KEY=gsk_XXXXXXXX...

# Application Settings
VECTOR_INDEX_NAME=food-rag
LLM_MODEL=mixtral-8x7b-32768
EMBEDDING_DIMENSION=1024
```

### 3.2 Protect Your Credentials

⚠️ **IMPORTANT**: Never commit `.env` to git!

Verify `.gitignore` includes:
```
.env
.env.local
.env.*.local
```

---

## Step 4: Verify Setup

### 4.1 Install Dependencies

```bash
cd cloud-version
pip install -r requirements.txt
```

### 4.2 Test Connections

```python
# Quick test script
import os
from dotenv import load_dotenv

load_dotenv()

# Test Upstash
url = os.getenv("UPSTASH_VECTOR_REST_URL")
token = os.getenv("UPSTASH_VECTOR_REST_TOKEN")
print(f"✅ Upstash configured" if url and token else "❌ Upstash missing")

# Test Groq
key = os.getenv("GROQ_API_KEY")
print(f"✅ Groq configured" if key else "❌ Groq missing")
```

### 4.3 Run Application

```bash
python rag_run.py
```

If you see:
```
✅ Connected to Upstash Vector Database
✅ Connected to Groq API
🆕 Upserting 90 food items to Upstash Vector...
```

**Success! ✅ Setup complete!**

---

## Troubleshooting

### Error: "Cannot connect to Upstash Vector"

**Causes:**
- Invalid REST URL
- Invalid token
- Network issues
- Upstash service outage

**Solutions:**
1. Verify credentials from Upstash dashboard
2. Test connection: `curl -H "Authorization: Bearer YOUR_TOKEN" https://YOUR_URL/info`
3. Check internet connection
4. Wait for service recovery

### Error: "Groq API authentication failed"

**Causes:**
- Invalid API key
- API key expired
- Typo in `.env`

**Solutions:**
1. Generate new API key from Groq dashboard
2. Verify exact copy (no extra spaces)
3. Restart application after updating `.env`

### Error: ".env file not found"

**Causes:**
- Working in wrong directory
- File is named `.env.txt` instead of `.env`

**Solutions:**
```bash
# Make sure you're in cloud-version/
cd cloud-version

# Create file with correct name
cp .env.example .env  # if template exists
# OR
nano .env  # create and edit
```

### Error: "No module named 'upstash_vector'"

```bash
# Install missing package
pip install upstash-vector

# Or reinstall all
pip install -r requirements.txt
```

---

## Cost Estimates

### Upstash Vector (pay-as-you-go)

- **Free tier**: 
  - Up to 10,000 vectors
  - Queries included
  - Perfect for testing

- **Paid tier**:
  - Additional vectors: $0.0002 per vector
  - No query limits

### Groq API (free while in beta)

- Currently **free** for all users
- Will have pricing model in future
- Estimated: $0.0005-0.002 per request when paid

### Typical Monthly Cost

- 100 requests/day × 30 days = 3,000 requests
- Upstash: $0 (under free tier)
- Groq: $0 (beta free) → $1-5 (when paid)
- **Total: $0-5/month**

---

## Security Best Practices

### ✅ DO:

- [x] Keep `.env` out of git
- [x] Use strong, unique API keys
- [x] Rotate keys periodically
- [x] Use read-only tokens where possible
- [x] Monitor API usage in dashboards

### ❌ DON'T:

- [ ] Commit `.env` to repository
- [ ] Share API keys in messages/emails
- [ ] Use same key for multiple projects
- [ ] Hardcode credentials in code
- [ ] Post screenshots showing keys

---

## Environment Variables Reference

| Variable | Required | Example | Notes |
|----------|----------|---------|-------|
| `UPSTASH_VECTOR_REST_URL` | ✅ Yes | `https://...upstash.io` | From Upstash console |
| `UPSTASH_VECTOR_REST_TOKEN` | ✅ Yes | `ABgXXXX...` | Keep secret! |
| `GROQ_API_KEY` | ✅ Yes | `gsk_XXXX...` | From Groq dashboard |
| `LLM_MODEL` | ❌ No | `mixtral-8x7b-32768` | Defaults shown |
| `EMBEDDING_DIMENSION` | ❌ No | `1024` | Match Upstash setting |

---

## Next Steps

1. ✅ Complete this setup guide
2. ✅ Verify connections work
3. 👉 Read `ARCHITECTURE_COMPARISON.md` for system design
4. 👉 Check `MIGRATION_PLAN.md` for implementation details
5. 👉 Start with `rag_run.py` to use the app

---

## Support Resources

- **Upstash Docs**: https://upstash.com/docs
- **Groq Docs**: https://console.groq.com/docs
- **Python Dotenv**: https://github.com/theskumar/python-dotenv

---

**Last Updated**: 2026-02-07
