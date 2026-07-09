from openai import OpenAI
import ollama
import json
from backend.agent.prompts import PLANNER_PROMPT


def create_plan(user_input: str, tool_results=None, chat_history=None, api_key=None, mode="openai"):
    tool_results = tool_results or []
    chat_history = chat_history or []

    history_context = ""
    if chat_history:
        history_context = "\n\nPrevious conversation:\n"
        for turn in chat_history[-3:]:
            history_context += f"User: {turn['user']}\nBriefAI: {turn['assistant']}\n"

    messages = [
        {"role": "system", "content": PLANNER_PROMPT},
        {
            "role": "user",
            "content": json.dumps({
                "user_input": user_input + history_context,
                "tool_results": tool_results[-5:]
            })
        }
    ]

    if mode == "local":
        from backend.agent.hardware import get_best_model, ensure_model_available
        model_name, _ = get_best_model()
        ensure_model_available(model_name)
        response = ollama.chat(
            model=model_name,
            messages=messages,
            options={"temperature": 0}
        )
        content = response["message"]["content"]
    else:
        client = OpenAI(api_key=api_key) if api_key else OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0
        )
        content = response.choices[0].message.content

    try:
        # Strip markdown code fences if model wraps JSON in them
        content = content.strip()
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        plan = json.loads(content.strip())
    except Exception:
        return {"thought": "fallback due to parsing error", "tool": "none", "input": "", "done": True}

    plan["tool"] = plan.get("tool") or "none"
    plan["input"] = plan.get("input") or ""
    plan["done"] = plan.get("done", False)

    return plan