# -*- coding: utf-8 -*-
import os
import json
import sys
import chromadb
import requests
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import threading

# Force UTF-8 output on Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

# Constants
CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "foods"
JSON_FILE = "foods.json"
EMBED_MODEL = "mxbai-embed-large"
LLM_MODEL = "llama3.2"

# Load data
with open(JSON_FILE, "r", encoding="utf-8") as f:
    food_data = json.load(f)

# Setup ChromaDB
chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)

# Ollama embedding function
def get_embedding(text):
    try:
        response = requests.post("http://localhost:11434/api/embeddings", json={
            "model": EMBED_MODEL,
            "prompt": text
        }, timeout=30)
        response.raise_for_status()
        return response.json()["embedding"]
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to Ollama at http://localhost:11434")
        print("   Please ensure Ollama is running. Start it with: ollama serve")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("❌ Error: Request to Ollama timed out")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error getting embedding: {e}")
        sys.exit(1)

# Add only new items
existing_ids = set(collection.get()['ids'])
new_items = [item for item in food_data if item['id'] not in existing_ids]

if new_items:
    print(f"🆕 Adding {len(new_items)} new documents to Chroma...")
    for item in new_items:
        # Enhance text with region/type and new metadata fields
        enriched_text = item["text"]
        if "region" in item:
            enriched_text += f" This food is popular in {item['region']}."
        if "type" in item:
            enriched_text += f" It is a type of {item['type']}."
        if "cooking_method" in item:
            enriched_text += f" Cooking method: {item['cooking_method']}."
        if "nutritional_benefits" in item:
            enriched_text += f" Nutritional benefits: {item['nutritional_benefits']}."
        if "cultural_background" in item:
            enriched_text += f" Cultural background: {item['cultural_background']}."
        if "dietary_tags" in item:
            enriched_text += f" Dietary tags: {', '.join(item['dietary_tags'])}."
        if "allergens" in item:
            enriched_text += f" Common allergens: {', '.join(item['allergens'])}."

        emb = get_embedding(enriched_text)

        collection.add(
            documents=[item["text"]],  # Use original text as retrievable context
            embeddings=[emb],
            ids=[item["id"]]
        )
else:
    print("✅ All documents already in ChromaDB.")


# GUI Application
class RAGEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RAG Editor - Ask Questions & Edit Answers")
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
        
        self.status_label = tk.Label(root, text="Ready", bg="#f0f0f0", font=("Arial", 9), fg="#666")
        self.status_label.pack(anchor=tk.W, padx=10, pady=5)
    
    def ask_question(self):
        question = self.question_entry.get().strip()
        if not question:
            messagebox.showwarning("Warning", "Please enter a question!")
            return
        
        # Disable button during processing
        self.ask_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Processing... retrieving documents and generating answer")
        self.root.update()
        
        # Run in separate thread to avoid freezing UI
        thread = threading.Thread(target=self._process_question, args=(question,))
        thread.start()
    
    def _process_question(self, question):
        try:
            # Step 1: Embed the user question
            self.status_label.config(text="Getting embedding...")
            self.root.update()
            q_emb = get_embedding(question)

            # Step 2: Query the vector DB
            results = collection.query(query_embeddings=[q_emb], n_results=3)

            # Step 3: Extract documents
            top_docs = results['documents'][0]
            top_ids = results['ids'][0]

            # Step 4: Build output with retrieved documents
            output = f"{'='*80}\n"
            output += f"Question: {question}\n"
            output += f"{'='*80}\n\n"
            output += "🧠 Retrieved Documents:\n"
            output += f"{'-'*80}\n"

            for i, doc in enumerate(top_docs):
                output += f"\n🔹 Source {i + 1} (ID: {top_ids[i]}):\n"
                output += f"    {doc}\n"

            output += f"\n{'-'*80}\n"

            # Step 5: Build prompt from context
            context = "\n".join(top_docs)

            prompt = f"""Use the following context to answer the question.

Context:
{context}

Question: {question}
Answer:"""

            # Step 6: Generate answer with Ollama
            self.status_label.config(text="Generating answer from LLM...")
            self.root.update()
            
            response = requests.post("http://localhost:11434/api/generate", json={
                "model": LLM_MODEL,
                "prompt": prompt,
                "stream": False
            }, timeout=60)
            response.raise_for_status()
            answer = response.json()["response"].strip()
            
            output += f"\n🤖 Answer:\n{'-'*80}\n"
            output += answer
            output += f"\n{'-'*80}\n\n"
            
            # Update UI from main thread
            self.output_text.insert(tk.END, output)
            self.output_text.see(tk.END)
            self.status_label.config(text="Ready")
            self.question_entry.delete(0, tk.END)
            self.ask_btn.config(state=tk.NORMAL)
            
        except requests.exceptions.ConnectionError:
            error_msg = "❌ Error: Cannot connect to Ollama at http://localhost:11434\n   Please ensure Ollama is running."
            messagebox.showerror("Connection Error", error_msg)
            self.status_label.config(text="Error - Connection failed")
            self.ask_btn.config(state=tk.NORMAL)
        except requests.exceptions.Timeout:
            messagebox.showerror("Timeout Error", "Request to Ollama timed out")
            self.status_label.config(text="Error - Request timeout")
            self.ask_btn.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")
            self.status_label.config(text=f"Error - {str(e)}")
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
root = tk.Tk()
app = RAGEditorApp(root)
root.mainloop()
