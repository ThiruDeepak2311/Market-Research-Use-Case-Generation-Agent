
# AI Use Case Generator

The **AI Use Case Generator** is a modular, multi-agent system designed to generate actionable AI and Generative AI (GenAI) use cases for specific industries or companies. The system conducts in-depth research, proposes innovative AI use cases, fetches relevant datasets, and generates a professional PDF report. Additionally, it includes an interactive AI Chat System to query the report for insights.

## Demo
https://private-user-images.githubusercontent.com/116452492/400663327-939b29ec-80ee-41f2-b94c-d37b24f4665b.mp4?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzYyMzI1NzgsIm5iZiI6MTczNjIzMjI3OCwicGF0aCI6Ii8xMTY0NTI0OTIvNDAwNjYzMzI3LTkzOWIyOWVjLTgwZWUtNDFmMi1iOTRjLWQzN2IyNGY0NjY1Yi5tcDQ_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwMTA3JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDEwN1QwNjQ0MzhaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1lODJiMjhjYjlhMDU4Yjk5OTQyZDBmYTZlMmIwMjEwNjMxNmMwMWEwZTExNjFmOGM3ZmRkZDQ3MGUxODlmNzEzJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.z0IuKARBPl2BqVy3xmI8j_VOO5Inls2bXBcQ4CJIgvw

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Key Features
1. **Multi-Agent Workflow**:
   - **Research Agent**: Collects industry trends, competitors, and company details using APIs.
   - **Use Case Agent**: Generates AI/GenAI use cases with problems, solutions, impacts, and differentiators.
   - **Resource Asset Agent**: Fetches relevant datasets from Kaggle, Hugging Face, and GitHub.
   - **PDF Report Generator**: Creates a structured, professional PDF summarizing all findings.
   - **AI Chat System**: Interactive chatbot to answer questions about the generated PDF.

2. **APIs and Tools Used**:
   - **Serper API**: For fetching industry trends, competitors, and company details.
   - **Cohere API**: For generating AI/GenAI use cases.
   - **Hugging Face API**: For contextual question-answering and fetching datasets.
   - **Kaggle API**: For fetching relevant datasets.
   - **GitHub API**: For finding repositories with relevant datasets.
   - **FAISS**: For creating embeddings and enabling efficient context retrieval for the chatbot.

3. **Technologies**:
   - **Streamlit**: For building an interactive and user-friendly interface.
   - **FPDF**: For generating structured PDF reports.
   - **PyPDF2**: For extracting text from PDF files.
   - **SentenceTransformers**: For creating embeddings for the chatbot.
   - **FAISS**: For enabling fast similarity searches in the AI Chat System.

## Workflow
1. **Research Agent**:
   - Fetches industry trends using the Serper API.
   - Retrieves competitor details and company overview.
   - Outputs structured data for downstream agents.

2. **Use Case Agent**:
   - Uses Cohere API to generate 5 actionable AI use cases based on research data.
   - Includes problem statements, solutions, impacts, and differentiation strategies.

3. **Resource Asset Agent**:
   - Fetches relevant datasets from Kaggle, Hugging Face, and GitHub to support AI use cases.

4. **PDF Report Generator**:
   - Generates a well-structured PDF summarizing industry insights, use cases, and datasets.

5. **AI Chat System**:
   - Allows users to upload the generated PDF or any valid PDF.
   - Uses FAISS and Hugging Face APIs to answer questions interactively.


## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ai-use-case-generator.git
   cd ai-use-case-generator
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Add API keys:
   - Create a `.env` file or directly add your API keys in the script:
     ```
     SERPER_API_KEY = "your-serper-api-key"
     COHERE_API_KEY = "your-cohere-api-key"
     HUGGINGFACE_API_KEY = "your-huggingface-api-key"
     GITHUB_API_KEY = "your-github-api-key"
     KAGGLE_JSON_PATH = "path/to/your/kaggle.json"
     ```

4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## How to Use
1. **Research Agent**:
   - Enter the industry and company name.
   - Fetches trends, competitors, and company details.

2. **Use Case Agent**:
   - Generates innovative AI use cases based on research data.

3. **Resource Asset Agent**:
   - Fetches datasets supporting the AI use cases.

4. **PDF Report Generator**:
   - Generates a professional PDF summarizing findings.

5. **AI Chat System**:
   - Upload a PDF file and interact with it through the chatbot.

## File Structure
```
ai-use-case-generator/
├── app.py                     # Main Streamlit application file
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── utils/                     # Utility functions
│   ├── research_agent.py      # Research Agent logic
│   ├── use_case_agent.py      # Use Case Agent logic
│   ├── resource_asset_agent.py# Resource Asset Agent logic
│   ├── pdf_report_generator.py# PDF generation logic
│   ├── ai_chat_system.py      # AI Chat System logic
└── assets/                    # Additional assets (e.g., diagrams, images)
```

## Example Outputs
- **PDF Report**:
  A structured document containing:
  - Industry trends
  - AI/GenAI use cases
  - Relevant datasets

- **Chat System**:
  Interact with the PDF report to get detailed answers.

## Future Enhancements
- Add support for more dataset platforms (e.g., Databricks, Azure ML).
- Improve chatbot accuracy with fine-tuned models.
- Add real-time performance monitoring for all agents.
