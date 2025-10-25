import pytest


@pytest.fixture(scope="session")
def schema():
    return {
        "type": "object",
        "properties": {
            "user": {
                "type": "object",
                "properties": {
                    "first_name": {"type": "string", "extract_to": "user_first_name"},
                    "last_name": {"type": "string", "extract_to": "user_last_name"},
                },
            }
        },
    }
