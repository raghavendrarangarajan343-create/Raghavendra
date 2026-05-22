import pytest
from validators.base_validators import ClassificationValidator

@pytest.mark.global_record
@pytest.mark.parametrize("test_id, description, input_data, expected", [
    ("TC-13.2-01", "Response Time Measurement: Measure total generation time for a Fortune 500 company with full metadata", "Complete dataset (e.g., Apple-like entity with 150+ fields populated)", "Pass: Response time ≤ defined SLA (e.g., ≤ 2 sec). System handles large, complex records efficiently."),
    ("TC-13.2-02", "Response Time Measurement: Measure generation time for a startup entity with minimal data.", "Partial dataset (10–20 fields populated)", "Pass: Faster response than enterprise case; ≤ 1 sec expected."),
    ("TC-13.2-03", "Comparative Performance: Compare response time between Public vs Private companies.", "Public: Full dataset; Private: Medium dataset", "Pass: Public company processing time ≥ Private; difference within acceptable threshold (<30%)."),
    ("TC-13.2-04", "Scalability Test: Measure response time as number of fields increases.", "Dataset sizes: 20 fields → 80 fields → 150+ fields", "Pass: Response time increases linearly; no exponential degradation."),
    ("TC-13.2-05", "High Load Scenario: Measure response time under concurrent requests.", "50 parallel company records (mixed types)", "Pass: Avg response time within SLA; no timeout or crash."),
    ("TC-13.2-06", "Data Complexity Impact: Evaluate response time for high-text vs numeric-heavy datasets.", "Text-heavy (Narratives, Risks) vs Numeric-heavy (Financials)", "Pass: Text processing slightly slower but within SLA limits."),
    ("TC-13.2-07", "Edge Case Performance: Measure response time for maximum allowed input size.", "Max length fields (e.g., 5000-char descriptions across multiple fields)", "Pass: System processes without latency spike or memory failure."),
    ("TC-13.2-08", "Timeout Handling: Ensure system fails gracefully if response exceeds limit.", "Artificial delay > SLA threshold", "Fail/Pass: System returns timeout error or fallback response."),
    ("TC-13.2-09", "Caching Efficiency: Measure repeated query response time.", "Same company queried multiple times", "Pass: Subsequent responses faster due to caching."),
    ("TC-13.2-10", "End-to-End Pipeline Time: Validate total processing time (ingestion → validation → output).", "Full pipeline execution", "Pass: Total time within SLA; no stage bottlenecks."),
])
def test_performance_and_scalability(test_id, description, input_data, expected):
    print(f"\nRunning {test_id}: {description}")
    ClassificationValidator.validate(input_data, expected)

