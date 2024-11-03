from datetime import datetime, timezone
import uuid

from src.exceptions import ParamInvalid


def log_extra(individual_id, unique_id):
    return {"unique_id": unique_id, "individual_id": individual_id}


def uuid_4(is_hex=False):
    if is_hex:
        return uuid.uuid4().hex
    return str(uuid.uuid4())


def date_utc_now():
    return datetime.now(timezone.utc)


def date_app_now(value):
    return datetime.now(value)


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
        msg = "Param {} {} is invalid!".format(field, value)
        msg = msg if type_ is None else "{} It is not a {}.".format(msg, type_)
        raise ParamInvalid(msg)


def validate_date(date_string):
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
    except Exception:
        raise ParamInvalid("Param with value '{}' is invalid!".format(date_string))
