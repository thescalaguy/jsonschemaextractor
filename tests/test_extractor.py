from jsonschema.validators import Draft7Validator

from jsonschemaextractor import Extractor


def test_valid_json_object(schema):
    instance = {"user": {"first_name": "John", "last_name": "Doe"}}

    validator = Draft7Validator(schema=schema)
    extractor = Extractor(validator=validator)  # noqa
    result = extractor.validate_and_extract(instance)

    assert not result.errors
    assert result.extracted_values["user_first_name"] == "John"
    assert result.extracted_values["user_last_name"] == "Doe"


def test_invalid_json_object(schema):
    instance = {"user": {"first_name": 0, "last_name": 0}}

    validator = Draft7Validator(schema=schema)
    extractor = Extractor(validator=validator)  # noqa
    result = extractor.validate_and_extract(instance)

    assert result.errors
    assert result.extracted_values["user_first_name"] == 0
    assert result.extracted_values["user_last_name"] == 0
