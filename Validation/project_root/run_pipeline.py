import os
import sys
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from agents.graph import build_graph

async def main():
    if len(sys.argv) < 2:
        print("Usage: python run_pipeline.py \"Company Name\"")
        sys.exit(1)
        
    company_name = sys.argv[1]
    print(f"Starting Company Intelligence Pipeline for: {company_name}")
    
    # Check OpenAI API Key
    openai_key = os.environ.get("OPENAI_API_KEY")
    if not openai_key or openai_key == "your_openai_api_key_here":
        print("WARN: OPENAI_API_KEY is not set. Running in MOCK MODE for demonstration.")
        
    app = build_graph()
    
    # Initial state
    initial_state = {
        "company_name": company_name,
        "research_outputs": [],
        "consolidated_data": {},
        "validation_errors": [],
        "retry_count": 0,
        "final_status": "pending"
    }
    
    # We use stream to show the progression through nodes
    print("\n[Pipeline Execution Started]")
    async for output in app.astream(initial_state, stream_mode="updates"):
        for node_name, state_update in output.items():
            print(f"\n--- Completed Node: {node_name} ---")
            if "validation_errors" in state_update and node_name == "validate":
                if not state_update["validation_errors"]:
                    print("Status: Validation Passed!")
                else:
                    print(f"Status: Validation Failed with {len(state_update['validation_errors'])} errors")
            
            if "final_status" in state_update and node_name == "save":
                print(f"Status: Persistence {state_update['final_status']}")

if __name__ == "__main__":
    asyncio.run(main())
