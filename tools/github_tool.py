import os
import requests
from typing import List, Dict, Any

class GitHubTool:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"

    def search_repositories(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Searches for GitHub repositories based on a query.
        """
        headers = {}
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        
        url = f"{self.base_url}/search/repositories?q={query}&per_page={limit}"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            items = response.json().get("items", [])
            results = []
            for item in items:
                results.append({
                    "name": item["full_name"],
                    "description": item["description"],
                    "stars": item["stargazers_count"],
                    "url": item["html_url"]
                })
            return results
        else:
            return [{"error": f"Failed to fetch data from GitHub. Status code: {response.status_code}"}]

    def run(self, action: str, **kwargs) -> Any:
        if action == "search":
            return self.search_repositories(kwargs.get("query"), kwargs.get("limit", 5))
        return {"error": "Unknown action"}
