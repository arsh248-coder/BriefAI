from openai import OpenAI
import ollama
from backend.agent.prompts import RESPONDER_PROMPT


def generate_response(user_input, tool_results, chat_history=None, api_key=None, mode="openai"):
    chat_history = chat_history or []

    history_context = ""
    if chat_history:
        history_context = "\n\nPrevious conversation for context:\n"
        for turn in chat_history[-3:]:
            history_context += f"User: {turn['user']}\nBriefAI: {turn['assistant']}\n"

    messages = [
        {"role": "system", "content": RESPONDER_PROMPT},
        {
            "role": "user",
            "content": f"""
User request:
{user_input}
{history_context}
Tool results:
{tool_results}
"""
        }
    ]

    if mode == "local":
        from backend.agent.hardware import get_best_model, ensure_model_available
        model_name, _ = get_best_model()
        ensure_model_available(model_name)
        response = ollama.chat(
            model=model_name,
            messages=messages,
            options={"temperature": 0.3}
        )
        return response["message"]["content"]
    else:
        client = OpenAI(api_key=api_key) if api_key else OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.3
        )
        return response.choices[0].message.content