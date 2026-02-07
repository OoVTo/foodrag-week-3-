# 🚀 Cloud Migration Plan: ChromaDB → Upstash Vector + Groq

## Executive Summary

This document outlines the strategic migration from a local RAG system (ChromaDB + Ollama) to a cloud-native architecture (Upstash Vector + Groq API).

**Migration Status**: ✅ In Progress (Week 2 → Week 3)

---

## Phase 1: Assessment & Planning ✅

### Current State (Week 2 - Local Version)
- **Vector DB**: ChromaDB (local persistent storage)
- **LLM**: Ollama (local inference)
- **Infrastructure**: Single machine dependent
- **Scalability**: Limited to local resources
- **Setup Complexity**: Requires Ollama installation + model pulls

### Target State (Week 3 - Cloud Version)
- **Vector DB**: Upstash Vector (serverless)
- **LLM**: Groq API (high-speed cloud inference)
- **Infrastructure**: Cloud-native, scalable
- **Scalability**: Unlimited horizontal scaling
- **Setup Complexity**: API keys only (no local setup)

---

## Phase 2: Technical Requirements ✅

### Removed Components
- ❌ ChromaDB persistent client
- ❌ Local embedding generation
- ❌ Ollama API calls
- ❌ Manual vector management

### Added Components
- ✅ Upstash Vector SDK initialization
- ✅ Groq API client integration
- ✅ Environment variable management (.env)
- ✅ Retry logic with exponential backoff
- ✅ Error handling for cloud services

### API Contracts Changed
```
# OLD: Local embedding generation
embedding = get_ollama_embedding(text)
collection.add(embeddings=[embedding], documents=[text])

# NEW: Upstash handles embedding automatically
vector_index.upsert(vectors=[(id, text, metadata)])
```

---

## Phase 3: Implementation Details ✅

### Data Migration
- ✅ Foods JSON preserved (90 food items)
- ✅ Metadata fields maintained (region, type)
- ✅ Batch upsert implementation (10 items per batch)
- ✅ Automatic embedding by Upstash

### Configuration
- ✅ Environment variables in `.env`:
  - `UPSTASH_VECTOR_REST_URL`
  - `UPSTASH_VECTOR_REST_TOKEN`
  - `GROQ_API_KEY`
  - `LLM_MODEL` (defaults to mixtral-8x7b-32768)

### Error Handling
- ✅ Retry mechanism with exponential backoff (3 attempts)
- ✅ Connection error handling with clear messages
- ✅ Timeout handling for API calls
- ✅ Graceful degradation warnings

---

## Phase 4: Testing Strategy

### Unit Tests
- [ ] Upstash connection validation
- [ ] Groq API authentication
- [ ] Vector upsert with metadata
- [ ] Similarity search accuracy
- [ ] LLM response generation
- [ ] Error handling and retries

### Integration Tests
- [ ] End-to-end query processing
- [ ] UI interaction tests
- [ ] Data persistence verification
- [ ] Cross-version compatibility (if needed)

### Performance Benchmarks
- [ ] Query latency comparison
- [ ] LLM response time (Groq vs Ollama)
- [ ] Embedding quality assessment
- [ ] Memory usage reduction

---

## Phase 5: Deployment Strategy

### Pre-deployment Checklist
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] API rate limits verified
- [ ] Cost estimation completed
- [ ] Rollback plan documented

### Deployment Steps
1. Create `cloud-migration` branch
2. Organize code into subdirectories
3. Document architecture decisions
4. Prepare testing suite
5. Merge to main after review
6. Archive local version for reference

### Post-deployment
- [ ] Monitor API usage
- [ ] Validate response quality
- [ ] Track cost implications
- [ ] Gather user feedback

---

## Risk Analysis & Mitigation

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **API Outage** | High | Implement fallback cache, retry logic |
| **Rate Limits** | Medium | Monitor usage, implement throttling |
| **Cost Overrun** | Medium | Set usage alerts, optimize batch sizes |
| **Data Loss** | Low | Upstash has built-in redundancy |

---

## Cost-Benefit Analysis

### Benefits
- ✅ No local infrastructure maintenance
- ✅ Automatic scaling for concurrent users
- ✅ Faster LLM inference (Groq: sub-100ms vs Ollama: 1-5s)
- ✅ Reduced operational overhead
- ✅ Geographic distribution capabilities

### Costs
- ⚠️ Recurring cloud API fees
- ⚠️ Dependencies on external services
- ⚠️ Potential API rate limit constraints

---

## Rollback Plan

If issues arise, can revert to:
- Local version: `local-version/rag_run_chromadb.py`
- Restore local ChromaDB data
- Start Ollama service locally

---

## Timeline

| Phase | Duration | Status |
|-------|----------|--------|
| Assessment | Complete | ✅ Done |
| Implementation | In Progress | 🔄 Week 3 |
| Testing | Pending | ⏳ Next |
| Deployment | Pending | ⏳ Final |

---

## Sign-off

- **Developer**: Gab
- **Reviewer**: [Pending]
- **Approval**: [Pending]
- **Date Completed**: [2026-02-07 - In Progress]
