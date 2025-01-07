import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import cohere
import json

# API Keys
SERPER_API_KEY = "72133600e1fc14e4ebccb6983dcff0f24fd9acac"  # Ensure this is vali
COHERE_API_KEY = "2lsphdgSl6HTz6KZJ5uMxT2yPZBdDTRtANGkv8Xh"
co = cohere.Client(COHERE_API_KEY)

def fetch_industry_trends(industry, num_results=5):
    """
    Fetches industry trends using the Serper REST API.
    """
    try:
        query = f"{industry} industry trends 2025"
        headers = {"X-API-KEY": SERPER_API_KEY}
        payload = {"q": query}
        response = requests.post("https://google.serper.dev/search", headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        trends = [
            f"{result.get('title', 'No title available')} - {result.get('link', 'No link available')}"
            for result in data.get("organic", [])
        ]
        return trends[:num_results]
    except Exception as e:
        return [f"Error fetching industry trends: {str(e)}"]

def fetch_competitors(company_name):
    """
    Fetches competitors of the given company using Serper API.
    """
    try:
        headers = {"X-API-KEY": SERPER_API_KEY}
        payload = {"q": f"{company_name} competitors"}
        response = requests.post("https://google.serper.dev/search", headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        competitors = [
            f"{result.get('title', 'No title available')} - {result.get('link', 'No link available')}"
            for result in data.get("organic", [])
        ]
        return competitors[:5]
    except Exception as e:
        return [f"Error fetching competitors: {str(e)}"]

def fetch_insights_with_cohere(industry):
    """
    Fetches AI/ML insights using Cohere API.
    """
    try:
        prompt = (
            f"Provide detailed insights into AI/ML trends in the {industry} industry. Focus on:\n"
            f"1. Disruptive AI-powered solutions in manufacturing and logistics.\n"
            f"2. Enhancements to customer experience using AI.\n"
            f"3. Emerging opportunities for Generative AI in the industry."
        )
        response = co.generate(
            model="command-xlarge",
            prompt=prompt,
            max_tokens=750,
            temperature=0.7,
        )
        return response.generations[0].text.strip()
    except Exception as e:
        return f"Error fetching insights with Cohere: {str(e)}"

def fetch_company_details(company_name):
    """
    Fetches basic company details using Serper API.
    """
    try:
        headers = {"X-API-KEY": SERPER_API_KEY}
        payload = {"q": f"{company_name} company overview"}
        response = requests.post("https://google.serper.dev/search", headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if "organic" in data and len(data["organic"]) > 0:
            result = data["organic"][0]
            return {
                "name": company_name,
                "description": result.get("snippet", "No description found."),
                "url": result.get("link", "https://www.example.com"),
            }
        return {"name": company_name, "description": "No description found.", "url": "https://www.example.com"}
    except Exception as e:
        return {"name": company_name, "description": f"Error fetching details: {str(e)}", "url": ""}

def enhanced_fetch_research_data(industry, company_name):
    """
    Fetches research data and saves it to a JSON file.
    """
    try:
        # Gather data
        industry_trends = fetch_industry_trends(industry)
        competitors = fetch_competitors(company_name)
        ai_insights = fetch_insights_with_cohere(industry)
        company_details = fetch_company_details(company_name)

        # Combine results
        research_data = {
            "industry_trends": industry_trends,
            "competitors": competitors,
            "ai_insights": ai_insights,
            "company_details": company_details,
        }

        # Save to file
        with open("research_output.json", "w") as file:
            json.dump(research_data, file, indent=4)

        print("\nResearch data saved to 'research_output.json'")
        return research_data
    except Exception as e:
        print(f"Error fetching research data: {str(e)}")

if __name__ == "__main__":
    industry = input("Enter the industry to research: ")
    company_name = input("Enter the company name: ")
    enhanced_fetch_research_data(industry, company_name)
