from openai import OpenAI
from backend.agent.prompts import RESPONDER_PROMPT

client = OpenAI()

def generate_response(user_input, tool_results):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": RESPONDER_PROMPT},
            {
                "role": "user",
                "content": f"""
User request:
{user_input}

Tool results:
{tool_results}
"""
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content