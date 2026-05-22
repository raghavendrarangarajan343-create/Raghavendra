import csv
import io
import os

new_data = """column_name	Test ID	Test Case Description	Input Data	Expected Result
Customer Concentration Risk	TC-12.5-01	Valid Risk Classification: Detect high customer dependency risk.	Yes – Top client contributes 35% revenue	Pass: Classified as High Risk (business rule: >20% concentration)
Customer Concentration Risk	TC-12.5-02	Valid Risk Classification: Low concentration risk.	No – Top client contributes 10%	Pass: Classified as Low Risk
Customer Concentration Risk	TC-12.5-03	Invalid Input Handling: Reject unsupported values.	Maybe	Fail: Must match `(Yes
Geopolitical Risks	TC-12.5-04	High Risk Detection: Identify geopolitical threats.	"Operations impacted by trade sanctions in China"	Pass: Classified as High Risk (keyword: sanctions)
Geopolitical Risks	TC-12.5-05	Medium Risk Detection: Moderate exposure scenario.	"Dependent on imports from multiple regions"	Pass: Classified as Medium Risk
Geopolitical Risks	TC-12.5-06	Low Risk Detection: Minimal geopolitical exposure.	"Domestic-only operations"	Pass: Classified as Low Risk
Geopolitical Risks	TC-12.5-07	Null Handling: Allow empty if no known risks.	NULL	Pass: Field is Nullable
Burn Rate	TC-12.5-08	High Risk Assessment: Excessive burn rate detection.	$5M/month with low revenue	Pass: Classified as High Risk
Burn Rate	TC-12.5-10	Invalid Value Handling: Reject negative burn.	-$500K	Fail: Burn rate must be > 0
Runway	TC-12.5-11	Critical Risk Detection: Low runway threshold.	4 months	Pass: Classified as High Risk (rule: <6 months critical)
Runway	TC-12.5-12	Safe Range Validation: Adequate runway.	18 months	Pass: Classified as Low Risk
Runway	TC-12.5-13	Invalid Input Handling: Reject negative runway.	-3 months	Fail: Must be positive numeric
Macro Risks	TC-12.5-14	Risk Identification: Detect macroeconomic risks.	"High inflation and rising interest rates"	Pass: Classified as High Risk
Macro Risks	TC-12.5-15	Neutral Risk Scenario.	"Stable economic conditions"	Pass: Classified as Low/Medium Risk
Cybersecurity Posture	TC-12.5-16	High Risk Detection: Missing certifications or breach history.	"No SOC2; recent data breach"	Pass: Classified as High Risk
Cybersecurity Posture	TC-12.5-17	Low Risk Detection: Strong security posture.	"SOC2, ISO27001 certified"	Pass: Classified as Low Risk
Cybersecurity Posture	TC-12.5-18	Text Validation: Detect risk keywords.	"Minor vulnerabilities identified"	Pass: Classified as Medium Risk
GLOBAL RECORD	TC-12.5-19	Cross-field Risk Consistency: Ensure burn + runway alignment.	Burn=$5M/month, Runway=3 months	Pass: Overall classified as High Risk
GLOBAL RECORD	TC-12.5-20	Contradiction Detection: Prevent inconsistent risk signals.	Burn=$5M, Runway=24 months, Risk=Low	Fail: Inconsistent risk classification
GLOBAL RECORD	TC-12.5-21	Aggregated Risk Validation: Ensure overall risk reflects multiple factors.	High burn, low runway, high geo risk	Pass: Final classification = High Risk
GLOBAL RECORD	TC-13.2-01	Response Time Measurement: Measure total generation time for a Fortune 500 company with full metadata (all fields populated).	Complete dataset (e.g., Apple-like entity with 150+ fields populated)	Pass: Response time ≤ defined SLA (e.g., ≤ 2 sec). System handles large, complex records efficiently.
GLOBAL RECORD	TC-13.2-02	Response Time Measurement: Measure generation time for a startup entity with minimal data.	Partial dataset (10–20 fields populated)	Pass: Faster response than enterprise case; ≤ 1 sec expected.
GLOBAL RECORD	TC-13.2-03	Comparative Performance: Compare response time between Public vs Private companies.	Public: Full dataset; Private: Medium dataset	Pass: Public company processing time ≥ Private; difference within acceptable threshold (<30%).
GLOBAL RECORD	TC-13.2-04	Scalability Test: Measure response time as number of fields increases.	Dataset sizes: 20 fields → 80 fields → 150+ fields	Pass: Response time increases linearly; no exponential degradation.
GLOBAL RECORD	TC-13.2-05	High Load Scenario: Measure response time under concurrent requests.	50 parallel company records (mixed types)	Pass: Avg response time within SLA; no timeout or crash.
GLOBAL RECORD	TC-13.2-06	Data Complexity Impact: Evaluate response time for high-text vs numeric-heavy datasets.	Text-heavy (Narratives, Risks) vs Numeric-heavy (Financials)	Pass: Text processing slightly slower but within SLA limits.
GLOBAL RECORD	TC-13.2-07	Edge Case Performance: Measure response time for maximum allowed input size.	Max length fields (e.g., 5000-char descriptions across multiple fields)	Pass: System processes without latency spike or memory failure.
GLOBAL RECORD	TC-13.2-08	Timeout Handling: Ensure system fails gracefully if response exceeds limit.	Artificial delay > SLA threshold	Fail/Pass: System returns timeout error or fallback response.
GLOBAL RECORD	TC-13.2-09	Caching Efficiency: Measure repeated query response time.	Same company queried multiple times	Pass: Subsequent responses faster due to caching.
GLOBAL RECORD	TC-13.2-10	End-to-End Pipeline Time: Validate total processing time (ingestion → validation → output).	Full pipeline execution	Pass: Total time within SLA; no stage bottlenecks.
GLOBAL RECORD	TC-13.3-01	Token Limit Handling: Validate that long company descriptions are not truncated mid-sentence	Overview of the Company = 5000-character narrative text	Pass: No mid-sentence cutoff; content ends with complete sentence; complies with max length constraint (≤5000)
GLOBAL RECORD	TC-13.3-02	Token Limit Handling: Validate handling of records with multiple long text fields simultaneously	Overview, Services / Offerings / Products, Recent News all near max length	Pass: All fields fully preserved; no truncation or data loss across fields
GLOBAL RECORD	TC-13.3-03	Token Limit Handling: Validate large list fields are not partially truncated	Office Locations = 100+ entries (comma-separated or structured text)	Pass: All entries retained; no broken or incomplete location values
GLOBAL RECORD	TC-13.3-04	Token Limit Handling: Ensure no mid-word truncation occurs at token boundary	Long narrative text near token limit	Pass: Output ends at full word boundary; no partial words present
GLOBAL RECORD	TC-13.3-05	Token Limit Handling: Validate structured data integrity under high token load	Key Business Leaders = large JSON array with multiple entries	Pass: JSON remains valid; no missing brackets or structural corruption
GLOBAL RECORD	TC-13.3-06	Token Limit Handling: Validate system behavior with maximum allowed cumulative payload size	Full dataset (150+ fields populated; multiple max-length TEXT fields)	Pass: Entire record processed without truncation; respects individual field constraints and validation_mode
GLOBAL RECORD	TC-13.3-07	Token Limit Handling: Validate that smaller fields are not dropped when one field is very large	Overview = max length; other fields = normal size	Pass: All fields populated; no starvation or omission of smaller fields
GLOBAL RECORD	TC-13.3-08	Token Limit Handling: Validate encoding preservation in long text fields	Long text with UTF-8 characters (é, ü, ñ)	Pass: Characters preserved; no encoding corruption; complies with regex where applicable
GLOBAL RECORD	TC-13.3-09	Token Limit Handling: Validate behavior when input slightly exceeds allowed limits	Overview = 6000 characters	Pass: Data truncated gracefully to 5000 OR rejected per validation rules; no system crash
GLOBAL RECORD	TC-13.3-10	Token Limit Handling: Validate end-to-end pipeline does not truncate data across stages	Full pipeline: ingestion → validation → output with large record	Pass: No truncation across pipeline; output matches input within defined constraints
GLOBAL RECORD	TC-14.4-11	Mixed Data Type Load: Validate token handling across text, numeric, and URL fields	Large text + multiple URLs + numeric metrics	Pass: No truncation across any data type; all formats preserved
GLOBAL RECORD	TC-14.4-12	Pipeline Integrity: Validate full record survives ingestion → validation → output without truncation	Full dataset (150+ fields populated)	Pass: No data loss across pipeline stages; aligns with validation_mode (Automated/Manual)
GLOBAL RECORD	TC-13.4-01	Memory Independence: Validate no data leakage between sequential requests	Request 1: Company A (e.g., fintech dataset)Request 2: Company B (e.g., healthcare dataset)	Pass: Response for Company B contains only B’s data; no fields, values, or context from Company A present
GLOBAL RECORD	TC-13.4-02	Memory Independence: Validate isolation when similar companies are processed sequentially	Request 1: Company A (SaaS CRM)Request 2: Company B (SaaS CRM competitor)	Pass: No attribute/value mixing (e.g., customers, products, metrics) between A and B
GLOBAL RECORD	TC-13.4-03	Memory Independence: Validate no cross-contamination in batch processing	Batch input: 10 companies with similar structure	Pass: Each output record strictly maps to its input; no shared or duplicated data across records
GLOBAL RECORD	TC-13.4-04	Memory Independence: Validate field-level isolation across requests	Company A has CEO Name = John DoeCompany B has CEO Name = Alice Smith	Pass: Company B output must not contain "John Doe"; strict field-level correctness maintained
GLOBAL RECORD	TC-13.4-05	Memory Independence: Validate isolation under high load (parallel processing)	20 parallel requests with different company datasets	Pass: No cross-request contamination; all outputs correctly mapped to respective inputs
GLOBAL RECORD	TC-13.4-06	Memory Independence: Validate no residual memory from previous failed request	Request 1: Invalid/partial datasetRequest 2: Valid dataset	Pass: Request 2 output unaffected by Request 1 failure; no residual artifacts
GLOBAL RECORD	TC-13.4-07	Memory Independence: Validate no contamination across different data types	Company A: text-heavy datasetCompany B: numeric-heavy dataset	Pass: No mixing of textual/numeric values across records
GLOBAL RECORD	TC-13.4-08	Memory Independence: Validate repeated requests do not accumulate stale data	Same Company B requested multiple times with slight variations	Pass: Each response reflects only current input; no accumulation of prior values
GLOBAL RECORD	TC-13.4-09	Memory Independence: Validate isolation across derived and dependent fields	Company A and B with different Annual Revenues, Profitability Status	Pass: Derived/logically linked fields remain correct per entity; no cross-entity influence
GLOBAL RECORD	TC-13.4-10	Memory Independence: End-to-end validation across pipeline stages	Sequential pipeline execution for multiple companies	Pass: No contamination across ingestion, validation, and output stages"""

def clean_value(val):
    return val.strip().replace('\n', ' ')

output_rows = []
lines = new_data.split('\n')
for line in lines:
    if not line.strip(): continue
    if line.startswith('column_name'): continue
    
    parts = line.split('\t')
    if len(parts) < 5: continue
        
    category = clean_value(parts[0])
    test_id = clean_value(parts[1])
    description = clean_value(parts[2])
    input_data = clean_value(parts[3])
    expected = clean_value(parts[4])
    
    norm_category = category.lower().replace(' ', '_').replace(':', '').replace('(', '').replace(')', '')
    
    output_rows.append({
        'Test ID': test_id,
        'Description': description,
        'Input Data': input_data,
        'Expected Result': expected,
        'Category': norm_category
    })

# Append to existing CSV
file_exists = os.path.isfile('data/test_cases.csv')
with open('data/test_cases.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['Test ID', 'Description', 'Input Data', 'Expected Result', 'Category'])
    if not file_exists:
        writer.writeheader()
    writer.writerows(output_rows)

print(f"Appended {len(output_rows)} test cases to data/test_cases.csv")
