from backend.agent.agent import run_agent
import json

def main():
    print("\nAutonomOS AI Agent Started")
    print("Type 'exit' to quit\n")

    while True:
        user_input = input("> ")

        if user_input.lower() in ["exit", "quit"]:
            print("Shutting down AutonomOS...")
            break

        try:
            result = run_agent(user_input)

            # Updated keys to match run_agent output
            print("\n--- EXECUTION TRACE ---")
            print(json.dumps(result["execution_trace"], indent=2))

            print("\n--- SUMMARY ---")
            print(json.dumps(result["summary"], indent=2))

            print("\n--- FINAL RESPONSE ---")
            print(result["final_response"])
            print("\n")

        except Exception as e:
            print("ERROR:", e)

if __name__ == "__main__":
    main()