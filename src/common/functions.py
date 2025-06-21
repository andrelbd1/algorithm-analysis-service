import json
import re
import uuid
from datetime import date, datetime, timezone
from typing import Any
from webargs import ValidationError

from src.exceptions import ObjectNotFound, ParamInvalid


def date_utc_now() -> datetime:
    """
    Get the current date and time in UTC.

    Returns:
        datetime: The current date and time with UTC timezone.
    """
    return datetime.now(tz=timezone.utc)


def format_date() -> str:
    return "%Y-%m-%d"


def format_datetime() -> str:
    return "%Y-%m-%d %H:%M:%S"


def format_to_alphanumeric(value: str, replace: str = '_') -> str:
    """
    Formats a given string to contain only alphanumeric characters.

    Any character that is not a digit or a letter will be replaced with the specified replacement string.

    Args:
        value (str): The input string to be formatted.
        replace (str, optional): The string to replace non-alphanumeric characters with. Defaults to '_'.

    Returns:
        str: The formatted string containing only alphanumeric characters and the specified replacements.
    """
    return re.sub('[^0-9a-zA-Z]+', replace, value)


def log_extra(individual_id: str, unique_id: str) -> dict:
    return {"unique_id": unique_id, "individual_id": individual_id}


def result_json(result: Any) -> dict:
    """
    Converts a given result to a JSON-compatible dictionary, ensuring that any datetime objects
    are transformed to ISO 8601 format.

    Args:
        result (Any): The result to be converted to JSON format. This can be any data type that is
                      serializable by the `json` module.

    Returns:
        dict: A dictionary representation of the result, with datetime objects converted to ISO 8601 format.
    """
    return json.loads(json.dumps(result, default=transform_datetime_to_isoformat))


def transform_datetime_to_isoformat(value: date | datetime) -> date | datetime:
    """
    Convert a date or datetime object to its ISO 8601 string representation.

    Args:
        value (date or datetime): The date or datetime object to be converted.

    Returns:
        str: The ISO 8601 string representation of the input date or datetime object.
    """
    if isinstance(value, (date, datetime)):
        return value.isoformat()


def uuid_4(is_hex: bool = False) -> str:
    """
    Generate a UUID version 4.

    Args:
        is_hex (bool): If True, return the UUID as a hexadecimal string.
                       If False, return the UUID as a standard string.

    Returns:
        str: The generated UUID, either as a hexadecimal string or a standard string.
    """
    if is_hex:
        return uuid.uuid4().hex
    return str(uuid.uuid4())


def validate_date(value: str):
    """
    Validates if the given date string matches the expected date format.

    Args:
        value (str): The date string to be validated.

    Raises:
        ParamInvalid: If the date string does not match the expected format.

    """
    try:
        datetime.strptime(value, format_date())
    except Exception:
        raise ParamInvalid("Date with value '{}' is invalid!".format(value))


def validate_datetime(value: str):
    """
    Validates if the given string value is a valid datetime.

    Args:
        value (str): The datetime string to be validated.

    Raises:
        ParamInvalid: If the datetime string is invalid.
    """
    try:
        datetime.strptime(value, format_datetime())
    except Exception:
        raise ParamInvalid("Datetime with value '{}' is invalid!".format(value))


def validate_field_null(value: Any):
    """
    Validates if the given value is null or empty.

    Args:
        value (Any): The value to be validated.

    Raises:
        ValidationError: If the value is null or empty.
    """
    if not value:
        raise ValidationError("Param Invalid")


def validate_non_negative_integer(value: int):
    """
    Validates that the given value is a non-negative integer.

    Args:
        value (int): The value to be validated.

    Raises:
        ParamInvalid: If the value is not an integer or if it is a negative integer.
    """
    if not isinstance(value, int) or value < 0:
        raise ParamInvalid(f'Number invalid: {value}')


def validate_object(p_id: Any, p_object: Any):
    """
    Validates if the given object exists.

    Args:
        p_id (Any): The identifier of the object.
        p_object (Any): The object to validate.

    Raises:
        ObjectNotFound: If the object is not found.
    """
    if not p_object:
        raise ObjectNotFound("Object Not found for id {}".format(p_id))


def validate_param(field: str, value: Any, type_: str = None):
    """
    Validates the type of a given parameter.

    Args:
        field (str): The name of the parameter.
        value (Any): The value of the parameter to be validated.
        type_ (str, optional): The expected type of the parameter.
            Can be one of "bool", "int", "float", "str", "list", "dict", "tuple".
            If None, the value is checked for being None.

    Raises:
        ParamInvalid: If the value does not match the expected type.
    """
    match type_:
        case "bool":
            res = not isinstance(value, bool)
        case "int":
            res = not isinstance(value, int)
        case "float":
            res = not isinstance(value, float)
        case "str":
            res = not isinstance(value, str)
        case "list":
            res = not isinstance(value, list)
        case "dict":
            res = not isinstance(value, dict)
        case "tuple":
            res = not isinstance(value, tuple)
        case _:
            res = value is None
    if res:
        raise ParamInvalid("Param {} {} is invalid!".format(field, value))


def validate_uuid(value: str):
    """
    Validates whether the given value is a valid UUID.

    Args:
        value (str): The value to be validated as a UUID.

    Raises:
        ParamInvalid: If the value is not a valid UUID.

    """
    try:
        uuid.UUID(value)
    except Exception:
        raise ParamInvalid("ID with value '{}' is invalid!".format(value))


def validate_item_dict(item: str, dict_search: dict):
    """
    Validates if the given item exists in the provided dictionary.

    Args:
        item (str): The item to be validated.
        dict_search (dict): The dictionary in which to search for the item.

    Raises:
        ParamInvalid: If the item is None, the dictionary is None, or the item is not found in the dictionary.
    """
    if (not item) or (not dict_search) or (item not in dict_search):
        raise ParamInvalid("Param '{}' invalid for searched".format(item))
