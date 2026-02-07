# -*- coding: utf-8 -*-
import os
import json
import sys
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import threading
import time
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Force UTF-8 output on Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

# Import Upstash Vector and Groq
try:
    from upstash_vector import Index
    from groq import Groq
except ImportError:
    print("❌ Required packages not installed. Please run:")
    print("   pip install upstash-vector groq python-dotenv")
    sys.exit(1)

# Constants
JSON_FILE = "foods.json"

# Environment variables
UPSTASH_URL = os.getenv("UPSTASH_VECTOR_REST_URL")
UPSTASH_TOKEN = os.getenv("UPSTASH_VECTOR_REST_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "mixtral-8x7b-32768")

# Validate environment variables
if not all([UPSTASH_URL, UPSTASH_TOKEN, GROQ_API_KEY]):
    print("❌ Error: Missing required environment variables in .env file")
    print("   Required: UPSTASH_VECTOR_REST_URL, UPSTASH_VECTOR_REST_TOKEN, GROQ_API_KEY")
    sys.exit(1)

# Initialize Upstash Vector client
try:
    vector_index = Index(url=UPSTASH_URL, token=UPSTASH_TOKEN)
    print("✅ Connected to Upstash Vector Database")
except Exception as e:
    print(f"❌ Error: Cannot connect to Upstash Vector: {e}")
    sys.exit(1)

# Initialize Groq client
try:
    groq_client = Groq(api_key=GROQ_API_KEY)
    print("✅ Connected to Groq API")
except Exception as e:
    print(f"❌ Error: Cannot initialize Groq client: {e}")
    sys.exit(1)

# Load data
with open(JSON_FILE, "r", encoding="utf-8") as f:
    food_data = json.load(f)

# Retry logic for cloud API calls
def retry_with_backoff(func, max_retries=3, base_delay=1):
    """Implement exponential backoff retry logic"""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            print(f"⏳ Retry attempt {attempt + 1}/{max_retries} after {delay}s... Error: {str(e)[:50]}")
            time.sleep(delay)

# Upsert food data to Upstash Vector
def upsert_foods_to_vector():
    """Upsert food data to Upstash Vector - automatic embedding"""
    print(f"🆕 Upserting {len(food_data)} food items to Upstash Vector...")
    
    try:
        vectors_to_upsert = []
        
        for item in food_data:
            # Enhance text with metadata (Upstash will automatically embed this)
            enriched_text = item["text"]
            if "region" in item:
                enriched_text += f" Region: {item['region']}."
            if "type" in item:
                enriched_text += f" Type: {item['type']}."
            
            vectors_to_upsert.append({
                "id": item["id"],
                "text": enriched_text,
                "metadata": {
                    "original_text": item["text"],
                    "region": item.get("region", ""),
                    "type": item.get("type", "")
                }
            })
        
        # Upsert in batches
        batch_size = 10
        for i in range(0, len(vectors_to_upsert), batch_size):
            batch = vectors_to_upsert[i:i + batch_size]
            data_to_upsert = [(v["id"], v["text"], v["metadata"]) for v in batch]
            
            vector_index.upsert(
                vectors=data_to_upsert
            )
            print(f"✅ Upserted batch {i//batch_size + 1}")
        
        print(f"✅ Successfully upserted all food items to Upstash Vector")
    
    except Exception as e:
        print(f"❌ Error upserting to Upstash Vector: {e}")
        raise

# Initialize vector database
try:
    upsert_foods_to_vector()
except Exception as e:
    print(f"⚠️  Warning: Could not upsert to Upstash Vector: {e}")
    print("   The application may have limited functionality")

# Query vector database with retry logic
def query_vector_db(question: str, top_k: int = 3) -> List[Dict]:
    """Query Upstash Vector with retry logic"""
    def _query():
        results = vector_index.query(
            data=question,
            top_k=top_k,
            include_vectors=False,
            include_metadata=True
        )
        return results
    
    try:
        return retry_with_backoff(_query)
    except Exception as e:
        print(f"❌ Error querying Upstash Vector: {e}")
        raise

# Query Groq LLM with retry logic
def query_groq_llm(prompt: str) -> str:
    """Query Groq API with retry logic and error handling"""
    def _query():
        message = groq_client.messages.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model=LLM_MODEL,
            max_tokens=1024,
            temperature=0.7,
        )
        return message.content[0].text
    
    try:
        return retry_with_backoff(_query, max_retries=3)
    except Exception as e:
        print(f"❌ Error querying Groq API: {e}")
        raise


