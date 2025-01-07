import os
import json
from kaggle.api.kaggle_api_extended import KaggleApi
import requests

# API Keys and Configurations
HUGGINGFACE_API_KEY = "your hugging face token"
GITHUB_API_KEY = "your github secret"
KAGGLE_JSON_PATH = r"location to your kaggle api json file"


def setup_kaggle_api(api_path):
    if not os.path.exists(api_path):
        raise FileNotFoundError(f"File not found: {api_path}")
    with open(api_path, "r") as f:
        kaggle_config = json.load(f)
    os.environ["KAGGLE_USERNAME"] = kaggle_config["username"]
    os.environ["KAGGLE_KEY"] = kaggle_config["key"]

def fetch_kaggle_datasets(query, num_results=5):
    try:
        api = KaggleApi()
        api.authenticate()
        datasets = api.dataset_list(search=query)
        return [f"{dataset.ref} - https://www.kaggle.com/{dataset.ref}" for dataset in datasets[:num_results]]
    except Exception as e:
        return [f"Error fetching datasets from Kaggle: {str(e)}"]

def fetch_huggingface_datasets(query):
    try:
        response = requests.get(
            f"https://huggingface.co/api/datasets?search={query}",
            headers={"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"},
        )
        response.raise_for_status()
        datasets = response.json()
        return [f"{dataset['id']} - https://huggingface.co/datasets/{dataset['id']}" for dataset in datasets[:5]]
    except Exception as e:
        return [f"Error fetching datasets from HuggingFace: {str(e)}"]

def fetch_github_datasets(query):
    try:
        headers = {"Authorization": f"token {GITHUB_API_KEY}"}
        response = requests.get(
            f"https://api.github.com/search/repositories?q={query}+dataset",
            headers=headers,
        )
        response.raise_for_status()
        repositories = response.json()["items"]
        return [f"{repo['full_name']} - {repo['html_url']}" for repo in repositories[:5]]
    except Exception as e:
        return [f"Error fetching datasets from GitHub: {str(e)}"]

def refine_query(use_case, problem):
    """
    Refines the query by combining the use case title and problem description with keywords.
    """
    keywords = {
        "Farther Reach": "electric vehicle customer segmentation dataset",
        "Optimized Productions & Predictive Maintenance": "predictive maintenance manufacturing dataset",
        "Safety & Sensing": "vehicle safety detection dataset",
        "Personalized Energy Solutions": "renewable energy dataset AI",
        "Enhanced Autonomous Features (EA)": "autonomous driving simulation dataset",
    }
    return keywords.get(use_case, problem)

def save_resources_to_markdown(use_cases, resources):
    try:
        with open("resources.md", "w") as file:
            file.write("# Resource Links\n\n")
            for i, use_case in enumerate(use_cases, 1):
                file.write(f"## Use Case {i}: {use_case}\n")
                file.write("### Relevant Datasets:\n")
                if use_case in resources and resources[use_case]:
                    for resource in resources[use_case]:
                        file.write(f"- {resource}\n")
                else:
                    file.write("- No relevant datasets found. Consider refining the query.\n")
                file.write("\n")
        print("\nResources saved to 'resources.md'")
    except Exception as e:
        print(f"Error saving resources to Markdown: {str(e)}")

def resource_asset_agent():
    try:
        # Setup Kaggle API
        setup_kaggle_api(KAGGLE_JSON_PATH)

        # Read use cases from Markdown file
        with open("use_cases.md", "r") as file:
            lines = file.readlines()

        # Extract use case titles and problems
        use_cases = [line.split(": ", 1)[1].strip() for line in lines if line.startswith("### Use Case")]
        problem_descriptions = [
            lines[i + 1].replace("**Problem:**", "").strip()
            for i, line in enumerate(lines) if line.startswith("### Use Case")
        ]

        # Fetch datasets for each use case
        resources = {}
        for use_case, problem in zip(use_cases, problem_descriptions):
            query = refine_query(use_case, problem)
            print(f"\nFetching datasets for: {use_case} with query: {query}")
            kaggle_datasets = fetch_kaggle_datasets(query)
            huggingface_datasets = fetch_huggingface_datasets(query)
            github_datasets = fetch_github_datasets(query)

            # Combine datasets
            resources[use_case] = kaggle_datasets + huggingface_datasets + github_datasets

        # Save resources to Markdown
        save_resources_to_markdown(use_cases, resources)

    except Exception as e:
        print(f"Error in Resource Asset Agent: {str(e)}")

if __name__ == "__main__":
    resource_asset_agent()
