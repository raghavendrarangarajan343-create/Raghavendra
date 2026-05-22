import csv
import io

data = """column_name	Test ID	Test Case Description	Input Data	Expected Result
Category	TC_12.1_01	Validate correct classification for Startup-stage company	Startup	✅ Accepted. Matches regex ^(Startup|MSME|SMB|Enterprise|Investor|VC|Conglomerate)$ and aligns with business rule (taxonomy mapping).
Category	TC_12.1_02	Validate classification for MSME based on small-scale company	MSME	✅ Accepted. Valid enum and passes "Value In List check" (Automated validation).
Category	TC_12.1_03	Validate classification for SMB (mid-sized company)	SMB	✅ Accepted. Matches allowed enum list and satisfies classification taxonomy rule.
Category	TC_12.1_04	Validate classification for Venture Capital firm	VC	✅ Accepted. Correct classification for investor-type entity per business rules.
Category	TC_12.1_05	Validate classification for Investor entity	Investor	✅ Accepted. Matches enum and aligns with business taxonomy.
Category	TC_12.1_06	Reject invalid classification outside enum	SmallBiz	❌ Rejected. Fails regex and "Value In List check".
Category	TC_12.1_07	Reject incorrect casing if strict enum enforcement applied	startup	❌ Rejected if case-sensitive. Should normalize or enforce exact enum match.
Employee Size	TC_12.1_08	Validate SMB classification consistency with employee size	50-200 + Category=SMB	✅ Accepted. Range aligns with SMB classification. Passes regex ^(\\d+|\\d+-\\d+)$ and logical consistency.
Employee Size	TC_12.1_09	Detect mismatch: Large employee size but classified as Startup	1000 + Category=Startup	❌ Rejected. Violates business inference rule (Startup typically small scale).
Nature of Company	TC_12.1_10	Validate VC classification aligns with company nature	Private + Category=VC	⚠️ Conditional: Accepted if entity is a VC firm structured as private. Requires cross-field validation.
Nature of Company	TC_12.1_11	Detect mismatch: Non-Profit classified as VC	Non-Profit + Category=VC	❌ Rejected. Violates logical classification consistency.
Category	TC_12.1_12	Validate Enterprise classification	Enterprise	✅ Accepted. Matches enum and taxonomy rule-12.1 test case
column_name	Test ID	Test Case Description	Input Data	Expected Result
ALL_FIELDS	TC_14.4_001	Validate that inappropriate default values are NOT assigned to critical or measurable fields (e.g., financials, metrics, counts)	{ "Annual Revenues": "$0", "Employee Size": "0", "Website Traffic Rank": "0" }	❌ Fail – As per business_rules, measurable fields must not default to misleading values like 0 unless explicitly valid. Validation should flag incorrect defaults.
ALL_FIELDS	TC_14.4_002	Validate that nullable descriptive or categorical fields can use safe defaults like "Unknown" where allowed	{ "Remote Work Policy": "Unknown", "Vision": null }	✅ Pass – Nullable fields with no strict business_rules can default to "Unknown" or remain null per nullability rules.
ALL_FIELDS	TC_14.4_003	Validate that NOT NULL fields never receive default placeholders like "N/A", "Unknown", or empty strings	{ "Company Name": "Unknown", "Category": "N/A" }	❌ Fail – Violates Not Null + business_rules requiring valid, real values (e.g., official registry match, enum constraint).
ALL_FIELDS	TC_14.4_004	Validate that default values do not violate format_constraints or regex patterns	{ "Website URL": "Unknown", "CEO LinkedIn URL": "N/A" }	❌ Fail – Invalid format; does not match required regex (HTTPS URL patterns).
ALL_FIELDS	TC_14.4_005	Validate context-aware defaulting: derived or calculated fields must NOT be defaulted arbitrarily	{ "CAC:LTV Ratio": "0", "Runway": "0" }	❌ Fail – Derived metrics must be computed or null; defaulting to 0 violates data_rules and business logic.
ALL_FIELDS	TC_14.4_006	Validate that optional list/text fields can remain null instead of forced defaults	{ "Awards & Recognitions": "N/A", "Case Studies": "None" }	❌ Fail – Should be null instead of forced placeholders per nullability rules.
ALL_FIELDS	TC_14.4_007	Validate that enum-based fields do not accept invalid default placeholders	{ "Nature of Company": "Unknown", "Profitability Status": "N/A" }	❌ Fail – Must match strict enum values defined in regex_pattern.
ALL_FIELDS	TC_14.4_008	Validate that numeric fields respect domain constraints even when defaulted	{ "Employee Turnover": "150%", "Market Share (%)": "-10%" }	❌ Fail – Violates range constraints (0–100%) defined in business_rules.
ALL_FIELDS	TC_14.4_009	Validate that valid contextual defaults are applied only where business-safe	{ "Decision Maker Accessibility": "Low - Not publicly reachable" }	✅ Pass – Matches allowed enum prefix + descriptive extension per regex and business_rules.
ALL_FIELDS	TC_14.4_010	Validate that system avoids over-defaulting and preserves data integrity by leaving unknowns null	{ "Glassdoor Rating": null, "Indeed Rating": null }	✅ Pass – Nullable fields should remain null instead of forced defaults, preserving data accuracy---12.2 test case
column_name	Test ID	Test Case Description	Input Data	Expected Result
Nature of Company	TC-12.3-01	Valid Classification: Verify Private companies are correctly identified.	SpaceX → Private	Pass: Matches enum `(Private
Nature of Company	TC-12.3-02	Valid Classification: Verify Public companies are correctly identified.	Apple → Public	Pass: Valid classification; aligns with legal filings.
Nature of Company	TC-12.3-03	Valid Classification: Verify Subsidiary companies are correctly identified.	WhatsApp → Subsidiary	Pass: Correct parent-child ownership classification.
Nature of Company	TC-12.3-04	Invalid Classification: Reject values outside predefined enums.	Startup	Fail: Not in allowed enum list.
Nature of Company	TC-12.3-05	Case Sensitivity Check: Ensure standardized enum format is enforced.	private	Fail: Should match exact enum (or normalized).
Nature of Company	TC-12.3-06	Null Handling: Ensure field does not accept null values.	NULL	Fail: Field is Not Null (business rule violation).
Nature of Company	TC-12.3-07	Special Character Validation: Reject invalid characters in classification.	Private@123	Fail: Violates regex constraint.
Nature of Company	TC-12.3-08	Multi-value Rejection: Ensure only single classification is allowed.	Private/Public	Fail: Violates granularity (One per Entity).
Nature of Company	TC-12.3-09	Whitespace Handling: Ensure trimming of leading/trailing spaces.	" Public "	Pass: Trimmed → "Public"; matches enum.
Nature of Company	TC-12.3-10	Boundary Enum Validation: Validate acceptance of all allowed enum values.	Govt	Pass: Valid enum value accepted.
Category	TC-12.3-11	Cross-field Consistency: Ensure Category aligns with Nature of Company.	Category=Startup, Nature=Public	Fail: Logical inconsistency (Startup typically Private).
Category	TC-12.3-12	Cross-field Validation: Accept valid Category & Nature combinations.	Category=Enterprise, Nature=Public	Pass: Valid mapping.
GLOBAL RECORD	TC-12.3-13	Entity Validation: Ensure classification aligns with external trusted data sources.	Tesla → Public	Pass: Matches SEC/registry data.
GLOBAL RECORD	TC-12.3-14	Classification Completeness: Ensure every entity has a valid Nature of Company.	Missing field	Fail: Mandatory field missing---12.3 test case
column_name	Test ID	Test Case Description	Input Data	Expected Result
Brand Sentiment Score	TC-12.4-01	Valid Sentiment Classification: Accept standard sentiment categories.	Positive	Pass: Matches allowed values `(Positive
Brand Sentiment Score	TC-12.4-02	Valid Numeric Sentiment Score: Accept numeric sentiment index.	85	Pass: Valid numeric score (0–100 scale)
Brand Sentiment Score	TC-12.4-03	Invalid Sentiment Value: Reject unsupported labels.	Very Good	Fail: Not in allowed enum or numeric format
Brand Sentiment Score	TC-12.4-04	Null Handling: Ensure optional field allows null.	NULL	Pass: Field is Nullable
Glassdoor Rating	TC-12.4-05	Positive Sentiment Mapping: High rating should map to Positive sentiment.	4.5	Pass: Interpreted as Positive (range 4.0–5.0)
Glassdoor Rating	TC-12.4-06	Neutral Sentiment Mapping: Mid rating classification.	3	Pass: Interpreted as Neutral
Glassdoor Rating	TC-12.4-07	Negative Sentiment Mapping: Low rating classification.	1.8	Pass: Interpreted as Negative
Glassdoor Rating	TC-12.4-08	Range Validation: Reject out-of-bound rating.	5.5	Fail: Must be between 1.0 and 5.0
Indeed Rating	TC-12.4-09	Cross-platform Consistency: Validate rating follows same sentiment logic.	4.2	Pass: Interpreted as Positive
Google Reviews Rating	TC-12.4-10	Customer Sentiment Classification via rating.	2.5	Pass: Interpreted as Negative/Neutral boundary
Net Promoter Score (NPS)	TC-12.4-11	Positive Sentiment Mapping using NPS.	70	Pass: Promoter-heavy → Positive sentiment
Net Promoter Score (NPS)	TC-12.4-12	Neutral Sentiment Mapping using NPS.	10	Pass: Neutral sentiment
Net Promoter Score (NPS)	TC-12.4-13	Negative Sentiment Mapping using NPS.	-40	Pass: Detractor-heavy → Negative sentiment
Net Promoter Score (NPS)	TC-12.4-14	Range Validation for NPS.	150	Fail: Must be between -100 and 100
Work culture	TC-12.4-15	Text Sentiment Extraction: Detect sentiment from descriptive text.	"Collaborative and supportive environment"	Pass: Classified as Positive sentiment
Manager quality	TC-12.4-16	Negative Sentiment Detection from text.	"Micromanagement and high pressure"	Pass: Classified as Negative sentiment
Psychological safety	TC-12.4-17	Enum-based Sentiment Classification.	High	Pass: Interpreted as Positive
Psychological safety	TC-12.4-18	Invalid Enum Value Handling.	Very High	Fail: Not in allowed enum `(Low
GLOBAL RECORD	TC-12.4-19	Cross-field Sentiment Consistency: Ensure ratings and sentiment do not contradict.	Glassdoor=4.5, Brand Sentiment=Negative	Fail: Logical inconsistency
GLOBAL RECORD	TC-12.4-20	Aggregated Sentiment Validation: Ensure overall sentiment aligns with underlying metrics.	Ratings high, NPS high, Sentiment=Positive	Pass: Consistent sentiment classification"""

def clean_value(val):
    return val.strip().replace('\n', ' ')

output_rows = []
lines = data.split('\n')
for line in lines:
    if not line.strip(): continue
    if line.startswith('column_name'): continue
    
    parts = line.split('\t')
    if len(parts) < 5: 
        # Handle cases where tabs might be missing or different
        parts = [p.strip() for p in line.split('  ') if p.strip()]
        if len(parts) < 5: continue
        
    category = clean_value(parts[0])
    test_id = clean_value(parts[1])
    description = clean_value(parts[2])
    input_data = clean_value(parts[3])
    expected = clean_value(parts[4])
    
    # Normalize category for marker/filename safety
    norm_category = category.lower().replace(' ', '_').replace(':', '').replace('(', '').replace(')', '')
    
    output_rows.append({
        'Test ID': test_id,
        'Description': description,
        'Input Data': input_data,
        'Expected Result': expected,
        'Category': norm_category
    })

with open('data/test_cases.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['Test ID', 'Description', 'Input Data', 'Expected Result', 'Category'])
    writer.writeheader()
    writer.writerows(output_rows)

print(f"Saved {len(output_rows)} test cases to data/test_cases.csv")
