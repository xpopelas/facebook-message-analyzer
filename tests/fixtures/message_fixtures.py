import json
from pathlib import Path

import pytest


@pytest.fixture
def simple_message_dict() -> dict:
    path = Path("tests") / Path("samples") / Path("simple_message.json")
    with open(path, "r", encoding="UTF-8") as fh:
        return json.load(fh)


@pytest.fixture
def fake_fbdata_path() -> Path:
    return Path("tests") / Path("samples") / Path("fake_fbdata")
