"""
CLI Interface for CPG Decision Support Agent
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.decision_agent import DecisionSupportAgent


def run_cli():
    print("=" * 60)
    print("CPG Decision Support Agent")
    print("Type 'exit' to quit")
    print("=" * 60)

    agent = DecisionSupportAgent()

    while True:
        user_input = input("\nBusiness Question > ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("\nExiting Decision Support Agent. Goodbye!")
            break

        try:
            response = agent.ask(user_input)
            print("\n--- Agent Response ---")
            print(response)
        except Exception as e:
            print("\n[ERROR]")
            print(str(e))


if __name__ == "__main__":
    run_cli()
