import uuid
import json
import re
from datetime import date, datetime, timezone
from webargs import ValidationError

from src.exceptions import ObjectNotFound, ParamInvalid


def log_extra(individual_id, unique_id):
    return {"unique_id": unique_id, "individual_id": individual_id}


def uuid_4(is_hex=False):
    if is_hex:
        return uuid.uuid4().hex
    return str(uuid.uuid4())


def date_utc_now():
    return datetime.now(timezone.utc)


def format_date():
    return "%Y-%m-%d"


def format_datetime():
    return "%Y-%m-%d %H:%M:%S"


def format_to_alphanumeric(value):
    return re.sub('[^0-9a-zA-Z]+', '_', value)


def validate_param(field, value, type_=None):
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


def validate_date(value):
    try:
        datetime.strptime(value, format_date())
    except Exception:
        raise ParamInvalid("Date with value '{}' is invalid!".format(value))


def validate_datetime(value):
    try:
        datetime.strptime(value, format_datetime())
    except Exception:
        raise ParamInvalid("Datetime with value '{}' is invalid!".format(value))


def validate_field_null(value):
    if not value:
        raise ValidationError("Param Invalid")


def validate_boolean(value):
    if not isinstance(value, bool):
        raise ParamInvalid(f'Boolean invalid: {value}')


def validate_non_negative_integer(value):
    if not isinstance(value, int) or value < 0:
        raise ParamInvalid(f'Number invalid: {value}')


def validate_uuid(value):
    try:
        uuid.UUID(value)
    except Exception:
        raise ParamInvalid("ID with value '{}' is invalid!".format(value))


def validate_item_dict(item, dict_search):
    if (not item) or (not dict_search) or (item not in dict_search):
        raise ParamInvalid(
            "Param {param} invalid for searched".format(param=item)
        )


def transform_datetime_to_isoformat(value):
    if isinstance(value, (date, datetime)):
        return value.isoformat()


def result_json(result):
    return json.loads(json.dumps(result, default=transform_datetime_to_isoformat))


def validate_object(p_id, p_object):
    if not p_object:
        raise ObjectNotFound("Object Not found for id {}".format(p_id))
