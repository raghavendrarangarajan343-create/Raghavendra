import pytest
import re

class DefaultValueValidator:
    """
    Entity-level validator to check for inappropriate defaults across all parameters.
    """
    @staticmethod
    def validate_entity_defaults(entity_data):
        errors = []

        # 1. Inappropriate Default: Annual Revenues should not default to $0
        # If the revenue is strictly $0, it might be an improper default rather than actual zero revenue.
        revenue = entity_data.get("Annual Revenues")
        if revenue in ["$0", "0", "$0.00"]:
            errors.append("Validation Error: 'Annual Revenues' should not default to $0. Keep it Null if unknown.")

        # 2. Inappropriate Default: Employee Turnover should not default to 0%
        turnover = entity_data.get("Employee Turnover")
        if turnover in ["0%", "0.0%"]:
            errors.append("Validation Error: 'Employee Turnover' should not default to 0%. Keep it Null if unknown.")

        # 3. Appropriate Default: Legal Issues / Controversies can be "N/A"
        legal_issues = entity_data.get("Legal Issues / Controversies")
        if legal_issues is not None:
            # Check against the regex `^(N/A|...)` conceptually
            if legal_issues == "N/A":
                pass # This is an acceptable default as per format constraints

        # 4. Inappropriate Default: Year of Incorporation shouldn't be defaulted to a generic placeholder like 1900 
        # (unless actually verified) but let's check for 0 or 9999
        yoi = entity_data.get("Year of Incorporation")
        if yoi in [0, 9999]:
            errors.append(f"Validation Error: 'Year of Incorporation' has invalid default {yoi}.")

        if errors:
            raise ValueError("\n".join(errors))
        return True


@pytest.mark.all_parameters
@pytest.mark.null_handling
class TestDefaultValueHandling:
    
    @pytest.mark.parametrize("test_id, description, entity_data, expected_pass", [
        (
            "TC_DEF_01",
            "Reject inappropriate default: Revenue = $0",
            {
                "Company Name": "TechCorp",
                "Annual Revenues": "$0"
            },
            False
        ),
        (
            "TC_DEF_02",
            "Reject inappropriate default: Employee Turnover = 0%",
            {
                "Company Name": "TechCorp",
                "Employee Turnover": "0%"
            },
            False
        ),
        (
            "TC_DEF_03",
            "Accept appropriate default: Legal Issues = N/A",
            {
                "Company Name": "TechCorp",
                "Legal Issues / Controversies": "N/A",
                "Annual Revenues": "$10,000,000"
            },
            True
        ),
        (
            "TC_DEF_04",
            "Accept nulls where defaults shouldn't be used (Context-dependent)",
            {
                "Company Name": "TechCorp",
                "Annual Revenues": None,
                "Employee Turnover": None
            },
            True
        )
    ])
    def test_entity_default_values(self, test_id, description, entity_data, expected_pass):
        """
        Validates entity-level data for appropriate vs inappropriate default values.
        """
        print(f"\nRunning {test_id}: {description}")
        
        if expected_pass:
            # Should pass without raising ValueError
            DefaultValueValidator.validate_entity_defaults(entity_data)
            assert True
        else:
            # Should raise ValueError due to inappropriate default
            with pytest.raises(ValueError) as excinfo:
                DefaultValueValidator.validate_entity_defaults(entity_data)
            print(f"Caught expected error: {excinfo.value}")

