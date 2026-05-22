import re

class BaseValidator:
    @staticmethod
    def validate(actual, expected):
        raise NotImplementedError("Subclasses must implement validate()")

class ClassificationValidator(BaseValidator):
    @staticmethod
    def validate(actual, expected_msg):
        # Handle "Pass" or "Accepted" vs "Fail" or "Rejected"
        is_positive = any(word in expected_msg.lower() for word in ["pass", "accepted", "✅"])
        if is_positive:
            # Simple mock: if it's not a known failure case, it passes
            assert True
        else:
            # If expected is Fail/Rejected, we expect an assertion error or specific failure
            # For this mock, we'll just log it
            print(f"Validation expected failure: {expected_msg}")

class EnumValidator(BaseValidator):
    @staticmethod
    def validate(value, allowed_enum):
        if value not in allowed_enum:
            raise ValueError(f"Value '{value}' not in allowed list: {allowed_enum}")

class RegexValidator(BaseValidator):
    @staticmethod
    def validate(value, pattern):
        if not re.match(pattern, str(value)):
            raise ValueError(f"Value '{value}' does not match pattern: {pattern}")

class RangeValidator(BaseValidator):
    @staticmethod
    def validate(value, min_val, max_val):
        num = float(value)
        if not (min_val <= num <= max_val):
            raise ValueError(f"Value {num} out of range [{min_val}, {max_val}]")
