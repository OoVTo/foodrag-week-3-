# -*- coding: utf-8 -*-
"""
ORIGINAL LOCAL VERSION: ChromaDB + Ollama RAG System
This is the Week 2 implementation using local vector database and LLM
"""
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
JSON_FILE = "../data/foods.json"
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
        enriched_text = item["text"]
        if "region" in item:
            enriched_text += f" This food is popular in {item['region']}."
        if "type" in item:
            enriched_text += f" It is a type of {item['type']}."

        emb = get_embedding(enriched_text)

        collection.add(
            documents=[item["text"]],
            embeddings=[emb],
            ids=[item["id"]]
        )
else:
    print("✅ All documents already in ChromaDB.")


# GUI Application
class RAGEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RAG Editor - Local Version (ChromaDB + Ollama)")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        
        input_frame = tk.Frame(root, bg="#f0f0f0")
        input_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(input_frame, text="Your Question:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.question_entry = tk.Entry(input_frame, font=("Arial", 11), width=80)
        self.question_entry.pack(pady=5, fill=tk.X)
        self.question_entry.bind("<Return>", lambda e: self.ask_question())
        
        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.pack(pady=5, padx=10, fill=tk.X)
        
        self.ask_btn = tk.Button(button_frame, text="Ask", command=self.ask_question, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=10)
        self.ask_btn.pack(side=tk.LEFT, padx=5)
        
        self.save_btn = tk.Button(button_frame, text="Save Output", command=self.save_output, bg="#2196F3", fg="white", font=("Arial", 10, "bold"), width=10)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = tk.Button(button_frame, text="Clear", command=self.clear_output, bg="#f44336", fg="white", font=("Arial", 10, "bold"), width=10)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        status_frame = tk.Frame(root, bg="#fff3e0")
        status_frame.pack(pady=5, padx=10, fill=tk.X)
        tk.Label(status_frame, text="📍 Local Version: ChromaDB + Ollama", bg="#fff3e0", font=("Arial", 9, "bold"), fg="#e65100").pack(anchor=tk.W)
        
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
        
        self.ask_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Processing...")
        self.root.update()
        
        thread = threading.Thread(target=self._process_question, args=(question,))
        thread.start()
    
    def _process_question(self, question):
        try:
            self.status_label.config(text="Getting embedding...")
            self.root.update()
            q_emb = get_embedding(question)

            results = collection.query(query_embeddings=[q_emb], n_results=3)
            top_docs = results['documents'][0]
            top_ids = results['ids'][0]

            output = f"{'='*80}\n"
            output += f"Question: {question}\n"
            output += f"{'='*80}\n\n"
            output += "🧠 Retrieved Documents (ChromaDB):\n"
            output += f"{'-'*80}\n"

            for i, doc in enumerate(top_docs):
                output += f"\n🔹 Source {i + 1} (ID: {top_ids[i]}):\n"
                output += f"    {doc}\n"

            output += f"\n{'-'*80}\n"

            context = "\n".join(top_docs)
            prompt = f"""Use the following context to answer the question.

Context:
{context}

Question: {question}
Answer:"""

            self.status_label.config(text="Generating answer from Ollama...")
            self.root.update()
            
            response = requests.post("http://localhost:11434/api/generate", json={
                "model": LLM_MODEL,
                "prompt": prompt,
                "stream": False
            }, timeout=60)
            response.raise_for_status()
            answer = response.json()["response"].strip()
            
            output += f"\n🤖 Answer (Ollama):\n{'-'*80}\n"
            output += answer
            output += f"\n{'-'*80}\n\n"
            
            self.output_text.insert(tk.END, output)
            self.output_text.see(tk.END)
            self.status_label.config(text="Ready")
            self.question_entry.delete(0, tk.END)
            self.ask_btn.config(state=tk.NORMAL)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")
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


if __name__ == "__main__":
    root = tk.Tk()
    app = RAGEditorApp(root)
    root.mainloop()
