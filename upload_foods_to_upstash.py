# -*- coding: utf-8 -*-
"""
Upload Food Data to Upstash Vector Database

This script reads foods.json and uploads all food items to Upstash Vector.
Upstash automatically handles embedding using state-of-the-art embedding models.

Requirements:
- Upstash Vector account with a database created
- Environment variables set: UPSTASH_VECTOR_REST_URL and UPSTASH_VECTOR_REST_TOKEN
"""

import os
import json
import sys
import time
from dotenv import load_dotenv
from upstash_vector import Index

# Force UTF-8 output on Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

# Load environment variables
load_dotenv()

# Get Upstash credentials
UPSTASH_URL = os.getenv("UPSTASH_VECTOR_REST_URL")
UPSTASH_TOKEN = os.getenv("UPSTASH_VECTOR_REST_TOKEN")

# Validate credentials
if not UPSTASH_URL or not UPSTASH_TOKEN:
    print("❌ Error: Missing Upstash credentials")
    print("\nPlease create a .env file with:")
    print("  UPSTASH_VECTOR_REST_URL=<your_upstash_url>")
    print("  UPSTASH_VECTOR_REST_TOKEN=<your_upstash_token>")
    print("\n📚 Get these from: https://console.upstash.com/vector")
    sys.exit(1)

# Load foods data
JSON_FILE = "foods.json"
try:
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        food_data = json.load(f)
    print(f"✅ Loaded {len(food_data)} food items from {JSON_FILE}")
except FileNotFoundError:
    print(f"❌ Error: Could not find {JSON_FILE}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"❌ Error: Invalid JSON in {JSON_FILE}")
    sys.exit(1)

# Initialize Upstash Vector Index
print("\n🔗 Connecting to Upstash Vector...")
try:
    vector_index = Index(url=UPSTASH_URL, token=UPSTASH_TOKEN)
    # Test connection by fetching info
    info = vector_index.info()
    print(f"✅ Connected to Upstash Vector")
    # InfoResult object has vector_count attribute directly
    vector_count = info.vector_count if hasattr(info, 'vector_count') else 'N/A'
    print(f"   Vector count: {vector_count}")
except Exception as e:
    print(f"❌ Error connecting to Upstash: {e}")
    print("   Check your UPSTASH_VECTOR_REST_URL and UPSTASH_VECTOR_REST_TOKEN")
    sys.exit(1)

# Prepare vectors for upload
print(f"\n📤 Preparing {len(food_data)} food items for upload...")
vectors_to_upsert = []

for item in food_data:
    item_id = item.get("id", "unknown")
    
    # Create enriched text with metadata
    enriched_text = item.get("text", "")
    
    if "region" in item and item["region"]:
        enriched_text += f" Region: {item['region']}."
    if "type" in item and item["type"]:
        enriched_text += f" Type: {item['type']}."
    if "cooking_method" in item and item["cooking_method"]:
        enriched_text += f" Cooking method: {item['cooking_method']}."
    if "nutritional_benefits" in item and item["nutritional_benefits"]:
        enriched_text += f" Nutritional benefits: {item['nutritional_benefits']}."
    if "cultural_background" in item and item["cultural_background"]:
        enriched_text += f" Cultural background: {item['cultural_background']}."
    if "dietary_tags" in item and item["dietary_tags"]:
        enriched_text += f" Dietary tags: {', '.join(item['dietary_tags'])}."
    if "allergens" in item and item["allergens"]:
        enriched_text += f" Common allergens: {', '.join(item['allergens'])}."
    
    # Prepare vector for upsert (Upstash uses 'data' field, not 'text')
    vectors_to_upsert.append({
        "id": str(item_id),
        "data": enriched_text,  # Use 'data' instead of 'text' for auto-embedding
        "metadata": {
            "original_text": item.get("text", ""),
            "region": item.get("region", "Unknown"),
            "type": item.get("type", "Unknown"),
            "cuisine": item.get("type", "Unknown")
        }
    })

print(f"✅ Prepared {len(vectors_to_upsert)} vectors")

# Upload in batches
print(f"\n🚀 Uploading to Upstash Vector (batch size: 10)...\n")
batch_size = 10
success_count = 0
error_count = 0

for i in range(0, len(vectors_to_upsert), batch_size):
    batch = vectors_to_upsert[i:i + batch_size]
    batch_num = i // batch_size + 1
    
    try:
        vector_index.upsert(vectors=batch)
        success_count += len(batch)
        print(f"✅ Batch {batch_num}: Upserted {len(batch)} items ({success_count}/{len(vectors_to_upsert)})")
        time.sleep(0.5)  # Rate limiting
    except Exception as e:
        error_count += len(batch)
        print(f"❌ Batch {batch_num}: Error - {e}")

# Final summary
print(f"\n{'='*60}")
print(f"📊 Upload Summary")
print(f"{'='*60}")
print(f"✅ Success: {success_count}/{len(vectors_to_upsert)}")
if error_count > 0:
    print(f"❌ Errors:  {error_count}/{len(vectors_to_upsert)}")

if success_count == len(vectors_to_upsert):
    print(f"\n🎉 All food items successfully uploaded to Upstash Vector!")
    print(f"   Your database is ready for RAG queries.")
    print(f"\n📝 Next steps:")
    print(f"   1. Run 'python -m cloud-version.rag_run' to start the cloud RAG app")
    print(f"   2. The app will query Upstash Vector and use Groq for LLM responses")
else:
    print(f"\n⚠️  Some items failed to upload. Please retry.")
    sys.exit(1)

print(f"{'='*60}\n")
