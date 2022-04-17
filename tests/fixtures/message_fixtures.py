import json

import pytest


@pytest.fixture
def simple_message_content() -> str:
    path = "tests/samples/simple_message.json"
    with open(path, "r", encoding="UTF-8") as fh:
        file_content = "".join(fh.readlines())
    return file_content


@pytest.fixture
def simple_message_dict(simple_message_content) -> dict:
    return json.loads(simple_message_content)
