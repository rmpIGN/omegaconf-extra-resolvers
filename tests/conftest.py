"""Shared fixtures loading real OmegaConf config files."""

from pathlib import Path

import pytest
from omegaconf import OmegaConf

_CONFIGS_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def list_cfg():
    return OmegaConf.load(_CONFIGS_DIR / "list.yaml")


@pytest.fixture
def os_cfg():
    return OmegaConf.load(_CONFIGS_DIR / "os.yaml")


@pytest.fixture
def string_cfg():
    return OmegaConf.load(_CONFIGS_DIR / "string.yaml")
