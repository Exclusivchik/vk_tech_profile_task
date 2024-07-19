from pydantic import BaseModel, Field, ConfigDict


class CarConfigurationSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CarConfigurationSpecification(BaseModel):
    model_config = ConfigDict(extra="forbid")
    motor: str = Field(max_length=15)
    body: str = Field(max_length=10)


class CarConfiguration(BaseModel):
    model_config = ConfigDict(extra="forbid")
    specification: CarConfigurationSpecification
    settings: CarConfigurationSettings


class Car(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: str = Field(max_length=32, pattern="^car$")
    name: str = Field(max_length=128)
    description: str = Field(max_length=4096)
    version: str = Field(pattern=r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$")
    configuration: CarConfiguration

