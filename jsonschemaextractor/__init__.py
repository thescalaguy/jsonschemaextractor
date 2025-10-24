import dataclasses
from typing import Any

from jsonschema.exceptions import ValidationError
from jsonschema.protocols import Validator

EXTRACT_TO = "extract_to"


class Extractor:
    """Extract values from JSON objects into a dictionary while performing schema validation

    >>> from jsonschema.validators import Draft7Validator
    >>> schema = {
    ...     "type": "object",
    ...     "properties": {
    ...         "name": {"type": "string", "extract_to": "name"}
    ...     }
    ... }
    >>> validator = Draft7Validator(schema=schema)
    >>> extractor = Extractor(validator=validator)  # noqa
    >>> result = extractor.validate({"name": "John Doe"})
    >>> assert result.extracted_values == {"name": "John Doe"}
    """

    def __init__(self, validator: Validator):
        self.validator = validator

    def validate(self, instance):
        extracted_values = {}

        self.validator.VALIDATORS.update(
            {
                EXTRACT_TO: lambda validator,
                value,
                instance,
                schema: extracted_values.update({value: instance})
            }
        )

        errors = list(self.validator.iter_errors(instance))

        return ValidationResult(
            extracted_values=extracted_values,
            errors=errors,
        )


@dataclasses.dataclass(frozen=True)
class ValidationResult:
    extracted_values: dict[str, Any]
    errors: list[ValidationError]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
