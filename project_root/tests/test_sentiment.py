import pytest
from validators.base_validators import ClassificationValidator

@pytest.mark.brand_sentiment_score
@pytest.mark.parametrize("test_id, description, input_data, expected", [
    ("TC-12.4-01", "Valid Sentiment Classification: Accept standard sentiment categories.", "Positive", "Pass: Matches allowed values `(Positive, Neutral, Negative)`."),
    ("TC-12.4-02", "Valid Numeric Sentiment Score: Accept numeric sentiment index.", "85", "Pass: Valid numeric score (0–100 scale)"),
    ("TC-12.4-03", "Invalid Sentiment Value: Reject unsupported labels.", "Very Good", "Fail: Not in allowed enum or numeric format"),
    ("TC-12.4-04", "Null Handling: Ensure optional field allows null.", "NULL", "Pass: Field is Nullable"),
])
def test_brand_sentiment(test_id, description, input_data, expected):
    print(f"\nRunning {test_id}: {description}")
    ClassificationValidator.validate(input_data, expected)

@pytest.mark.glassdoor_rating
@pytest.mark.parametrize("test_id, description, input_data, expected", [
    ("TC-12.4-05", "Positive Sentiment Mapping: High rating should map to Positive sentiment.", "4.5", "Pass: Interpreted as Positive (range 4.0–5.0)"),
    ("TC-12.4-06", "Neutral Sentiment Mapping: Mid rating classification.", "3", "Pass: Interpreted as Neutral"),
    ("TC-12.4-07", "Negative Sentiment Mapping: Low rating classification.", "1.8", "Pass: Interpreted as Negative"),
    ("TC-12.4-08", "Range Validation: Reject out-of-bound rating.", "5.5", "Fail: Must be between 1.0 and 5.0"),
])
def test_glassdoor_rating(test_id, description, input_data, expected):
    print(f"\nRunning {test_id}: {description}")
    ClassificationValidator.validate(input_data, expected)

@pytest.mark.indeed_rating
@pytest.mark.parametrize("test_id, description, input_data, expected", [
    ("TC-12.4-09", "Cross-platform Consistency: Validate rating follows same sentiment logic.", "4.2", "Pass: Interpreted as Positive"),
])
def test_indeed_rating(test_id, description, input_data, expected):
    print(f"\nRunning {test_id}: {description}")
    ClassificationValidator.validate(input_data, expected)

@pytest.mark.google_reviews_rating
@pytest.mark.parametrize("test_id, description, input_data, expected", [
    ("TC-12.4-10", "Customer Sentiment Classification via rating.", "2.5", "Pass: Interpreted as Negative/Neutral boundary"),
])
def test_google_reviews_rating(test_id, description, input_data, expected):
    print(f"\nRunning {test_id}: {description}")
    ClassificationValidator.validate(input_data, expected)

@pytest.mark.net_promoter_score_nps
@pytest.mark.parametrize("test_id, description, input_data, expected", [
    ("TC-12.4-11", "Positive Sentiment Mapping using NPS.", "70", "Pass: Promoter-heavy → Positive sentiment"),
    ("TC-12.4-12", "Neutral Sentiment Mapping using NPS.", "10", "Pass: Neutral sentiment"),
    ("TC-12.4-13", "Negative Sentiment Mapping using NPS.", "-40", "Pass: Detractor-heavy → Negative sentiment"),
    ("TC-12.4-14", "Range Validation for NPS.", "150", "Fail: Must be between -100 and 100"),
])
def test_nps_mapping(test_id, description, input_data, expected):
    print(f"\nRunning {test_id}: {description}")
    ClassificationValidator.validate(input_data, expected)

@pytest.mark.work_culture
@pytest.mark.parametrize("test_id, description, input_data, expected", [
    ("TC-12.4-15", "Text Sentiment Extraction: Detect sentiment from descriptive text.", "\"Collaborative and supportive environment\"", "Pass: Classified as Positive sentiment"),
])
def test_work_culture_sentiment(test_id, description, input_data, expected):
    print(f"\nRunning {test_id}: {description}")
    ClassificationValidator.validate(input_data, expected)

@pytest.mark.manager_quality
@pytest.mark.parametrize("test_id, description, input_data, expected", [
    ("TC-12.4-16", "Negative Sentiment Detection from text.", "\"Micromanagement and high pressure\"", "Pass: Classified as Negative sentiment"),
])
def test_manager_quality_sentiment(test_id, description, input_data, expected):
    print(f"\nRunning {test_id}: {description}")
    ClassificationValidator.validate(input_data, expected)

@pytest.mark.psychological_safety
@pytest.mark.parametrize("test_id, description, input_data, expected", [
    ("TC-12.4-17", "Enum-based Sentiment Classification.", "High", "Pass: Interpreted as Positive"),
    ("TC-12.4-18", "Invalid Enum Value Handling.", "Very High", "Fail: Not in allowed enum `(Low, Medium, High)`"),
])
def test_psychological_safety_enum(test_id, description, input_data, expected):
    print(f"\nRunning {test_id}: {description}")
    ClassificationValidator.validate(input_data, expected)

@pytest.mark.global_record
@pytest.mark.parametrize("test_id, description, input_data, expected", [
    ("TC-12.4-19", "Cross-field Sentiment Consistency: Ensure ratings and sentiment do not contradict.", "Glassdoor=4.5, Brand Sentiment=Negative", "Fail: Logical inconsistency"),
    ("TC-12.4-20", "Aggregated Sentiment Validation: Ensure overall sentiment aligns with underlying metrics.", "Ratings high, NPS high, Sentiment=Positive", "Pass: Consistent sentiment classification"),
])
def test_aggregated_sentiment(test_id, description, input_data, expected):
    print(f"\nRunning {test_id}: {description}")
    ClassificationValidator.validate(input_data, expected)
