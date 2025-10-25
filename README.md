# jsonschemaextractor

An extension to JSON schema allowing extracting values from objects declaratively by specifying them in the schema.

## Installation

```shell
pip install jsonvalidatingschemaextractor
```

## Usage

To extract a value from a JSON object into a field, specify an `extract_to` property in the JSON schema which contains the name
with which the value should be extracted into the resulting dictionary.

In the example below, we extract the `name` field in the JSON to a `username` field in the dictionary.

```python
from jsonschema.validators import Draft7Validator
from jsonvalidatingschemaextractor import Extractor

schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "extract_to": "username"
        }
    }
}

validator = Draft7Validator(schema=schema)
extractor = Extractor(validator=validator)  # noqa
result = extractor.validate_and_extract({"name": "John Doe"})

assert result.extracted_values == {"username": "John Doe"}
```

# Why  

The intended use-case for the library is to help extract values from deeply-nested JSON into a flat dictionary. For example, you may be parsing a JSONL file and writing them to a relational table. 

Consider the following JSON.

```python
instance = {
  "user": {
    "first_name": "John",
    "last_name": "Doe",
    "address": {
      "line1": "2950 Southern Street",
      "line2": "Mineola, New York",
      "zipcode": "11501"
    }
  }
}
```  

The schema for this, with extraction, is as follows.  

```python
schema = {
    "type": "object",
    "properties": {
        "user": {
            "type": "object",
            "properties": {
                "first_name": {
                    "type": "string", 
                    "extract_to": "user_first_name"
                },
                "last_name": {
                    "type": "string", 
                    "extract_to": "user_last_name"
                },
                "address": {
                    "type": "object",
                    "properties": {
                        "line1": {
                            "type": "string",
                            "extract_to": "address_line_1"
                        },
                        "line2": {
                            "type": "string",
                            "extract_to": "address_line_2"
                        },
                        "zipcode": {
                            "type": "string",
                            "extract_to": "zipcode"
                        }
                    }
                }
            }
        }
    }
}
```

Finally, we can extract these values into a dictionary.

```python
import json
from jsonschema.validators import Draft7Validator
from jsonvalidatingschemaextractor import Extractor

schema = ...
instance = ...

validator = Draft7Validator(schema=schema)
extractor = Extractor(validator=validator)  # noqa

result = extractor.validate_and_extract(instance)

print(json.dumps(result.extracted_values, indent=4))
```

This gives us the following.

```json
{
    "user_first_name": "John",
    "user_last_name": "Doe",
    "address_line_1": "2950 Southern Street",
    "address_line_2": "Mineola, New York",
    "zipcode": "11501"
}
```  

These dictionaries can then be used to create Pandas or Dask dataframes and written to permanent storage for easier querying.  

Additionally, any validation error that arises can be spotted to ensure data quality.