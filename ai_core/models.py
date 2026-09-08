from pydantic import BaseModel, Field, model_validator
from typing import Dict, Any, List, Optional


class ToolCall(BaseModel):
    tool_name: str
    arguments: Dict[str, Any] = Field(default_factory=dict)


class ToolPlan(BaseModel):
    response: Optional[str] = ""
    tool_calls: List[ToolCall] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def handle_message_alias(cls, data: Any):
        if isinstance(data, dict):
            if not data.get("response") and data.get("message"):
                data["response"] = data["message"]
        return data