# GUI Application
class RAGEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RAG Editor - Cloud-Powered (Upstash + Groq)")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        
        # Input frame
        input_frame = tk.Frame(root, bg="#f0f0f0")
        input_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(input_frame, text="Your Question:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.question_entry = tk.Entry(input_frame, font=("Arial", 11), width=80)
        self.question_entry.pack(pady=5, fill=tk.X)
        self.question_entry.bind("<Return>", lambda e: self.ask_question())
        
        # Button frame
        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.pack(pady=5, padx=10, fill=tk.X)
        
        self.ask_btn = tk.Button(button_frame, text="Ask", command=self.ask_question, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=10)
        self.ask_btn.pack(side=tk.LEFT, padx=5)
        
        self.save_btn = tk.Button(button_frame, text="Save Output", command=self.save_output, bg="#2196F3", fg="white", font=("Arial", 10, "bold"), width=10)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = tk.Button(button_frame, text="Clear", command=self.clear_output, bg="#f44336", fg="white", font=("Arial", 10, "bold"), width=10)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Status frame showing cloud services
        status_frame = tk.Frame(root, bg="#e8f5e9")
        status_frame.pack(pady=5, padx=10, fill=tk.X)
        tk.Label(status_frame, text="☁️  Using: Upstash Vector + Groq API", bg="#e8f5e9", font=("Arial", 9, "bold"), fg="#2e7d32").pack(anchor=tk.W)
        
        # Output frame
        tk.Label(root, text="Output (Editable):", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(anchor=tk.W, padx=10)
        
        self.output_text = scrolledtext.ScrolledText(root, font=("Courier", 10), height=20, bg="white", fg="#333")
        self.output_text.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        self.status_label = tk.Label(root, text="Ready", bg="#f0f0f0", font=("Arial", 9), fg="#666")
        self.status_label.pack(anchor=tk.W, padx=10, pady=5)
    
    def ask_question(self):
        question = self.question_entry.get().strip()
        if not question:
            messagebox.showwarning("Warning", "Please enter a question!")
            return
        
        # Disable button during processing
        self.ask_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Processing... querying cloud services")
        self.root.update()
        
        # Run in separate thread to avoid freezing UI
        thread = threading.Thread(target=self._process_question, args=(question,))
        thread.start()
    
    def _process_question(self, question):
        try:
            # Step 1: Query Upstash Vector
            self.status_label.config(text="Querying Upstash Vector Database...")
            self.root.update()
            
            results = query_vector_db(question, top_k=3)
            
            # Step 2: Extract documents from results
            top_docs = []
            top_ids = []
            
            if isinstance(results, list):
                for result in results:
                    if isinstance(result, dict):
                        top_ids.append(result.get("id", "N/A"))
                        # Try to get metadata first, then fall back to score
                        if "metadata" in result:
                            top_docs.append(result["metadata"].get("original_text", str(result)))
                        else:
                            top_docs.append(str(result))
                    else:
                        top_docs.append(str(result))
                        top_ids.append("N/A")
            
            if not top_docs:
                raise ValueError("No results returned from vector search")

            # Step 3: Build output with retrieved documents
            output = f"{'='*80}\n"
            output += f"Question: {question}\n"
            output += f"{'='*80}\n\n"
            output += "🧠 Retrieved Documents (from Upstash Vector):\n"
            output += f"{'-'*80}\n"

            for i, doc in enumerate(top_docs):
                output += f"\n🔹 Source {i + 1} (ID: {top_ids[i]}):\n"
                output += f"    {doc}\n"

            output += f"\n{'-'*80}\n"

            # Step 4: Build prompt from context
            context = "\n".join(top_docs)

            prompt = f"""Use the following context to answer the question accurately.

Context:
{context}

Question: {question}
Answer:"""

            # Step 5: Generate answer with Groq
            self.status_label.config(text="Generating answer from Groq API...")
            self.root.update()
            
            answer = query_groq_llm(prompt)
            
            output += f"\n🤖 Answer (from Groq API):\n{'-'*80}\n"
            output += answer
            output += f"\n{'-'*80}\n\n"
            
            # Update UI from main thread
            self.output_text.insert(tk.END, output)
            self.output_text.see(tk.END)
            self.status_label.config(text="Ready")
            self.question_entry.delete(0, tk.END)
            self.ask_btn.config(state=tk.NORMAL)
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            messagebox.showerror("Error", error_msg)
            self.status_label.config(text=f"Error - {str(e)[:40]}")
            self.ask_btn.config(state=tk.NORMAL)
    
    def clear_output(self):
        self.output_text.delete(1.0, tk.END)
        self.status_label.config(text="Output cleared")
    
    def save_output(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.output_text.get(1.0, tk.END))
            messagebox.showinfo("Success", f"Output saved to {file_path}")
            self.status_label.config(text=f"Saved to {file_path}")


# Start GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = RAGEditorApp(root)
    root.mainloop()

