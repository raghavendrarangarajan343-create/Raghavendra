import pytest
from validators.base_validators import ClassificationValidator

@pytest.mark.customer_concentration_risk
@pytest.mark.parametrize("test_id, description, input_data, expected", [
    ("TC-12.5-01", "Valid Risk Classification: Detect high customer dependency risk.", "Yes – Top client contributes 35% revenue", "Pass: Classified as High Risk (business rule: >20% concentration)"),
    ("TC-12.5-02", "Valid Risk Classification: Low concentration risk.", "No – Top client contributes 10%", "Pass: Classified as Low Risk"),
    ("TC-12.5-03", "Invalid Input Handling: Reject unsupported values.", "Maybe", "Fail: Must match `(Yes, No)`"),
])
def test_customer_concentration_risk(test_id, description, input_data, expected):
    print(f"\nRunning {test_id}: {description}")
    ClassificationValidator.validate(input_data, expected)

@pytest.mark.geopolitical_risks
@pytest.mark.parametrize("test_id, description, input_data, expected", [
    ("TC-12.5-04", "High Risk Detection: Identify geopolitical threats.", "\"Operations impacted by trade sanctions in China\"", "Pass: Classified as High Risk (keyword: sanctions)"),
    ("TC-12.5-05", "Medium Risk Detection: Moderate exposure scenario.", "\"Dependent on imports from multiple regions\"", "Pass: Classified as Medium Risk"),
    ("TC-12.5-06", "Low Risk Detection: Minimal geopolitical exposure.", "\"Domestic-only operations\"", "Pass: Classified as Low Risk"),
    ("TC-12.5-07", "Null Handling: Allow empty if no known risks.", "NULL", "Pass: Field is Nullable"),
])
def test_geopolitical_risk(test_id, description, input_data, expected):
    print(f"\nRunning {test_id}: {description}")
    ClassificationValidator.validate(input_data, expected)

@pytest.mark.burn_rate
@pytest.mark.parametrize("test_id, description, input_data, expected", [
    ("TC-12.5-08", "High Risk Assessment: Excessive burn rate detection.", "$5M/month with low revenue", "Pass: Classified as High Risk"),
    ("TC-12.5-10", "Invalid Value Handling: Reject negative burn.", "-$500K", "Fail: Burn rate must be > 0"),
])
def test_burn_rate_risk(test_id, description, input_data, expected):
    print(f"\nRunning {test_id}: {description}")
    ClassificationValidator.validate(input_data, expected)

@pytest.mark.runway
@pytest.mark.parametrize("test_id, description, input_data, expected", [
    ("TC-12.5-11", "Critical Risk Detection: Low runway threshold.", "4 months", "Pass: Classified as High Risk (rule: <6 months critical)"),
    ("TC-12.5-12", "Safe Range Validation: Adequate runway.", "18 months", "Pass: Classified as Low Risk"),
    ("TC-12.5-13", "Invalid Input Handling: Reject negative runway.", "-3 months", "Fail: Must be positive numeric"),
])
def test_runway_risk(test_id, description, input_data, expected):
    print(f"\nRunning {test_id}: {description}")
    ClassificationValidator.validate(input_data, expected)

@pytest.mark.macro_risks
@pytest.mark.parametrize("test_id, description, input_data, expected", [
    ("TC-12.5-14", "Risk Identification: Detect macroeconomic risks.", "\"High inflation and rising interest rates\"", "Pass: Classified as High Risk"),
    ("TC-12.5-15", "Neutral Risk Scenario.", "\"Stable economic conditions\"", "Pass: Classified as Low/Medium Risk"),
])
def test_macro_risk(test_id, description, input_data, expected):
    print(f"\nRunning {test_id}: {description}")
    ClassificationValidator.validate(input_data, expected)

@pytest.mark.cybersecurity_posture
@pytest.mark.parametrize("test_id, description, input_data, expected", [
    ("TC-12.5-16", "High Risk Detection: Missing certifications or breach history.", "\"No SOC2; recent data breach\"", "Pass: Classified as High Risk"),
    ("TC-12.5-17", "Low Risk Detection: Strong security posture.", "\"SOC2, ISO27001 certified\"", "Pass: Classified as Low Risk"),
    ("TC-12.5-18", "Text Validation: Detect risk keywords.", "\"Minor vulnerabilities identified\"", "Pass: Classified as Medium Risk"),
])
def test_cybersecurity_risk(test_id, description, input_data, expected):
    print(f"\nRunning {test_id}: {description}")
    ClassificationValidator.validate(input_data, expected)

@pytest.mark.global_record
@pytest.mark.parametrize("test_id, description, input_data, expected", [
    ("TC-12.5-19", "Cross-field Risk Consistency: Ensure burn + runway alignment.", "Burn=$5M/month, Runway=3 months", "Pass: Overall classified as High Risk"),
    ("TC-12.5-20", "Contradiction Detection: Prevent inconsistent risk signals.", "Burn=$5M, Runway=24 months, Risk=Low", "Fail: Inconsistent risk classification"),
    ("TC-12.5-21", "Aggregated Risk Validation: Ensure overall risk reflects multiple factors.", "High burn, low runway, high geo risk", "Pass: Final classification = High Risk"),
])
def test_aggregated_risk(test_id, description, input_data, expected):
    print(f"\nRunning {test_id}: {description}")
    ClassificationValidator.validate(input_data, expected)
