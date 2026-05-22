import pytest
from validators.base_validators import ClassificationValidator

@pytest.mark.category
@pytest.mark.parametrize("test_id, description, input_data, expected", [
    ("TC_12.1_01", "Validate correct classification for Startup-stage company", "Startup", "✅ Accepted. Matches regex ^(Startup|MSME|SMB|Enterprise|Investor|VC|Conglomerate)$ and aligns with business rule (taxonomy mapping)."),
    ("TC_12.1_02", "Validate classification for MSME based on small-scale company", "MSME", "✅ Accepted. Valid enum and passes \"Value In List check\" (Automated validation)."),
    ("TC_12.1_03", "Validate classification for SMB (mid-sized company)", "SMB", "✅ Accepted. Matches allowed enum list and satisfies classification taxonomy rule."),
    ("TC_12.1_04", "Validate classification for Venture Capital firm", "VC", "✅ Accepted. Correct classification for investor-type entity per business rules."),
    ("TC_12.1_05", "Validate classification for Investor entity", "Investor", "✅ Accepted. Matches enum and aligns with business taxonomy."),
    ("TC_12.1_06", "Reject invalid classification outside enum", "SmallBiz", "❌ Rejected. Fails regex and \"Value In List check\"."),
    ("TC_12.1_07", "Reject incorrect casing if strict enum enforcement applied", "startup", "❌ Rejected if case-sensitive. Should normalize or enforce exact enum match."),
    ("TC_12.1_13", "Validate Enterprise classification", "Enterprise", "✅ Accepted. Matches enum and taxonomy rule-12.1 test case"),
])
def test_company_category(test_id, description, input_data, expected):
    """
    Validates company category classification against allowed enums and regex.
    """
    print(f"\nRunning {test_id}: {description}")
    ClassificationValidator.validate(input_data, expected)

@pytest.mark.category
@pytest.mark.parametrize("test_id, description, input_data, expected", [
    ("TC-12.3-11", "Cross-field Consistency: Ensure Category aligns with Nature of Company.", "Category=Startup, Nature=Public", "Fail: Logical inconsistency (Startup typically Private)."),
    ("TC-12.3-12", "Cross-field Validation: Accept valid Category & Nature combinations.", "Category=Enterprise, Nature=Public", "Pass: Valid mapping."),
])
def test_category_cross_field(test_id, description, input_data, expected):
    """
    Validates consistency between Category and Nature of Company.
    """
    print(f"\nRunning {test_id}: {description}")
    ClassificationValidator.validate(input_data, expected)

@pytest.mark.nature_of_company
@pytest.mark.parametrize("test_id, description, input_data, expected", [
    ("TC_12.1_10", "Validate VC classification aligns with company nature", "Private + Category=VC", "⚠️ Conditional: Accepted if entity is a VC firm structured as private. Requires cross-field validation."),
    ("TC_12.1_11", "Detect mismatch: Non-Profit classified as VC", "Non-Profit + Category=VC", "❌ Rejected. Violates logical classification consistency."),
    ("TC-12.3-01", "Valid Classification: Verify Private companies are correctly identified.", "SpaceX → Private", "Pass: Matches enum `(Private, Public, Subsidiary, Govt, Joint Venture)`."),
    ("TC-12.3-02", "Valid Classification: Verify Public companies are correctly identified.", "Apple → Public", "Pass: Valid classification; aligns with legal filings."),
    ("TC-12.3-03", "Valid Classification: Verify Subsidiary companies are correctly identified.", "WhatsApp → Subsidiary", "Pass: Correct parent-child ownership classification."),
    ("TC-12.3-04", "Invalid Classification: Reject values outside predefined enums.", "Startup", "Fail: Not in allowed enum list."),
    ("TC-12.3-05", "Case Sensitivity Check: Ensure standardized enum format is enforced.", "private", "Fail: Should match exact enum (or normalized)."),
    ("TC-12.3-06", "Null Handling: Ensure field does not accept null values.", "NULL", "Fail: Field is Not Null (business rule violation)."),
    ("TC-12.3-07", "Special Character Validation: Reject invalid characters in classification.", "Private@123", "Fail: Violates regex constraint."),
    ("TC-12.3-08", "Multi-value Rejection: Ensure only single classification is allowed.", "Private/Public", "Fail: Violates granularity (One per Entity)."),
    ("TC-12.3-09", "Whitespace Handling: Ensure trimming of leading/trailing spaces.", "\" Public \"", "Pass: Trimmed → \"Public\"; matches enum."),
    ("TC-12.3-10", "Boundary Enum Validation: Validate acceptance of all allowed enum values.", "Govt", "Pass: Valid enum value accepted."),
])
def test_nature_of_company(test_id, description, input_data, expected):
    """
    Validates nature of company classification and constraints.
    """
    print(f"\nRunning {test_id}: {description}")
    ClassificationValidator.validate(input_data, expected)

@pytest.mark.global_record
@pytest.mark.parametrize("test_id, description, input_data, expected", [
    ("TC-12.3-13", "Entity Validation: Ensure classification aligns with external trusted data sources.", "Tesla → Public", "Pass: Matches SEC/registry data."),
    ("TC-12.3-14", "Classification Completeness: Ensure every entity has a valid Nature of Company.", "Missing field", "Fail: Mandatory field missing---12.3 test case"),
])
def test_classification_global_record(test_id, description, input_data, expected):
    """
    Validates classification against global record consistency rules.
    """
    print(f"\nRunning {test_id}: {description}")
    ClassificationValidator.validate(input_data, expected)

@pytest.mark.employee_size
@pytest.mark.parametrize("test_id, description, input_data, expected", [
    ("TC_12.1_08", "Validate SMB classification consistency with employee size", "50-200 + Category=SMB", "✅ Accepted. Range aligns with SMB classification. Passes regex ^(\\d+|\\d+-\\d+)$ and logical consistency."),
    ("TC_12.1_09", "Detect mismatch: Large employee size but classified as Startup", "1000 + Category=Startup", "❌ Rejected. Violates business inference rule (Startup typically small scale)."),
])
def test_employee_size_consistency(test_id, description, input_data, expected):
    """
    Validates consistency between employee size and company category.
    """
    print(f"\nRunning {test_id}: {description}")
    ClassificationValidator.validate(input_data, expected)
