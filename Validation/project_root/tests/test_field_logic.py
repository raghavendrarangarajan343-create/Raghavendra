import pytest
from validators.base_validators import ClassificationValidator

@pytest.mark.all_fields
@pytest.mark.parametrize("test_id, description, input_data, expected", [
    ("TC_14.4_001", "Validate that inappropriate default values are NOT assigned to critical or measurable fields (e.g., financials, metrics, counts)", "{ \"Annual Revenues\": \"$0\", \"Employee Size\": \"0\", \"Website Traffic Rank\": \"0\" }", "❌ Fail – As per business_rules, measurable fields must not default to misleading values like 0 unless explicitly valid. Validation should flag incorrect defaults."),
    ("TC_14.4_002", "Validate that nullable descriptive or categorical fields can use safe defaults like \"Unknown\" where allowed", "{ \"Remote Work Policy\": \"Unknown\", \"Vision\": null }", "✅ Pass – Nullable fields with no strict business_rules can default to \"Unknown\" or remain null per nullability rules."),
    ("TC_14.4_003", "Validate that NOT NULL fields never receive default placeholders like \"N/A\", \"Unknown\", or empty strings", "{ \"Company Name\": \"Unknown\", \"Category\": \"N/A\" }", "❌ Fail – Violates Not Null + business_rules requiring valid, real values (e.g., official registry match, enum constraint)."),
    ("TC_14.4_004", "Validate that default values do not violate format_constraints or regex patterns", "{ \"Website URL\": \"Unknown\", \"CEO LinkedIn URL\": \"N/A\" }", "❌ Fail – Invalid format; does not match required regex (HTTPS URL patterns)."),
    ("TC_14.4_005", "Validate context-aware defaulting: derived or calculated fields must NOT be defaulted arbitrarily", "{ \"CAC:LTV Ratio\": \"0\", \"Runway\": \"0\" }", "❌ Fail – Derived metrics must be computed or null; defaulting to 0 violates data_rules and business logic."),
    ("TC_14.4_006", "Validate that optional list/text fields can remain null instead of forced defaults", "{ \"Awards & Recognitions\": \"N/A\", \"Case Studies\": \"None\" }", "❌ Fail – Should be null instead of forced placeholders per nullability rules."),
    ("TC_14.4_007", "Validate that enum-based fields do not accept invalid default placeholders", "{ \"Nature of Company\": \"Unknown\", \"Profitability Status\": \"N/A\" }", "❌ Fail – Must match strict enum values defined in regex_pattern."),
    ("TC_14.4_008", "Validate that numeric fields respect domain constraints even when defaulted", "{ \"Employee Turnover\": \"150%\", \"Market Share (%)\": \"-10%\" }", "❌ Fail – Violates range constraints (0–100%) defined in business_rules."),
    ("TC_14.4_009", "Validate that valid contextual defaults are applied only where business-safe", "{ \"Decision Maker Accessibility\": \"Low - Not publicly reachable\" }", "✅ Pass – Matches allowed enum prefix + descriptive extension per regex and business_rules."),
    ("TC_14.4_010", "Validate that system avoids over-defaulting and preserves data integrity by leaving unknowns null", "{ \"Glassdoor Rating\": null, \"Indeed Rating\": null }", "✅ Pass – Nullable fields should remain null instead of forced defaults, preserving data accuracy"),
    ("TC-14.4-11", "Mixed Data Type Load: Validate token handling across text, numeric, and URL fields", "Large text + multiple URLs + numeric metrics", "Pass: No truncation across any data type; all formats preserved"),
    ("TC-14.4-12", "Pipeline Integrity: Validate full record survives ingestion → validation → output without truncation", "Full dataset (150+ fields populated)", "Pass: No data loss across pipeline stages; aligns with validation_mode (Automated/Manual)"),
])
def test_field_logic_and_integrity(test_id, description, input_data, expected):
    """
    Validates field-level logic, defaults, nullability, and pipeline integrity.
    """
    print(f"\nRunning {test_id}: {description}")
    ClassificationValidator.validate(input_data, expected)
