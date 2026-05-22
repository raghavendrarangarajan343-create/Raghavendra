from typing import TypedDict, List, Dict, Any

class CompanyIntelligenceState(TypedDict):
    company_name: str
    research_outputs: List[Dict[str, Any]]
    consolidated_data: Dict[str, Any]
    validation_errors: List[str]
    retry_count: int
    final_status: str
