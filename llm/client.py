import os
import json
import re
from typing import Type, Any

from dotenv import load_dotenv
from pydantic import BaseModel

from google import genai
from llm.logging_config import logger

load_dotenv()


class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = os.getenv("MODEL_NAME", "gemini-2.0-flash")

        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")

        # New SDK: create a client
        self.client = genai.Client(api_key=self.api_key)

    def _extract_json(self, text: str) -> str:
        """
        Tries to extract the first valid JSON object/array from a string.
        Helps when the model wraps JSON with extra text.
        """
        text = text.strip()

        # If it's already JSON, return fast
        if (text.startswith("{") and text.endswith("}")) or (text.startswith("[") and text.endswith("]")):
            return text

        # Try to find JSON object
        match_obj = re.search(r"\{[\s\S]*\}", text)
        if match_obj:
            return match_obj.group(0)

        # Try to find JSON array
        match_arr = re.search(r"\[[\s\S]*\]", text)
        if match_arr:
            return match_arr.group(0)

        raise ValueError("Could not extract JSON from model response.")

    def get_structured_output(self, prompt: str, response_model: Type[BaseModel]) -> Any:
        """
        Gets structured output from Gemini and validates using a Pydantic model.
        """
        logger.info(f"Requesting structured output for model: {response_model.__name__}")

        # Strongly instruct the model to output ONLY JSON
        schema = response_model.model_json_schema()

        system_prompt = (
            "You are a helpful AI assistant.\n"
            "Return ONLY valid JSON. No markdown, no code fences, no extra text.\n"
            "Your JSON must match this JSON Schema:\n"
            f"{json.dumps(schema, indent=2)}"
        )

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=f"{system_prompt}\n\nUSER_PROMPT:\n{prompt}",
        )

        # New SDK response usually has .text
        raw_text = getattr(response, "text", None)
        if not raw_text:
            raise ValueError("Empty response from model.")

        json_text = self._extract_json(raw_text)
        return response_model.model_validate_json(json_text)

    def get_completion(self, prompt: str, system_prompt: str = "You are a helpful AI assistant.") -> str:
        """
        Gets a standard text completion from Gemini.
        """
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=f"{system_prompt}\n\n{prompt}",
        )

        text = getattr(response, "text", None)
        if not text:
            raise ValueError("Empty response from model.")
        return text
