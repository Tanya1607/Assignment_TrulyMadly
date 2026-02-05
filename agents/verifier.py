from llm.client import LLMClient
from agents.models import VerificationResult
from typing import List, Dict, Any
from llm.logging_config import logger

class VerifierAgent:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def verify_and_finalize(self, user_query: str, execution_results: List[Dict[str, Any]]) -> VerificationResult:
        logger.info("Starting verification and final output formatting.")
        prompt = f"""
        You are a Verifier Agent for an AI Operations Assistant.
        Your task is to review the execution results of a plan and provide a final answer to the user.
        
        User Query: "{user_query}"
        
        Execution Results:
        {execution_results}
        
        1. Check if all parts of the user query have been addressed.
        2. If information is missing or there were errors, state it clearly.
        3. Format the final output neatly for the user.
        
        Return a valid JSON representation following the VerificationResult schema.
        """
        return self.llm_client.get_structured_output(prompt, VerificationResult)
