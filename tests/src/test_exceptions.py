from src.exceptions import (AppError, BadRequest, NotFound,
                            ErrorPartnerGreaterEqual500, 
                            ErrorPartnerGreaterEqual400,
                            ErrorRequests, ParamInvalid, ObjectNotFound)
from tests import BaseTestClass


class TestException(BaseTestClass):

    def test_bad_request_is_app_error(self):
        try:
            raise BadRequest("message")
        except AppError as error:
            assert error.status == 400

    def test_not_found_is_app_error(self):
        try:
            raise NotFound("message")
        except AppError as error:
            assert error.status == 404

    def test_error_partner_greater_equal_500_is_app_error(self):
        try:
            raise ErrorPartnerGreaterEqual500("message")
        except AppError as error:
            assert error.status == 500

    def test_error_partner_greater_equal_400_is_app_error(self):
        try:
            raise ErrorPartnerGreaterEqual400("message")
        except AppError as error:
            assert error.status == 400

    def test_error_requests_is_app_error(self):
        try:
            raise ErrorRequests("message")
        except AppError as error:
            assert error.status == 500

    def test_param_invalid_is_app_error(self):
        try:
            raise ParamInvalid("message")
        except AppError as error:
            assert error.status == 400

    def test_object_not_found_is_app_error(self):
        try:
            raise ObjectNotFound("message")
        except AppError as error:
            assert error.status == 404