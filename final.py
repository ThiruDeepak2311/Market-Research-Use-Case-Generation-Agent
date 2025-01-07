import os
import re
import requests
import json
from fpdf import FPDF
from kaggle.api.kaggle_api_extended import KaggleApi
from sentence_transformers import SentenceTransformer
from cohere import Client
import PyPDF2
import faiss
import numpy as np
import streamlit as st

# Configure environment and logging
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "your serper api key")
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "your cohere api key")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "your hugging face token")
GITHUB_API_KEY = os.getenv("GITHUB_API_KEY", "your github secret")
KAGGLE_JSON_PATH = os.getenv("KAGGLE_JSON_PATH", r"location to kaggle api json file")

# Initialize Cohere Client
co = Client(COHERE_API_KEY)

# Set Kaggle credentials
if os.path.exists(KAGGLE_JSON_PATH):
    with open(KAGGLE_JSON_PATH, "r") as f:
        kaggle_creds = json.load(f)
    os.environ["KAGGLE_USERNAME"] = kaggle_creds.get("username", "")
    os.environ["KAGGLE_KEY"] = kaggle_creds.get("key", "")

# Helper Functions
def format_as_bullets(items):
    return "\n".join([f"- {item}" for item in items])

def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file."""
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = "".join(page.extract_text() for page in reader.pages if page.extract_text())
        return text
    except Exception as e:
        return f"Error extracting text: {e}"

def create_embeddings_and_index(text):
    """Create embeddings and FAISS index from the given text."""
    model = SentenceTransformer('all-MiniLM-L6-v2')
    sentences = [sentence.strip() for sentence in text.split(". ") if sentence]
    embeddings = model.encode(sentences)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index, sentences, model

def retrieve_context(index, model, sentences, query):
    """Retrieve the most relevant context from the FAISS index."""
    try:
        query_vector = model.encode([query])
        distances, indices = index.search(query_vector, 1)
        return sentences[indices[0][0]] if indices[0][0] < len(sentences) else ""
    except Exception as e:
        return f"Error retrieving context: {e}"

def generate_answer_with_hf_api(context, query):
    """Generate an answer using Hugging Face API."""
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {
        "inputs": f"Context: {context}\n\nQuestion: {query}\nAnswer:",
        "parameters": {"max_length": 300, "temperature": 0.7},
    }
    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/google/flan-t5-large",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()[0]["generated_text"]
    except Exception as e:
        return f"Error generating answer: {e}"

# Streamlit App
st.title("AI Use Case Generator")
st.sidebar.title("Configure Workflow")

industry = st.sidebar.text_input("Enter Industry", "Automotive")
company = st.sidebar.text_input("Enter Company Name", "Tesla")

if st.sidebar.button("Run Research Agent"):
    st.subheader("Research Agent")
    st.write("Fetching industry trends and company details...")

    try:
        industry_trends = ["Trend 1", "Trend 2"]  # Dummy placeholder for trends
        competitors = ["Competitor 1", "Competitor 2"]  # Dummy placeholder for competitors
        company_details = {"description": "Innovative company", "url": "https://example.com"}

        st.write("**Industry Trends:**")
        st.write(format_as_bullets(industry_trends))

        st.write("**Competitors:**")
        st.write(format_as_bullets(competitors))

        st.write("**Company Details:**")
        st.write(f"{company_details['description']} ({company_details['url']})")

        st.session_state["research_data"] = {
            "industry_trends": industry_trends,
            "competitors": competitors,
            "company_details": company_details,
        }
    except Exception as e:
        st.error(f"Error during research: {e}")

if st.sidebar.button("Run Use Case Agent"):
    if "research_data" in st.session_state:
        st.subheader("Use Case Agent")
        research_data = st.session_state["research_data"]
        try:
            use_cases = "Generated Use Cases Here"  # Dummy placeholder
            st.write("**Generated Use Cases:**")
            st.write(use_cases)
            st.session_state["use_cases"] = use_cases
        except Exception as e:
            st.error(f"Error generating use cases: {e}")
    else:
        st.error("Run Research Agent first.")

if st.sidebar.button("Run Resource Asset Agent"):
    if "use_cases" in st.session_state:
        st.subheader("Resource Asset Agent")
        try:
            resources = {
                "HuggingFace": ["Dataset 1", "Dataset 2"],
                "Kaggle": ["Dataset 3", "Dataset 4"],
                "GitHub": ["Dataset 5", "Dataset 6"],
            }  # Dummy placeholders
            st.write("**Relevant Datasets:**")
            for key, links in resources.items():
                st.write(f"**{key}:**")
                st.write(format_as_bullets(links))
            st.session_state["resources"] = resources
        except Exception as e:
            st.error(f"Error fetching resources: {e}")
    else:
        st.error("Run Use Case Agent first.")

if st.sidebar.button("Generate PDF Report"):
    if "research_data" in st.session_state and "use_cases" in st.session_state and "resources" in st.session_state:
        st.subheader("Generate PDF Report")
        st.write("Generating PDF report...")

        try:
            pdf_path = "GenAI_Summary_Report.pdf"  # Dummy placeholder for PDF path
            st.download_button("Download Report", data=open(pdf_path, "rb"), file_name=pdf_path)
            st.session_state["pdf_path"] = pdf_path
        except Exception as e:
            st.error(f"Error generating PDF: {e}")
    else:
        st.error("Complete all steps before generating the PDF report.")

if st.sidebar.button("Run AI Chat System"):
    st.subheader("AI Chat System")
    uploaded_pdf = st.file_uploader("Upload a PDF file to enable chat:", type=["pdf"])

    if uploaded_pdf is not None:
        try:
            st.write("Processing uploaded PDF...")
            pdf_text = extract_text_from_pdf(uploaded_pdf)
            if not pdf_text:
                st.error("No text found in the uploaded PDF.")
            else:
                st.success("PDF successfully uploaded and processed!")
                st.write("You can now ask questions about the content in the PDF.")

                index, sentences, model = create_embeddings_and_index(pdf_text)

                query = st.text_input("Ask a question about the uploaded PDF:")
                if query:
                    context = retrieve_context(index, model, sentences, query)
                    if not context:
                        st.error("No relevant context found for the question.")
                    else:
                        answer = generate_answer_with_hf_api(context, query)
                        st.write(f"**Question:** {query}")
                        st.write(f"**Answer:** {answer}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please upload a valid PDF file to enable the chat system.")
