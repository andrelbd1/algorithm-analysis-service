import json

import mock

from tests import BaseTestClassTornado


class TestHealthcheck(BaseTestClassTornado):

    def setUp(self):
        super(TestHealthcheck, self).setUp()
        self._url = "/healthcheck"

    @mock.patch('src.api.healthcheck.OrmConnect', mock.MagicMock())
    def test_health_check(self):
        response = self.fetch(self._url)
        self.assertEqual(response.code, 200)
        resp = json.loads(response.body.decode("utf8"))
        self.assertEqual(resp["database"], True)

    @mock.patch('src.api.healthcheck.OrmConnect')
    def test_health_check_error_query(self, mock_orm):
        mock_orm().orm.test_connection_database.side_effect = Exception("erro Database")
        response = self.fetch(self._url, method="GET")
        resp = json.loads(response.body.decode("utf8"))
        self.assertEqual(response.code, 200)
        self.assertEqual(resp["database"], False)
