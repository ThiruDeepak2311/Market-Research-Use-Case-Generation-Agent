import json
import cohere

# Initialize Cohere Client
COHERE_API_KEY = "2lsphdgSl6HTz6KZJ5uMxT2yPZBdDTRtANGkv8Xh"
co = cohere.Client(COHERE_API_KEY)

def generate_use_cases(industry_trends, company_details, competitors):
    """
    Generates AI/GenAI use cases using Cohere's API, enhanced with industry trends and competitor analysis.
    """
    try:
        # Trim industry trends and competitors for concise input
        industry_trends_short = "\n".join([trend.split(" - ")[0] for trend in industry_trends])
        competitors_short = "\n".join([comp.split(" - ")[0] for comp in competitors])

        # Refined prompt with trends and competitor context
        prompt = (
            f"The following are key trends in the automotive industry:\n{industry_trends_short}\n\n"
            f"The following companies are competitors:\n{competitors_short}\n\n"
            f"Tesla's focus:\n{company_details}\n\n"
            f"Generate 5 innovative and actionable AI or Generative AI use cases for Tesla. For each use case, include:\n"
            f"1. The Problem it solves.\n"
            f"2. The AI/GenAI Solution.\n"
            f"3. The Impact or benefit of the solution.\n"
            f"4. How it differentiates Tesla from its competitors.\n\n"
            f"Format each use case as:\n"
            f"### Use Case [Number]: [Title]\n"
            f"**Problem**: [Description]\n"
            f"**Solution**: [Description]\n"
            f"**Impact**: [Description]\n"
            f"**Differentiation**: [Description]\n\n"
            f"Make sure all use cases are concise, relevant, and align with Tesla's vision."
        )

        # Generate use cases using Cohere API
        response = co.generate(
            model="command-xlarge",
            prompt=prompt,
            max_tokens=1000,
            temperature=0.7,
        )

        # Return the generated text
        return response.generations[0].text.strip()

    except Exception as e:
        return f"Error generating use cases: {str(e)}"

def save_use_cases_to_markdown(use_cases):
    """
    Saves the generated use cases to a Markdown file.
    """
    try:
        with open("use_cases.md", "w") as file:
            file.write("# Generated Use Cases\n\n")
            file.write(use_cases)
        print("\nUse cases saved to 'use_cases.md'")
    except Exception as e:
        print(f"Error saving use cases to Markdown: {str(e)}")

def use_case_agent():
    """
    Reads research data from a file, generates use cases, and saves them to a Markdown file.
    """
    try:
        # Load research data from the JSON file
        with open("research_output.json", "r") as file:
            research_data = json.load(file)

        # Extract inputs for Use Case Agent
        industry_trends = research_data["industry_trends"]
        company_details = research_data["company_details"]["description"]
        competitors = research_data["competitors"]

        # Generate use cases
        raw_use_cases = generate_use_cases(industry_trends, company_details, competitors)

        # Save use cases to Markdown file
        save_use_cases_to_markdown(raw_use_cases)

    except FileNotFoundError:
        print("Error: 'research_output.json' not found. Please run the Research Agent first.")
    except Exception as e:
        print(f"Error in Use Case Agent: {str(e)}")

if __name__ == "__main__":
    use_case_agent()
