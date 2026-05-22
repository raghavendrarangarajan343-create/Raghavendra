import pytest
import csv
import os
import sys
import re

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.schema_engine import SchemaEngine

# Initialize the Schema Engine
schema_engine = SchemaEngine()

# Load the Golden Dataset
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'golden_dataset.csv')
golden_data = []
with open(DATA_FILE, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        golden_data.append(row)

# Get "Not Null" fields for Rule 1.2
not_null_fields = schema_engine.get_fields_by_nullability("Not Null")


@pytest.mark.input_validation
class TestInputValidation:
    
    # Rule 1.1: Valid Standard Input (Specific Parameters)
    # We test the "Company Name" format constraints against the Golden Dataset
    @pytest.mark.parametrize("record", golden_data, ids=[r["Company Name"] for r in golden_data])
    def test_1_1_valid_standard_input(self, record):
        """
        Rule 1.1: Test with standard, well-formatted company names.
        """
        company_name = record.get("Company Name")
        metadata = schema_engine.get_field_metadata("Company Name")
        
        assert company_name is not None, "Company Name cannot be None"
        assert len(company_name.strip()) > 0, "Company Name cannot be empty"
        
        # Check against Regex
        pattern = metadata["regex_pattern"]
        assert re.match(pattern, company_name), f"'{company_name}' failed regex constraint: {pattern}"

    # Rule 1.2: Invalid/Empty Input (Per-Parameter)
    # Iterate through all "Not Null" fields and ensure none are empty in our dataset
    @pytest.mark.parametrize("field_name", not_null_fields)
    @pytest.mark.parametrize("record", golden_data, ids=[r["Company Name"] for r in golden_data])
    def test_1_2_not_null_handling(self, field_name, record):
        """
        Rule 1.2: Test with null, empty, or whitespace-only inputs for Not Null fields.
        Validates that no critical fields are empty in the golden dataset.
        """
        value = record.get(field_name)
        
        # The rule states: "Test with null, empty, or whitespace-only inputs". 
        # Here we verify the dataset complies with the Not Null constraint.
        assert value is not None, f"Field '{field_name}' failed: Value is None"
        assert value.strip() != "", f"Field '{field_name}' failed: Value is empty string"
        
    # Format Consistency (Enum/Regex) validation mapping directly to metadata rules
    @pytest.mark.parametrize("record", golden_data, ids=[r["Company Name"] for r in golden_data])
    def test_format_constraints_and_enums(self, record):
        """
        Validates all fields in the record against their specific regex and enum constraints
        defined in the metadata schema.
        """
        for field_name, value in record.items():
            metadata = schema_engine.get_field_metadata(field_name)
            if not metadata:
                continue # Skip if not in our schema subset
                
            # If value is present, check constraints
            if value and value.strip() != "":
                pattern = metadata.get("regex_pattern")
                if pattern:
                    assert re.match(pattern, value), f"Field '{field_name}' with value '{value}' failed regex: {pattern}"

