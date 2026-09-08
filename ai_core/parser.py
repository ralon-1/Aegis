import json
import re
from pydantic import ValidationError

from ai_core.models import ToolCall, ToolPlan


def clean_json_string(text: str) -> str:
    text = text.strip()
    # First try to extract from markdown fences
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        return match.group(1).strip()
    
    # If no fences, try to extract the outermost JSON object
    start_idx = text.find('{')
    end_idx = text.rfind('}')
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        return text[start_idx:end_idx+1]

    return text


def parse_tool_call(response: str):
    try:
        cleaned = clean_json_string(response)
        data = json.loads(cleaned)
        tool_call = ToolCall(**data)
        return tool_call

    except json.JSONDecodeError:
        print("Error: AI returned invalid JSON")
        return None

    except ValidationError as e:
        print("Error: Invalid tool structure")
        print(e)
        return None


def parse_tool_plan(response: str):
    try:
        cleaned = clean_json_string(response)
        data = json.loads(cleaned)
        plan = ToolPlan(**data)
        return plan

    except json.JSONDecodeError:
        # If the AI responded with plain text conversational response, wrap it cleanly in ToolPlan
        if response and not response.strip().startswith("{"):
            return ToolPlan(response=response.strip(), tool_calls=[])
        print("Error: AI returned invalid JSON")
        return None

    except ValidationError as e:
        print("Error: Invalid tool plan")
        print(e)
        return None