@pytest.mark.token_limit_handling
@pytest.mark.parametrize("test_id, description, input_data, expected", [
    ("TC-13.3-01", "Token Limit Handling: Validate that long company descriptions are not truncated mid-sentence", "Overview of the Company = 5000-character narrative text", "Pass: No mid-sentence cutoff; content ends with complete sentence; complies with max length constraint (≤5000)"),
    ("TC-13.3-02", "Token Limit Handling: Validate handling of records with multiple long text fields simultaneously", "Overview, Services / Offerings / Products, Recent News all near max length", "Pass: All fields fully preserved; no truncation or data loss across fields"),
    ("TC-13.3-03", "Token Limit Handling: Validate large list fields are not partially truncated", "Office Locations = 100+ entries (comma-separated or structured text)", "Pass: All entries retained; no broken or incomplete location values"),
    ("TC-13.3-04", "Token Limit Handling: Ensure no mid-word truncation occurs at token boundary", "Long narrative text near token limit", "Pass: Output ends at full word boundary; no partial words present"),
    ("TC-13.3-05", "Token Limit Handling: Validate structured data integrity under high token load", "Key Business Leaders = large JSON array with multiple entries", "Pass: JSON remains valid; no missing brackets or structural corruption"),
    ("TC-13.3-06", "Token Limit Handling: Validate system behavior with maximum allowed cumulative payload size", "Full dataset (150+ fields populated; multiple max-length TEXT fields)", "Pass: Entire record processed without truncation; respects individual field constraints and validation_mode"),
    ("TC-13.3-07", "Token Limit Handling: Validate that smaller fields are not dropped when one field is very large", "Overview = max length; other fields = normal size", "Pass: All fields populated; no starvation or omission of smaller fields"),
    ("TC-13.3-08", "Token Limit Handling: Validate encoding preservation in long text fields", "Long text with UTF-8 characters (é, ü, ñ)", "Pass: Characters preserved; no encoding corruption; complies with regex where applicable"),
    ("TC-13.3-09", "Token Limit Handling: Validate behavior when input slightly exceeds allowed limits", "Overview = 6000 characters", "Pass: Data truncated gracefully to 5000 OR rejected per validation rules; no system crash"),
    ("TC-13.3-10", "Token Limit Handling: Validate end-to-end pipeline does not truncate data across stages", "Full pipeline: ingestion → validation → output with large record", "Pass: No truncation across pipeline; output matches input within defined constraints"),
])
def test_token_limit_and_truncation(test_id, description, input_data, expected):
    print(f"\nRunning {test_id}: {description}")
    ClassificationValidator.validate(input_data, expected)

@pytest.mark.memory_independence
@pytest.mark.parametrize("test_id, description, input_data, expected", [
    ("TC-13.4-01", "Memory Independence: Validate no data leakage between sequential requests", "Request 1: Company A (e.g., fintech dataset)Request 2: Company B (e.g., healthcare dataset)", "Pass: Response for Company B contains only B’s data; no fields, values, or context from Company A present"),
    ("TC-13.4-02", "Memory Independence: Validate isolation when similar companies are processed sequentially", "Request 1: Company A (SaaS CRM)Request 2: Company B (SaaS CRM competitor)", "Pass: No attribute/value mixing (e.g., customers, products, metrics) between A and B"),
    ("TC-13.4-03", "Memory Independence: Validate no cross-contamination in batch processing", "Batch input: 10 companies with similar structure", "Pass: Each output record strictly maps to its input; no shared or duplicated data across records"),
    ("TC-13.4-04", "Memory Independence: Validate field-level isolation across requests", "Company A has CEO Name = John DoeCompany B has CEO Name = Alice Smith", "Pass: Company B output must not contain \"John Doe\"; strict field-level correctness maintained"),
    ("TC-13.4-05", "Memory Independence: Validate isolation under high load (parallel processing)", "20 parallel requests with different company datasets", "Pass: No cross-request contamination; all outputs correctly mapped to respective inputs"),
    ("TC-13.4-06", "Memory Independence: Validate no residual memory from previous failed request", "Request 1: Invalid/partial datasetRequest 2: Valid dataset", "Pass: Request 2 output unaffected by Request 1 failure; no residual artifacts"),
    ("TC-13.4-07", "Memory Independence: Validate no contamination across different data types", "Company A: text-heavy datasetCompany B: numeric-heavy dataset", "Pass: No mixing of textual/numeric values across records"),
    ("TC-13.4-08", "Memory Independence: Validate repeated requests do not accumulate stale data", "Same Company B requested multiple times with slight variations", "Pass: Each response reflects only current input; no accumulation of prior values"),
    ("TC-13.4-09", "Memory Independence: Validate isolation across derived and dependent fields", "Company A and B with different Annual Revenues, Profitability Status", "Pass: Derived/logically linked fields remain correct per entity; no cross-entity influence"),
    ("TC-13.4-10", "Memory Independence: End-to-end validation across pipeline stages", "Sequential pipeline execution for multiple companies", "Pass: No contamination across ingestion, validation, and output stages"),
])
def test_memory_isolation(test_id, description, input_data, expected):
    print(f"\nRunning {test_id}: {description}")
    ClassificationValidator.validate(input_data, expected)
