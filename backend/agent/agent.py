from backend.agent.planner import create_plan
from backend.agent.tools import list_documents, read_pdf, read_text_file, read_word_file
from backend.agent.responder import generate_response
import time

TOOLS = {
    "list_documents": list_documents,
    "read_pdf": read_pdf,
    "read_word_file": read_word_file,
    "read_text_file": read_text_file
}


# ---------------------------
# HELPERS
# ---------------------------

def log_step(step):
    print("\n🧠 STEP:")
    print(step)
    time.sleep(0.2)


def build_timeline(tool_results):
    timeline = []

    for item in tool_results:
        if "thought" in item:
            timeline.append({
                "type": "reasoning",
                "content": item["thought"]
            })

        elif "output" in item:
            timeline.append({
                "type": "tool_output",
                "tool": item.get("tool"),
                "content": str(item["output"])[:300]
            })

        elif "error" in item:
            timeline.append({
                "type": "error",
                "content": item["error"]
            })

    return timeline


# ---------------------------
# MAIN AGENT LOOP
# ---------------------------

def run_agent(user_input: str):

    tool_results = []
    max_steps = 8
    current_input = user_input

    for step_num in range(max_steps):

        # 1. PLAN
        decision = create_plan(current_input, tool_results)

        tool_name = decision.get("tool") or "none"
        tool_input = decision.get("input") or ""
        thought = decision.get("thought")
        done = decision.get("done", False)

        # 2. LOG REASONING
        step_log = {
            "step": step_num,
            "thought": thought,
            "tool": tool_name,
            "input": tool_input
        }

        tool_results.append(step_log)
        log_step(step_log)

        # 3. STOP CONDITION
        if done or tool_name == "none":
            tool_results.append({
                "step": step_num,
                "status": "stopped",
                "reason": "planner_finished"
            })
            break

        # 4. TOOL VALIDATION
        if tool_name not in TOOLS:
            tool_results.append({
                "step": step_num,
                "error": f"Unknown tool: {tool_name}"
            })
            break

        # 5. TOOL EXECUTION
        try:
            output = TOOLS[tool_name](tool_input)

            tool_results.append({
                "step": step_num,
                "tool": tool_name,
                "input": tool_input,
                "output": output
            })

            # 6. FEEDBACK LOOP
            current_input = f"""
User goal: {user_input}

Previous thought: {thought}

Latest observation:
{output}
"""

        except Exception as e:
            tool_results.append({
                "step": step_num,
                "tool": tool_name,
                "error": str(e)
            })
            break

    # 7. FINAL RESPONSE
    final_response = generate_response(user_input, tool_results)

    return {
        "user_input": user_input,
        "execution_trace": tool_results,
        "timeline": build_timeline(tool_results),
        "final_response": final_response,
        "summary": {
            "total_steps": len(tool_results),
            "tools_used": list(set([
                t.get("tool") for t in tool_results if "tool" in t
            ]))
        }
    }