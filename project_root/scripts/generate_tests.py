import os
import sys

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.csv_loader import load_test_cases

def generate_pytest_file(csv_path, output_path):
    test_cases = load_test_cases(csv_path)
    
    # Group test cases by category for parameterization
    grouped = {}
    for tc in test_cases:
        cat = tc['Category']
        if not cat: cat = "general"
        if cat not in grouped:
            grouped[cat] = []
        grouped[cat].append(tc)

    content = [
        "import pytest",
        "import sys",
        "import os",
        "sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))",
        "from validators.base_validators import ClassificationValidator",
        "",
        "# Auto-generated test suite from user-provided test cases",
        ""
    ]

    for category, cases in grouped.items():
        content.append(f"@pytest.mark.{category}")
        content.append(f"@pytest.mark.parametrize('test_id, description, input_data, expected', [")
        for tc in cases:
            input_repr = repr(tc['Input Data'])
            content.append(f"    ({repr(tc['Test ID'])}, {repr(tc['Description'])}, {input_repr}, {repr(tc['Expected Result'])}),")
        content.append("])")
        
        func_name = f"test_{category}"
        content.append(f"def {func_name}(test_id, description, input_data, expected):")
        content.append(f"    \"\"\"")
        content.append(f"    Auto-generated test for {category}")
        content.append(f"    \"\"\"")
        content.append(f"    print(f'\\nRunning {{test_id}}: {{description}}')")
        content.append(f"    print(f'Input: {{input_data}}')")
        content.append(f"    print(f'Expected: {{expected}}')")
        content.append(f"    ")
        content.append(f"    # Basic validation logic based on the 'Expected Result' string")
        content.append(f"    ClassificationValidator.validate(input_data, expected)")
        content.append("")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(content))
    
    print(f"Successfully generated {output_path}")

if __name__ == "__main__":
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    tests_dir = os.path.join(os.path.dirname(__file__), '..', 'tests')
    generate_pytest_file(os.path.join(data_dir, 'test_cases.csv'), os.path.join(tests_dir, 'test_generated.py'))
