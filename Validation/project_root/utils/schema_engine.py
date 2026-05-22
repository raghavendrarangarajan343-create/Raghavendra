import json
import os

class SchemaEngine:
    def __init__(self, schema_path=None):
        if schema_path is None:
            schema_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'metadata_schema.json')
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            self.schema = json.load(f)
            
    def get_all_fields(self):
        return [field['column_name'] for field in self.schema]
        
    def get_fields_by_nullability(self, nullability="Not Null"):
        """Returns fields that match the specific nullability requirement."""
        return [
            field['column_name'] for field in self.schema 
            if field.get('nullability') == nullability
        ]
        
    def get_fields_by_type(self, data_type_prefix):
        """Returns fields whose data type starts with the prefix (e.g., VARCHAR, DECIMAL)."""
        return [
            field['column_name'] for field in self.schema 
            if field.get('data_type', '').startswith(data_type_prefix)
        ]
        
    def get_field_metadata(self, column_name):
        """Returns the full metadata dictionary for a specific column."""
        for field in self.schema:
            if field['column_name'] == column_name:
                return field
        return None
