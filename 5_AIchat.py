import os
import re
import requests
import faiss
import numpy as np
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import logging
import PyPDF2  # Ensure PyPDF2 is imported

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Use environment variables for secure API token storage
HF_API_TOKEN = os.getenv("HF_API_TOKEN", "Your_Default_Token")

# Helper Functions
def extract_text_from_pdf(pdf_path):
    """
    Extract text from the provided PDF file with better error handling.
    """
    if not os.path.exists(pdf_path):
        logging.error(f"PDF file not found: {pdf_path}")
        return ""
    try:
        with open(pdf_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in tqdm(pdf_reader.pages, desc="Extracting pages"):
                text += page.extract_text() or ""
            return text
    except Exception as e:
        logging.error(f"Error reading PDF: {e}")
        return ""

def preprocess_text(text):
    """
    Improved text preprocessing.
    """
    text = re.sub(r"\s+", " ", text)  # Replace multiple spaces/newlines with a single space
    text = re.sub(r"[^A-Za-z0-9.,;!?()'\"$%-]+", " ", text)  # Retain $, %, and -
    return text.strip()

def create_embeddings_and_index(text):
    """
    Chunk text into smaller parts and create embeddings and FAISS index.
    """
    model = SentenceTransformer('all-MiniLM-L6-v2')
    chunk_size = 512
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    embeddings = model.encode(chunks)

    # Build FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    return index, chunks, model

def retrieve_context(index, model, chunks, query, top_k=1):
    """
    Retrieve the most relevant context from the FAISS index.
    """
    try:
        query_embedding = model.encode([query])
        distances, indices = index.search(np.array(query_embedding, dtype="float32"), top_k)
        context = " ".join([chunks[i] for i in indices[0]])
        return context
    except Exception as e:
        logging.error(f"Error during context retrieval: {e}")
        return ""

def generate_answer_with_hf_api(context, question):
    """
    Generate an answer using Hugging Face Inference API.
    """
    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}"
    }
    payload = {
        "inputs": f"Context: {context}\n\nQuestion: {question}\nAnswer:",
        "parameters": {"max_length": 300, "temperature": 0.6},
    }
    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/google/flan-t5-large",
            headers=headers,
            json=payload
        )
        if response.status_code == 200:
            return response.json()[0]["generated_text"]
        else:
            logging.error(f"API Error: {response.status_code}, {response.text}")
            return f"Error: {response.status_code}, {response.text}"
    except Exception as e:
        logging.error(f"Error during API call: {e}")
        return ""

# Main Function
def main():
    logging.info("=== AI-Powered PDF Chatbot ===")

    # Step 1: Get PDF path from user
    pdf_path = input("Enter the path to the PDF file: ").strip()

    # Step 2: Extract and preprocess text
    logging.info("\nLoading PDF content...")
    raw_text = extract_text_from_pdf(pdf_path)
    if not raw_text:
        logging.error("Failed to extract text. Exiting.")
        return
    preprocessed_text = preprocess_text(raw_text)

    # Step 3: Create embeddings and FAISS index
    logging.info("\nBuilding embeddings and FAISS index...")
    faiss_index, chunks, model = create_embeddings_and_index(preprocessed_text)

    # Step 4: Chat system
    logging.info("\nSystem is ready! Ask questions about the report (type 'exit' to quit):")
    while True:
        question = input("\nYour Question: ").strip()
        if question.lower() in ["exit", "quit", "bye"]:
            logging.info("Exiting. Thank you!")
            break

        # Retrieve context and generate answer
        context = retrieve_context(faiss_index, model, chunks, question)
        if not context:
            logging.warning("No relevant context found. Try rephrasing your question.")
            continue

        answer = generate_answer_with_hf_api(context, question)
        print(f"\nAnswer: {answer}")

if __name__ == "__main__":
    main()