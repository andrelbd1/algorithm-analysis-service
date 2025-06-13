from tornado.web import url

from src.routes import Routes
from tests import BaseTestClass


class TestRoutes(BaseTestClass):

    def test_have_routes(self):
        assert len(Routes.list) > 0

    def test_routes_are_urls(self):
        for item in Routes.list:
            assert isinstance(item, url)