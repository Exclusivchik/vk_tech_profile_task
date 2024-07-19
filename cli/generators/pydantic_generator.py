import json
import os
from typing import Any, Dict, List


def parse_schema(schema: Dict[str, Any], class_name: str) -> List[str]:
    lines = []
    properties = schema["properties"]
    additional_properties = schema["additionalProperties"]

    lines.append(f"class {class_name}(BaseModel):")
    if not additional_properties:
        lines.append(f'    model_config = ConfigDict(extra="forbid")')
    for prop, details in properties.items():
        prop_type = details["type"]
        if prop_type == "string":
            constraints = []
            if "maxLength" in details:
                constraints.append(f"max_length={details['maxLength']}")
            if "const" in details:
                constraints.append(f'pattern="^{details['const']}$"')
            if "pattern" in details:
                constraints.append(f'pattern=r"{details['pattern']}"')
            field = f"str = Field({', '.join(constraints)})" if constraints else "str"
            lines.append(f"    {prop}: {field}")
        elif prop_type == "number":
            constraints = []
            if "minimum" in details:
                constraints.append(f'le={details['minimum']}')
            if "maximum" in details:
                constraints.append(f'ge={details['maximum']}')
            if "exclusiveMaximum" in details:
                constraints.append(f'gt={details['exclusiveMaximum']}')
            if "exclusiveMinimum" in details:
                constraints.append(f'lt={details['exclusiveMinimum']}')

            field = f"float = Field({', '.join(constraints)})" if constraints else "str"
            lines.append(f"    {prop}: {field}")
        elif prop_type == "object":
            if "properties" in details:
                nested_class_name = class_name + prop.capitalize()
                nested_lines = parse_schema(details, nested_class_name)
                lines = nested_lines + lines
                lines.append(f"    {prop}: {nested_class_name}")
            else:
                lines.append(f"    {prop}: Dict[str, Any]")
    lines.append("\n")
    return lines


def generate_pydantic_model(schema_path: str, out_dir: str) -> None:
    with open(schema_path, 'r') as file:
        schema = json.load(file)

    imports = ("from typing import " + ", ".join(["Dict", "Any"]) + '\n' +
               "from pydantic import " + ", ".join(["BaseModel", "Field", "ConfigDict"]) +
               '\n\n\n')

    model_name = schema["properties"]["kind"]["const"].capitalize()

    content = parse_schema(schema, model_name)
    path_to_model = os.path.join(out_dir, model_name.lower() + ".py")
    with open(path_to_model, 'w+') as pydantic_model_file:
        pydantic_model_file.write(imports)
        pydantic_model_file.write("\n".join(content))

    print(model_name, "model has been generated")
