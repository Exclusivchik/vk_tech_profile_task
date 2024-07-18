import click

from generators.controller_generator import generate_rest_controllers
from generators.pydantic_generator import generate_pydantic_model
from utils.schema_validator import validate_json_schema


@click.group()
def cli():
    pass


@click.command()
@click.option(
    '--json-schema',
    type=click.Path(exists=True),
    required=True,
    help='Path to the JSON schema file.'
)
def validate_schema(json_schema):
    """Validate the JSON schema."""
    validate_json_schema(json_schema)


@click.command()
@click.option(
    '--json-schema',
    type=click.Path(exists=True),
    required=True,
    help='Path to the JSON schema file.'
)
@click.option(
    '--out-dir',
    type=click.Path(),
    required=True,
    help='Output directory for the generated models.'
)
def gen_pydantic(json_schema, out_dir):
    """Generate schemas model from JSON schema."""
    generate_pydantic_model(json_schema, out_dir)


@click.command()
@click.option(
    '--models-dir',
    type=click.Path(exists=True),
    required=True,
    help='Directory with schemas models.'
)
@click.option(
    '--out-dir',
    type=click.Path(),
    required=True,
    help='Output directory for the generated REST controllers.'
)
def gen_rest(models_dir, out_dir):
    """Generate REST controllers from schemas models."""
    generate_rest_controllers(models_dir, out_dir)


@click.command()
def valid_structure():
    """Structure of valid JSON Schema"""
    print("""
        • kind - String <= 32 characters. Identifies the json schema of this document.
        • name - String <= 128 characters. The name of the document.
        • description - String <= 4096 characters. An arbitrary description.
        • configuration.
        • specification - Dictionary. The structure is set by the user.
        • settings - Dictionary. The structure is set by the user.
        The structure of the following dictionaries is selected by the user:
        • configuration.specification
        • configuration.settings""")


cli.add_command(validate_schema)
cli.add_command(gen_pydantic)
cli.add_command(gen_rest)
cli.add_command(valid_structure)

if __name__ == '__main__':
    cli()
