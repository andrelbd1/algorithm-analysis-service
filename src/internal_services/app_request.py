import requests
from src.exceptions import (ErrorPartnerGreaterEqual400,
                            ErrorPartnerGreaterEqual500,
                            ErrorRequests)


class RequestsApp:

    ERRORS_REQUESTS = (requests.exceptions.HTTPError,
                       requests.exceptions.ConnectionError,
                       requests.exceptions.ProxyError,
                       requests.exceptions.SSLError,
                       requests.exceptions.Timeout,
                       requests.exceptions.ConnectTimeout,
                       requests.exceptions.ReadTimeout,
                       requests.exceptions.URLRequired,
                       requests.exceptions.TooManyRedirects,
                       requests.exceptions.MissingSchema,
                       requests.exceptions.InvalidSchema,
                       requests.exceptions.InvalidURL,
                       requests.exceptions.InvalidHeader,
                       requests.exceptions.ChunkedEncodingError,
                       requests.exceptions.ContentDecodingError,
                       requests.exceptions.StreamConsumedError,
                       requests.exceptions.RetryError,
                       requests.exceptions.UnrewindableBodyError,
                       )

    @staticmethod
    def __validate_return_response(response):
        """Validate return response."""
        error_msg = "Error calling url: {url}, status_code: {status}. content {content}"
        if response.status_code >= 500:
            error_msg = error_msg.format(url=response.url, status=str(response.status_code), content=response.content)
            error = ErrorPartnerGreaterEqual500(error_msg)
            error.status = response.status_code
            raise error

        if response.status_code >= 400 and response.status_code < 500:
            error_msg = error_msg.format(url=response.url, status=str(response.status_code), content=response.content)
            error = ErrorPartnerGreaterEqual400(error_msg)
            error.status = response.status_code
            raise error

    def __request(self, method, *args, **kwargs):
        """Method default."""
        try:
            method = getattr(requests, method)
            response = method(*args, **kwargs)
            self.__validate_return_response(response)
            return response
        except self.ERRORS_REQUESTS as error:
            raise ErrorRequests(str(error))

    def get(self, *args, **kwargs):
        return self.__request('get', *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.__request('post', *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.__request('delete', *args, **kwargs)

    def put(self, *args, **kwargs):
        return self.__request('put', *args, **kwargs)
