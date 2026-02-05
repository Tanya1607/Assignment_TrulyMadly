from llm.client import LLMClient
from agents.models import Plan
from llm.logging_config import logger

class PlannerAgent:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def create_plan(self, user_query: str) -> Plan:
        logger.info(f"Planning steps for query: {user_query}")
        prompt = f"""
        You are a Planner Agent for an AI Operations Assistant.
        Your goal is to break down a user query into a series of steps using the available tools.
        
        Available Tools and Actions:
        1. GitHubTool: 
           - action: "search"
           - args: {{"query": "search term", "limit": 5}}
        2. WeatherTool:
           - action: "get_weather"
           - args: {{"city": "city name"}}
        
        User Query: "{user_query}"
        
        Create a logical plan to fulfill this request. Return a valid JSON representation following the Plan schema.
        """
        return self.llm_client.get_structured_output(prompt, Plan)
