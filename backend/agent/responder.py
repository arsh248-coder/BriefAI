from openai import OpenAI
from backend.agent.prompts import RESPONDER_PROMPT

client = OpenAI()

def generate_response(user_input, tool_results, chat_history=None):
    chat_history = chat_history or []

    history_context = ""
    if chat_history:
        history_context = "\n\nPrevious conversation for context:\n"
        for turn in chat_history[-3:]:
            history_context += f"User: {turn['user']}\nBriefAI: {turn['assistant']}\n"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
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
        ],
        temperature=0.3
    )

    return response.choices[0].message.content