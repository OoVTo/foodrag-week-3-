# -*- coding: utf-8 -*-
import os
import json
import sys
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import threading
import time
from dotenv import load_dotenv
from upstash_vector import Index
from groq import Groq

# Force UTF-8 output on Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

# Load environment variables
load_dotenv()

# Constants
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(os.path.dirname(SCRIPT_DIR), "foods.json")
UPSTASH_URL = os.getenv("UPSTASH_VECTOR_REST_URL")
UPSTASH_TOKEN = os.getenv("UPSTASH_VECTOR_REST_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# List of supported models to try in order
GROQ_MODELS = [
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768"  # Fallback (may be deprecated)
]
LLM_MODEL = GROQ_MODELS[0]  # Start with the first model

# Validate environment variables
if not all([UPSTASH_URL, UPSTASH_TOKEN, GROQ_API_KEY]):
    print("❌ Error: Missing required environment variables")
    print("   Please ensure .env file contains UPSTASH_VECTOR_REST_URL, UPSTASH_VECTOR_REST_TOKEN, and GROQ_API_KEY")
    sys.exit(1)

# Initialize cloud services
vector_index = Index(url=UPSTASH_URL, token=UPSTASH_TOKEN)
groq_client = Groq(api_key=GROQ_API_KEY)

# Load food data
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


def retry_with_backoff(func, max_retries=3, base_delay=1):
    """Retry function with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            print(f"⚠️  Attempt {attempt + 1} failed, retrying in {delay}s...")
            time.sleep(delay)


def get_embedding_and_upsert():
    """Upsert food items to Upstash Vector with automatic embedding"""
    print("🚀 Syncing food database to Upstash Vector...")
    
    # Fetch existing vectors to check what's already stored
    try:
        fetch_result = vector_index.fetch(["1"])
        existing_ids = set()
    except:
        existing_ids = set()
    
    # Prepare batch for upsert (Upstash auto-embeds text)
    vectors_to_upsert = []
    
    for item in food_data:
        item_id = item["id"]
        
        # Skip if already exists
        if item_id in existing_ids:
            continue
        
        # Enrich text with metadata for better embeddings
        enriched_text = item["text"]
        if "region" in item:
            enriched_text += f" Region: {item['region']}."
        if "type" in item:
            enriched_text += f" Type: {item['type']}."
        if "cooking_method" in item:
            enriched_text += f" Method: {item['cooking_method']}."
        if "nutritional_benefits" in item:
            enriched_text += f" Benefits: {item['nutritional_benefits']}."
        if "dietary_tags" in item:
            enriched_text += f" Tags: {', '.join(item['dietary_tags'])}."
        
        vectors_to_upsert.append({
            "id": item_id,
            "text": enriched_text,
            "metadata": {
                "original_text": item["text"],
                "region": item.get("region", "Unknown"),
                "type": item.get("type", "Unknown")
            }
        })
    
    # Batch upsert (Upstash handles embedding automatically)
    if vectors_to_upsert:
        batch_size = 10
        for i in range(0, len(vectors_to_upsert), batch_size):
            batch = vectors_to_upsert[i:i + batch_size]
            try:
                def upsert_batch():
                    vector_index.upsert(vectors=batch)
                
                retry_with_backoff(upsert_batch)
                print(f"✅ Upserted batch {i // batch_size + 1} ({len(batch)} items)")
            except Exception as e:
                print(f"❌ Error upserting batch: {e}")
    else:
        print("✅ All documents already synced to Upstash Vector")


# Sync data on startup
try:
    get_embedding_and_upsert()
except Exception as e:
    print(f"⚠️  Warning: Could not sync to Upstash Vector: {e}")
    print("   Continuing with query-only mode...")


# GUI Application
class RAGEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("☁️ Cloud RAG Editor - Upstash + Groq")
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
        
        # Output frame
        tk.Label(root, text="Output (Editable):", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(anchor=tk.W, padx=10)
        
        self.output_text = scrolledtext.ScrolledText(root, font=("Courier", 10), height=25, bg="white", fg="#333")
        self.output_text.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        self.status_label = tk.Label(root, text="Ready (Cloud-Powered ☁️)", bg="#f0f0f0", font=("Arial", 9), fg="#666")
        self.status_label.pack(anchor=tk.W, padx=10, pady=5)
    
    def ask_question(self):
        question = self.question_entry.get().strip()
        if not question:
            messagebox.showwarning("Warning", "Please enter a question!")
            return
        
        # Disable button during processing
        self.ask_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Processing... querying Upstash Vector & Groq LLM ☁️")
        self.root.update()
        
        # Run in separate thread to avoid freezing UI
        thread = threading.Thread(target=self._process_question, args=(question,))
        thread.start()
    
    def _process_question(self, question):
        try:
            # Step 1: Query Upstash Vector
            self.status_label.config(text="Searching vector database...")
            self.root.update()
            
            def query_vector():
                return vector_index.query(data=question, top_k=3, include_metadata=True)
            
            results = retry_with_backoff(query_vector)
            
            # Step 2: Extract documents
            top_docs = []
            top_ids = []
            for result in results:
                if isinstance(result, dict) and "metadata" in result:
                    top_docs.append(result["metadata"].get("original_text", result.get("text", "")))
                    top_ids.append(result.get("id", "unknown"))
                else:
                    top_docs.append(str(result))
                    top_ids.append("unknown")
            
            # Step 3: Build output with retrieved documents
            output = f"{'='*80}\n"
            output += f"Question: {question}\n"
            output += f"{'='*80}\n\n"
            output += "🧠 Retrieved Documents:\n"
            output += f"{'-'*80}\n"
            
            for i, doc in enumerate(top_docs):
                output += f"\n🔹 Source {i + 1} (ID: {top_ids[i]}):\n"
                output += f"    {doc[:200]}...\n" if len(doc) > 200 else f"    {doc}\n"
            
            output += f"\n{'-'*80}\n"
            
            # Step 4: Build prompt from context
            context = "\n".join(top_docs)
            
            prompt = f"""Using the following food database context, answer the user's question about food, cooking, nutrition, or cuisine culture.

Context from Food Database:
{context}

User Question: {question}

Provide a helpful, informative answer based on the context. If the context doesn't contain relevant information, you can provide general knowledge but indicate this.

Answer:"""
            
            # Step 5: Generate answer with Groq (with model fallback)
            self.status_label.config(text="Generating answer from Groq LLM...")
            self.root.update()
            
            answer = None
            used_model = None
            
            for model in GROQ_MODELS:
                try:
                    response = groq_client.chat.completions.create(
                        model=model,
                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        temperature=0.7,
                        max_tokens=1024
                    )
                    answer = response.choices[0].message.content
                    used_model = model
                    break
                except Exception as e:
                    error_str = str(e)
                    if "decommissioned" in error_str or "deprecated" in error_str or "not supported" in error_str:
                        print(f"⚠️  Model {model} not available, trying next...")
                        continue
                    else:
                        raise
            
            if answer is None:
                raise Exception("No available Groq models could be used")
            
            output += f"\n🤖 Answer (via Groq {used_model}):\n{'-'*80}\n"
            output += answer
            output += f"\n{'-'*80}\n\n"
            
            # Update UI from main thread
            self.output_text.insert(tk.END, output)
            self.output_text.see(tk.END)
            self.status_label.config(text="Ready (Cloud-Powered ☁️)")
            self.question_entry.delete(0, tk.END)
            self.ask_btn.config(state=tk.NORMAL)
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            messagebox.showerror("Error", error_msg)
            self.status_label.config(text="Error - see message box")
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
