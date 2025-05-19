
from datetime import date, datetime
from src.common.functions import *
from src.exceptions import ObjectNotFound, ParamInvalid
from tests import BaseTestClass
from webargs import ValidationError


class TestFunctions(BaseTestClass):

    def test_date_utc_now(self):
        date = date_utc_now()
        assert isinstance(date, datetime)

    def test_uuid_v4_just_ex(self):
        value = uuid_4(True)
        self.assertFalse('-' in value)

    def test_uuid_v4(self):
        value = uuid_4()
        self.assertTrue('-' in value)
    
    def test_validate_param_success(self):
        param = 'mock_param'
        result = validate_param('field', param)
        self.assertIsNone(result)

    def test_validate_param_none(self):
        param = None
        with self.assertRaises(ParamInvalid):
            validate_param('field', param)

    def test_validate_param_bool_success(self):
        param = False        
        result = validate_param('field', param, 'bool')
        self.assertIsNone(result)

    def test_validate_param_bool_fail(self):
        param = 'mock_param'
        with self.assertRaises(ParamInvalid):
            validate_param('field', param, 'bool')

    def test_validate_param_int_success(self):
        param = 1        
        result = validate_param('field', param, 'int')
        self.assertIsNone(result)

    def test_validate_param_int_fail(self):
        param = 'mock_param'
        with self.assertRaises(ParamInvalid):
            validate_param('field', param, 'int')

    def test_validate_param_float_success(self):
        param = 1.5
        result = validate_param('field', param, 'float')
        self.assertIsNone(result)

    def test_validate_param_float_fail(self):
        param = 'mock_param'
        with self.assertRaises(ParamInvalid):
            validate_param('field', param, 'float')

    def test_validate_param_str_success(self):
        param = 'mock_param'
        result = validate_param('field', param, 'str')
        self.assertIsNone(result)

    def test_validate_param_str_fail(self):
        param = True
        with self.assertRaises(ParamInvalid):
            validate_param('field', param, 'str')

    def test_validate_param_list_success(self):
        param = ['mock_param']
        result = validate_param('field', param, 'list')
        self.assertIsNone(result)

    def test_validate_param_list_fail(self):
        param = True
        with self.assertRaises(ParamInvalid):
            validate_param('field', param, 'list')

    def test_validate_param_dict_success(self):
        param = {'mock_param': 'mock_val'}
        result = validate_param('field', param, 'dict')
        self.assertIsNone(result)

    def test_validate_param_dict_fail(self):
        param = ['mock_param']
        with self.assertRaises(ParamInvalid):
            validate_param('field', param, 'dict')

    def test_validate_param_tuple_success(self):
        param = 1, 2
        result = validate_param('field', param, 'tuple')
        self.assertIsNone(result)

    def test_validate_param_tuple_fail(self):
        param = ['mock_param']
        with self.assertRaises(ParamInvalid):
            validate_param('field', param, 'tuple')

    def test_validate_date_success(self):
        date_string = "2024-06-01"
        result = validate_date(date_string)
        self.assertIsNone(result)
    
    def test_validate_date_fail(self):
        date_string = "2024-06-01 12:30:25"
        with self.assertRaises(ParamInvalid):
            validate_date(date_string)

    def test_format_to_alphanumeric(self):
        string = "abc  123 *&@#$!;/[]|<>-.,    xz"
        result = format_to_alphanumeric(string)
        self.assertEqual(result, "abc_123_xz")

    def test_validate_date_success(self):
        try:
            validate_date('2022-10-01')
        except Exception:
            self.fail("raised Exception unexpectedly")

    def test_validate_date_using_datetime_format_invalid(self):
        with self.assertRaises(ParamInvalid):
            validate_date('2022-10-01 10:10:10')

    def test_validate_date_using_day_invalid(self):
        with self.assertRaises(ParamInvalid):
            validate_date('2022-02-31')

    def test_validate_datetime_success(self):
        try:
            validate_datetime('2022-10-01 10:10:10')
        except Exception:
            self.fail("raised Exception unexpectedly")

    def test_validate_datetime_using_date_format_invalid(self):
        with self.assertRaises(ParamInvalid):
            validate_datetime('2022-10-01')

    def test_validate_datetime_using_day_invalid(self):
        with self.assertRaises(ParamInvalid):
            validate_datetime('2022-02-31 10:10:10')

    def test_validate_field_null_success(self):
        try:
            validate_field_null('2022-10-01')
        except Exception:
            self.fail("raised Exception unexpectedly")

    def test_validate_field_null_invalid(self):
        with self.assertRaises(ValidationError):
            validate_field_null(None)

    def test_validate_non_negative_integer_success(self):
        try:
            validate_non_negative_integer(2)
        except Exception:
            self.fail("raised Exception unexpectedly")

    def test_validate_non_negative_integer_negative_invalid(self):
        with self.assertRaises(ParamInvalid):
            validate_non_negative_integer(-1)

    def test_validate_non_negative_integer_null_invalid(self):
        with self.assertRaises(ParamInvalid):
            validate_non_negative_integer(None)

    def test_validate_non_negative_integer_string_invalid(self):
        with self.assertRaises(ParamInvalid):
            validate_non_negative_integer('1')

    def test_validate_uuid_success(self):
        try:
            validate_uuid('550e8400-e29b-41d4-a716-446655440000')
        except Exception:
            self.fail("raised Exception unexpectedly")

    def test_validate_uuid_invalid(self):
        with self.assertRaises(ParamInvalid):
            validate_uuid('550e8400-e29b-41d4-a716-46655440000')

    def test_validate_uuid_null_invalid(self):
        with self.assertRaises(ParamInvalid):
            validate_uuid(None)

    def test_validate_item_dict_success(self):
        try:
            validate_item_dict('a', {'a': 2, 'b': '3'})
        except Exception:
            self.fail("raised Exception unexpectedly")

    def test_validate_item_dict_invalid(self):
        with self.assertRaises(ParamInvalid):
            validate_item_dict('a', {'b': 'a'})

    def test_validate_item_null_item_invalid(self):
        with self.assertRaises(ParamInvalid):
            validate_item_dict(None, {'b': 'a'})

    def test_validate_item_null_dict_invalid(self):
        with self.assertRaises(ParamInvalid):
            validate_item_dict('a', None)

    def test_transform_datetime_to_isoformat_datetime_success(self):
        value = datetime.strptime("2024-10-11 12:34:56", "%Y-%m-%d %H:%M:%S")
        result = transform_datetime_to_isoformat(value)
        self.assertIsNotNone(result)
        self.assertEqual(result, '2024-10-11T12:34:56')

    def test_transform_datetime_to_isoformat_date_success(self):
        value = datetime.strptime("2024-10-11", "%Y-%m-%d")
        result = transform_datetime_to_isoformat(value)
        self.assertIsNotNone(result)
        self.assertEqual(result, '2024-10-11T00:00:00')

    def test_transform_datetime_to_isoformat_date2_success(self):
        value = date(2024, 10, 11)
        result = transform_datetime_to_isoformat(value)
        self.assertIsNotNone(result)
        self.assertEqual(result, '2024-10-11')

    def test_transform_datetime_to_isoformat_null(self):
        result = transform_datetime_to_isoformat(None)
        self.assertIsNone(result)

    def test_transform_datetime_to_isoformat_int(self):
        result = transform_datetime_to_isoformat(2)
        self.assertIsNone(result)

    def test_transform_datetime_to_isoformat_string(self):
        result = transform_datetime_to_isoformat('2')
        self.assertIsNone(result)

    def test_validate_object_success(self):
        try:
            validate_object('a', 'a')
        except Exception:
            self.fail("raised Exception unexpectedly")

    def test_validate_object_invalid(self):
        with self.assertRaises(ObjectNotFound):
            validate_object('a', None)