from jsonschema import validate, ValidationError


def validate_config_schema(data, schema):
    try:
        validate(instance=data, schema=schema)
        return {"valid": True}
    except ValidationError as e:
        return {"valid": False, "error": str(e)}
