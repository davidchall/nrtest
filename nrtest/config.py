from pathlib import Path
from typing import List, Optional

import pkg_resources.extern.packaging.version as version
import pydantic
from pydantic import Field


class Version(version.Version):
    """Version with pydantic validation of PEP 440 strings."""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            examples=["0.4.2", "1.2.3"],
            type="string",
            format="version",
        )

    @classmethod
    def validate(cls, v: str):
        if not isinstance(v, str):
            raise TypeError('string required')
        return cls(v)


class BaseModel(pydantic.BaseModel):
    """BaseModel class underlying Config classes."""
    class Config:
        extra = "forbid"
        json_encoders = {
            Version: lambda x: str(x),
        }


class AppConfig(BaseModel):
    """Software under test."""
    name: str = Field(
        ...,
        description="Name of the software.",
    )
    exe: str = Field(
        ...,
        description="The executable name.",
    )
    version: Version = Field(
        ...,
        description="Version of the software.",
    )
    description: Optional[str] = Field(
        None,
        description="A short description to help identification of this version.",
    )
    setup_script: Optional[Path] = Field(
        None,
        description="Path to a bash script that shall be sourced in order to create the environment needed to run the software.",
    )
    timeout: Optional[float] = Field(
        None,
        description="The period in time [seconds] after which a test will be terminated and considered failed.",
        gt=0,
    )


class TestConfig(BaseModel):
    """A single test."""
    name: str = Field(
        ...,
        description="Name of the test.",
    )
    args: List[str] = Field(
        ...,
        description="A list of command-line arguments that will be passed to the software under test.",
    )
    description: Optional[str] = Field(
        None,
        description="A short description to help identification of this version.",
    )
    version: Optional[Version] = Field(
        None,
        description="Version of the test.",
    )
    minimum_app_version: Optional[Version] = Field(
        None,
        description="The minimum software version required for the test to be executed. If the software under test does not satisfy this requirement, then the test is removed from the test suite before execution. This allows you to run the latest test suite on old software without test failures.",
    )
    input_files: List[Path] = Field(
        [],
        description="A list of required input files. Each path is specified relative to the location of the configuration file itself.",
    )
    output_files: List[Path] = Field(
        [],
    )
    fail_strings: List[str] = Field(
        [],
        description="If any of these strings are found in the stdout or stderr streams, the test is considered failed.",
    )
