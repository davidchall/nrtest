import pytest
from pydantic import ValidationError

from nrtest.config import AppConfig


valid_args = {
    "name": "app_name",
    "exe": "app_exe",
    "version": "1.2.3",
}


def test_create_app_config():
    with pytest.raises(ValidationError):
        AppConfig()


def test_unknown_fields():
    with pytest.raises(ValidationError):
        AppConfig(**valid_args, unknown="unknown")
