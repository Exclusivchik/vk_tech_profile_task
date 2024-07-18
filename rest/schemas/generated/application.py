from pydantic import BaseModel, Field, ConfigDict


class ApplicationConfigurationSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")
    a: str
    b: str
    c: str


class ApplicationConfigurationSpecification(BaseModel):
    model_config = ConfigDict(extra="forbid")
    a: str
    b: str
    c: str


class ApplicationConfiguration(BaseModel):
    model_config = ConfigDict(extra="forbid")
    specification: ApplicationConfigurationSpecification
    settings: ApplicationConfigurationSettings


class Application(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: str = Field(max_length=32, pattern="^application$")
    name: str = Field(max_length=128)
    description: str = Field(max_length=4096)
    version: str = Field(pattern=r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$")
    configuration: ApplicationConfiguration

