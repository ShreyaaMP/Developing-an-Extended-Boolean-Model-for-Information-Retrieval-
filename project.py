import os
import math
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Directory where the document files are stored
DOCUMENTS_DIR = "D:\STUDY\project"

# Preprocessing
def preprocess(text):
    # Tokenization and lowercase
    tokens = text.lower().split()
    # Simple stemming for demo
    tokens = [token.rstrip(".,") for token in tokens]
    return tokens

# Calculate TF for a term in a document
def calculate_tf(term, document):
    tokens = preprocess(document)
    term_count = tokens.count(term)
    return term_count / len(tokens)

# Calculate IDF for a term in the corpus
def calculate_idf(term, corpus):
    doc_count = sum(1 for doc in corpus if term in preprocess(doc))
    return math.log(len(corpus) / (1 + doc_count))

# Calculate TF-IDF for a term in a document
def calculate_tf_idf(term, document, corpus):
    tf = calculate_tf(term, document)
    idf = calculate_idf(term, corpus)
    return tf * idf

# Load documents from files
def load_documents(directory):
    documents = {}
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), "r", encoding="utf-8") as file:
                documents[filename.split('.')[0]] = file.read()
    return documents

# Search function
def search(query, corpus):
    query_tokens = preprocess(query)
    relevant_docs = []
    
    # Evaluate each document
    for doc_id, document in corpus.items():
        score = 0
        for term in query_tokens:
            # Calculate TF-IDF for each term in the query
            if term in preprocess(document):
                tf_idf = calculate_tf_idf(term, document, corpus)
                score += tf_idf
                
        if score > 0:
            relevant_docs.append((doc_id, score))
    
    # Sort by relevance
    relevant_docs.sort(key=lambda x: x[1], reverse=True)
    return relevant_docs

# Get user input for query
def get_user_query():
    return entry_query.get()

# Perform search and display results
def perform_search():
    query = get_user_query()
    results = search(query, documents)
    
    # Clear previous results
    results_text.config(state=tk.NORMAL)
    results_text.delete("1.0", tk.END)
    
    if not results:
        results_text.insert(tk.END, "No documents found for the query: '{}'".format(query))
    else:
        results_text.insert(tk.END, "Search results for query: '{}'\n\n".format(query))
        for doc_id, score in results:
            results_text.insert(tk.END, "Document {}: Score {}\n".format(doc_id, score))
    
    results_text.config(state=tk.DISABLED)

# Create Tkinter GUI
def create_gui():
    window = tk.Tk()
    window.title("Information Retrieval System")

    label_query = tk.Label(window, text="Enter your query:")
    label_query.pack()

    global entry_query
    entry_query = tk.Entry(window, width=50)
    entry_query.pack()

    button_search = tk.Button(window, text="Search", command=perform_search)
    button_search.pack()

    global results_text
    results_text = scrolledtext.ScrolledText(window, width=80, height=20, wrap=tk.WORD)
    results_text.pack()

    window.mainloop()

# Example usage
def main():
    global documents
    documents = load_documents(DOCUMENTS_DIR)
    create_gui()

if __name__ == "__main__":
    main()
