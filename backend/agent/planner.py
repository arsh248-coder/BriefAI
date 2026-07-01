from openai import OpenAI
import json
from backend.agent.prompts import PLANNER_PROMPT

client = OpenAI()


def create_plan(user_input: str, tool_results=None):
    tool_results = tool_results or []

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": PLANNER_PROMPT},
            {
                "role": "user",
                "content": json.dumps({
                    "user_input": user_input,
                    "tool_results": tool_results[-5:]  # IMPORTANT: limit noise
                })
            }
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    try:
        plan = json.loads(content)
    except Exception:
        return {
            "thought": "fallback due to parsing error",
            "tool": "none",
            "input": "",
            "done": True
        }

    # HARD SANITIZATION
    plan["tool"] = plan.get("tool") or "none"
    plan["input"] = plan.get("input") or ""
    plan["done"] = plan.get("done", False)

    return plan