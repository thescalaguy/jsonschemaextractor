# jsonschemaextractor  

An extension to JSON schema allowing extracting values from objects declaratively by specifying them in the schema.  

By specifying an "extract_to" field in the schema, the value of that field will be saved into a dictionary with that name. See the usage example below.

## Installation

```shell
pip install jsonschemaextractor
```

## Usage

```python
from jsonschema.validators import Draft7Validator
from jsonschemaextractor import Extractor

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "extract_to": "name"}
    }
}

validator = Draft7Validator(schema=schema)
extractor = Extractor(validator=validator)  # noqa
result = extractor.validate({"name": "John Doe"})

assert result.extracted_values == {"name": "John Doe"}
```