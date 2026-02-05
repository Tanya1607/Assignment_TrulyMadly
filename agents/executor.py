from typing import List, Dict, Any
from agents.models import Plan, Step
from tools.github_tool import GitHubTool
from tools.weather_tool import WeatherTool
from llm.logging_config import logger

class ExecutorAgent:
    def __init__(self):
        self.tools = {
            "GitHubTool": GitHubTool(),
            "WeatherTool": WeatherTool()
        }

    def execute_plan(self, plan: Plan) -> List[Dict[str, Any]]:
        logger.info(f"Executing plan for goal: {plan.goal}")
        results = []
        for step in plan.steps:
            tool_name = step.tool
            action = step.action
            args = step.args
            
            logger.info(f"Executing step {step.id}: {step.description} (Tool: {tool_name}, Action: {action})")
            
            if tool_name in self.tools:
                try:
                    # Convert Pydantic model to dict, excluding None values
                    args_dict = args.model_dump(exclude_none=True)
                    output = self.tools[tool_name].run(action, **args_dict)
                    results.append({
                        "step_id": step.id,
                        "description": step.description,
                        "tool": tool_name,
                        "output": output
                    })
                except Exception as e:
                    results.append({
                        "step_id": step.id,
                        "description": step.description,
                        "tool": tool_name,
                        "error": str(e)
                    })
            else:
                results.append({
                    "step_id": step.id,
                    "description": step.description,
                    "tool": tool_name,
                    "error": f"Tool {tool_name} not found"
                })
        return results
