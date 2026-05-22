import os
import json
from typing import Any
import asyncio
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from agents.state import CompanyIntelligenceState
from agents.tools import validate_company_data

# Initialize LLMs (Using OpenAI as requested/defaulted)
# We will use temperature variations to simulate different agents
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

def is_mock_mode():
    key = os.environ.get("OPENAI_API_KEY")
    return not key or key == "your_openai_api_key_here"

async def research_node(state: CompanyIntelligenceState) -> dict[str, Any]:
    """Runs 3 parallel research agents."""
    print("--- RESEARCH AGENT ---")
    company_name = state["company_name"]
    
    if is_mock_mode():
        print("Using MOCK research data (No API Key provided)")
        return {
            "research_outputs": [
                {"source": "Financial Analyst", "data": f"{company_name} generates around $383 billion in revenue and operates as a large Enterprise."},
                {"source": "HR Specialist", "data": f"{company_name} has over 164,000 employees globally. They currently enforce an On-Site work policy."},
                {"source": "General Researcher", "data": f"{company_name} is a leading Enterprise in the tech industry."}
            ]
        }
    
    # Define 3 perspectives
    prompts = [
        ChatPromptTemplate.from_messages([
            ("system", "You are a Financial Analyst. Provide insights on {company}'s revenue and business category. Be concise."),
            ("user", "Research {company}")
        ]),
        ChatPromptTemplate.from_messages([
            ("system", "You are an HR Specialist. Provide insights on {company}'s employee size and remote work policy. Be concise."),
            ("user", "Research {company}")
        ]),
        ChatPromptTemplate.from_messages([
            ("system", "You are a General Business Researcher. Provide a brief overview of {company} including category and size. Be concise."),
            ("user", "Research {company}")
        ])
    ]
    
    # Run them in parallel
    async def fetch_insight(prompt):
        chain = prompt | llm
        response = await chain.ainvoke({"company": company_name})
        return {"source": "LLM Researcher", "data": response.content}
        
    results = await asyncio.gather(*[fetch_insight(p) for p in prompts])
    
    return {"research_outputs": list(results)}

def consolidation_node(state: CompanyIntelligenceState) -> dict[str, Any]:
    """Merges research into a final JSON adhering to the schema."""
    print("--- CONSOLIDATION AGENT ---")
    company_name = state["company_name"]
    raw_data = state["research_outputs"]
    errors = state.get("validation_errors", [])
    
    if is_mock_mode():
        print("Using MOCK consolidation (No API Key provided)")
        # In mock mode, if we have a retry, let's pretend the LLM fixed the issue
        if errors:
            print("MOCK: Fixing previous validation errors...")
        return {
            "consolidated_data": {
                "Company Name": company_name,
                "Category": "Enterprise",
                "Annual Revenues": "$383,000,000,000",
                "Employee Size": "164000",
                "Remote Work Policy": "On-Site"
            }
        }
    
    parser = JsonOutputParser()
    
    system_msg = """
    You are a Consolidation Agent. Your job is to take raw research data from multiple sources 
    and consolidate it into a single JSON object.
    
    The JSON must contain EXACTLY these keys:
    - "Company Name" (String, e.g. 'Apple Inc.')
    - "Category" (String, MUST BE ONE OF: Startup, MSME, SMB, Enterprise, Investor, VC, Conglomerate)
    - "Annual Revenues" (String, e.g. '$10,000,000' or '1000000')
    - "Employee Size" (String, e.g. '11-50' or '500')
    - "Remote Work Policy" (String, MUST START WITH ONE OF: Remote, Hybrid, On-Site, Office-First)
    """
    
    if errors:
        system_msg += f"\n\nPREVIOUS VALIDATION ERRORS (Fix these!):\n{chr(10).join(errors)}"
        
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_msg),
        ("user", "Company: {company}\nRaw Data:\n{data}\n\nOutput strict JSON.")
    ])
    
    chain = prompt | llm | parser
    
    # Note: we use sync invoke here for simplicity in LangGraph
    result = chain.invoke({"company": company_name, "data": json.dumps(raw_data)})
    
    return {"consolidated_data": result}

def validation_node(state: CompanyIntelligenceState) -> dict[str, Any]:
    """Validates the consolidated data using the validation suite tool."""
    print("--- VALIDATION AGENT ---")
    data = state["consolidated_data"]
    
    # Call our LangChain tool
    errors = validate_company_data.invoke({"data": data})
    
    if errors:
        print(f"Validation Failed with {len(errors)} errors:")
        for err in errors:
            print(f" - {err}")
    else:
        print("Validation Passed!")
        
    return {"validation_errors": errors, "retry_count": state.get("retry_count", 0) + 1}

import re

def save_node(state: CompanyIntelligenceState) -> dict[str, Any]:
    """Persists data to Supabase (Mocked if credentials missing)."""
    print("--- SAVE & VALIDATION AGENT (PERSIST) ---")
    data = state["consolidated_data"]
    
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        print(f"WARN: Supabase credentials missing. Mocking save for: {data.get('Company Name')}")
        return {"final_status": "saved_mock"}
        
    try:
        from supabase import create_client
        client = create_client(supabase_url, supabase_key)
        
        # Convert keys to snake_case for PostgreSQL
        def to_snake_case(name):
            return name.lower().replace(" ", "_").replace("-", "_")
            
        db_data = {to_snake_case(k): v for k, v in data.items()}
        
        # Assuming table is named 'companies'
        client.table("companies").insert(db_data).execute()
        print("Successfully saved to Supabase!")
        return {"final_status": "saved"}
    except Exception as e:
        print(f"Error saving to Supabase: {e}")
        return {"final_status": "failed"}
