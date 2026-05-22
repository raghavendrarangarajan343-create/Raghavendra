import csv
import ast
import os

def load_test_cases(file_path):
    """
    Loads test cases from a CSV file.
    Returns a list of dictionaries.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Test case file not found: {file_path}")

    test_cases = []
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Clean up column names (strip whitespace)
            clean_row = {k.strip(): v.strip() for k, v in row.items()}
            
            # Safely evaluate Input Data if it looks like a dict/list
            try:
                if clean_row['Input Data'].startswith('{') or clean_row['Input Data'].startswith('['):
                    clean_row['Input Data'] = ast.literal_eval(clean_row['Input Data'])
            except (ValueError, SyntaxError):
                pass
            
            test_cases.append(clean_row)
    
    return test_cases
