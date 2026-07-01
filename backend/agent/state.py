from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AgentState:
    user_input: str
    plan: Dict[str, Any]

    tool_results: List[Dict[str, Any]] = field(default_factory=list)

    # NEW: store reasoning/debug trace
    reasoning_log: List[str] = field(default_factory=list)

    # NEW: allows replanning later
    current_step_index: int = 0

    final_response: Optional[str] = None