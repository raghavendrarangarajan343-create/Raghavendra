"""
Stateful Authorization Workflow Simulation
Mimicking LangGraph's StateGraph Architecture
"""

from typing import TypedDict, Dict, Any, Callable, List

# 1. Define the State Schema
class AuthState(TypedDict):
    """Represents the persistent state of the authorization flow."""
    request_id: str
    user_id: str
    action: str
    user_role: str
    is_authorized: bool
    audit_logs: List[str]
    final_output: str

# 2. Define Nodes (Tasks)
def initialize_state_node(state: AuthState) -> AuthState:
    print(f"[NODE] Initializing flow for Request: {state['request_id']}")
    state['audit_logs'].append("Flow initialized.")
    return state

def validate_role_node(state: AuthState) -> AuthState:
    print(f"[NODE] Validating role for User: {state['user_id']}")
    # Business Logic: Only 'admin' or 'super_user' can perform 'delete' actions
    if state['action'].startswith("delete"):
        state['is_authorized'] = state['user_role'] in ["admin", "super_user"]
    else:
        state['is_authorized'] = True
    
    status = "Authorized" if state['is_authorized'] else "Unauthorized"
    state['audit_logs'].append(f"Role validation complete: {status}")
    return state

def execute_action_node(state: AuthState) -> AuthState:
    print(f"[NODE] Executing action: {state['action']}")
    state['final_output'] = f"SUCCESS: Action '{state['action']}' performed for User {state['user_id']}."
    state['audit_logs'].append("Action executed successfully.")
    return state

def deny_access_node(state: AuthState) -> AuthState:
    print(f"[NODE] Access Denied for Action: {state['action']}")
    state['final_output'] = f"FAILURE: User {state['user_id']} is not permitted to '{state['action']}'."
    state['audit_logs'].append("Access denied and logged.")
    return state

# 3. Define the Router (Conditional Edge Logic)
def route_after_validation(state: AuthState) -> str:
    if state['is_authorized']:
        return "execute"
    return "deny"

# 4. Simulation of the Graph Runner
class SimpleStateGraph:
    def __init__(self):
        self.nodes: Dict[str, Callable] = {}
        self.edges: Dict[str, str] = {}
        self.conditional_edges: Dict[str, Callable] = {}

    def add_node(self, name: str, func: Callable):
        self.nodes[name] = func

    def run(self, initial_state: AuthState):
        state = initial_state
        
        # Static Execution Flow Simulation
        state = self.nodes["init"](state)
        state = self.nodes["validate"](state)
        
        # Conditional Routing
        next_node_key = route_after_validation(state)
        
        if next_node_key == "execute":
            state = self.nodes["execute"](state)
        else:
            state = self.nodes["deny"](state)
            
        print("\n--- FINAL STATE SUMMARY ---")
        print(f"Result: {state['final_output']}")
        print(f"Audit Trail: {' -> '.join(state['audit_logs'])}")
        return state

# 5. Execution
if __name__ == "__main__":
    workflow = SimpleStateGraph()
    workflow.add_node("init", initialize_state_node)
    workflow.add_node("validate", validate_role_node)
    workflow.add_node("execute", execute_action_node)
    workflow.add_node("deny", deny_access_node)

    print("--- SCENARIO 1: Admin Deleting Record ---")
    admin_state: AuthState = {
        "request_id": "REQ-001",
        "user_id": "U_123",
        "action": "delete_record",
        "user_role": "admin",
        "is_authorized": False,
        "audit_logs": [],
        "final_output": ""
    }
    workflow.run(admin_state)

    print("\n" + "="*40 + "\n")

    print("--- SCENARIO 2: Guest Trying to Delete ---")
    guest_state: AuthState = {
        "request_id": "REQ-002",
        "user_id": "U_456",
        "action": "delete_record",
        "user_role": "guest",
        "is_authorized": False,
        "audit_logs": [],
        "final_output": ""
    }
    workflow.run(guest_state)
