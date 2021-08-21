import json
import pytest
from pydantic import ValidationError

from nrtest.config import AppConfig, TestConfig, Version


app_args = {
    "name": "app_name",
    "exe": "app_exe",
    "version": "1.2.3",
}

test_args = {
    "name": "test_name",
    "args": ["arg1", "arg2"],
}


def test_create_app_config():
    c = AppConfig(**app_args)
    assert c.name == app_args["name"]
    assert c.exe == app_args["exe"]
    assert c.version == Version(app_args["version"])


def test_validate_app_config():
    with pytest.raises(ValidationError, match="field required"):
        AppConfig()
    with pytest.raises(ValidationError):
        AppConfig(**app_args, unknown="unknown")
    with pytest.raises(TypeError, match="multiple values"):
        AppConfig(**app_args, name="duplicate")
    with pytest.raises(ValidationError, match="string required"):
        AppConfig(**dict(app_args, version=1.2))
    with pytest.raises(ValidationError, match="Invalid version"):
        AppConfig(**dict(app_args, version="invalid"))
    with pytest.raises(ValidationError, match="not a valid path"):
        AppConfig(**app_args, setup_script=123)
    with pytest.raises(ValidationError, match="not a valid float"):
        AppConfig(**app_args, timeout="string")
    with pytest.raises(ValidationError, match="ensure this value is greater than 0"):
        AppConfig(**app_args, timeout=-5)


def test_create_test_config():
    c = TestConfig(**test_args)
    assert c.name == test_args["name"]
    assert c.args == test_args["args"]


def test_validate_test_config():
    with pytest.raises(ValidationError, match="field required"):
        TestConfig()
    with pytest.raises(ValidationError):
        TestConfig(**test_args, unknown="unknown")
    with pytest.raises(TypeError, match="multiple values"):
        TestConfig(**test_args, name="duplicate")
    with pytest.raises(ValidationError, match="not a valid list"):
        TestConfig(**dict(app_args, args="arg1"))
    with pytest.raises(ValidationError, match="string required"):
        TestConfig(**test_args, version=1.2)
    with pytest.raises(ValidationError, match="Invalid version"):
        TestConfig(**test_args, version="invalid")
    with pytest.raises(ValidationError, match="Invalid version"):
        TestConfig(**test_args, minimum_app_version="invalid")
    with pytest.raises(ValidationError, match="not a valid list"):
        TestConfig(**test_args, input_files="invalid")
    with pytest.raises(ValidationError, match="not a valid list"):
        TestConfig(**test_args, fail_strings="invalid")


def test_version_serialization():
    ser = json.loads(AppConfig(**app_args).json())
    assert ser["version"] == app_args["version"]
