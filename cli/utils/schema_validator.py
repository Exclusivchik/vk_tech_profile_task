import json

from jsonschema.exceptions import ValidationError


def validate_json_schema(schema_path):
    try:
        with open(schema_path, 'r') as file:
            schema = json.load(file)

        props = schema["properties"]

        # kind
        if props["kind"]["type"] != "string" or props["kind"]["maxLength"] > 32 or "const" not in props["kind"]:
            raise ValidationError(f"kind mismatch")
        # name
        if props["name"]["type"] != "string" or props["name"]["maxLength"] > 128:
            raise ValidationError(f"name mismatch")
        # description
        if props["description"]["type"] != "string" or props["description"]["maxLength"] > 4096:
            raise ValidationError(f"description mismatch")
        # version
        if props["version"]["type"] != "string" or props["version"]["pattern"] != "^\\d+\\.\\d+\\.\\d+$":
            raise ValidationError(f"version mismatch")
        # config
        if props["configuration"]["type"] != "object" or props["configuration"]["additionalProperties"]:
            raise ValidationError(f"config mismatch")
        config_props = props["configuration"]["properties"]
        if config_props["specification"]["type"] != "object" or config_props["settings"]["type"] != "object":
            raise ValidationError(f"config mismatch")

        if schema["required"] != ["kind", "name", "description", "configuration"] or schema["additionalProperties"]:
            raise ValidationError(f"schema mismatch")

        print("JSON Schema is valid")
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e.msg}")
    except KeyError as e:
        print(f"Invalid schema: {e} is not exist")
