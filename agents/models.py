from pydantic import BaseModel
from typing import List, Optional

class ToolArgs(BaseModel):
    query: Optional[str] = None
    limit: Optional[int] = None
    city: Optional[str] = None

class Step(BaseModel):
    id: int
    description: str
    tool: str
    action: str
    args: ToolArgs

class Plan(BaseModel):
    goal: str
    steps: List[Step]

class VerificationResult(BaseModel):
    is_complete: bool
    summary: str
    missing_info: Optional[str] = None
    final_output: str
