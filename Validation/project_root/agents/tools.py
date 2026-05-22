import os
import sys
import re
from langchain_core.tools import tool

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.schema_engine import SchemaEngine
from validators.base_validators import RegexValidator

# Initialize schema engine
engine = SchemaEngine()

@tool
def validate_company_data(data: dict) -> list[str]:
    """
    Validates a consolidated company data dictionary against the schema rules.
    Returns a list of error strings. If the list is empty, validation passed.
    """
    errors = []
    
    # 1. Check for required fields
    required_fields = engine.get_fields_by_nullability("Not Null")
    for req in required_fields:
        val = data.get(req)
        if val is None or str(val).strip() == "":
            errors.append(f"Missing or empty required field: {req}")

    # 2. Check regex patterns for all provided fields
    for field_name, value in data.items():
        meta = engine.get_field_metadata(field_name)
        if not meta:
            continue
            
        # Skip empty values since they are either caught by nullability check or allowed
        if value is None or str(value).strip() == "":
            continue
            
        pattern = meta.get("regex_pattern")
        if pattern:
            try:
                # Our RegexValidator raises ValueError if it doesn't match
                RegexValidator.validate(value, pattern)
            except ValueError:
                errors.append(f"Field '{field_name}' invalid: value '{value}' does not match pattern '{pattern}'")
                
    return errors
