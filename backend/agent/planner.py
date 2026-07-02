from openai import OpenAI
import json
from backend.agent.prompts import PLANNER_PROMPT

client = OpenAI()

def create_plan(user_input: str, tool_results=None, chat_history=None):
    tool_results = tool_results or []
    chat_history = chat_history or []

    # Build conversation context from history
    history_context = ""
    if chat_history:
        history_context = "\n\nPrevious conversation:\n"
        for turn in chat_history[-3:]:  # only last 3 turns to avoid noise
            history_context += f"User: {turn['user']}\nBriefAI: {turn['assistant']}\n"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": PLANNER_PROMPT},
            {
                "role": "user",
                "content": json.dumps({
                    "user_input": user_input + history_context,
                    "tool_results": tool_results[-5:]
                })
            }
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    try:
        plan = json.loads(content)
    except Exception:
        return {"thought": "fallback due to parsing error", "tool": "none", "input": "", "done": True}

    plan["tool"] = plan.get("tool") or "none"
    plan["input"] = plan.get("input") or ""
    plan["done"] = plan.get("done", False)

    return plan