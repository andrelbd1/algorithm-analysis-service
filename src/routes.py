from tornado.web import url

from src.api.healthcheck import ServiceAlgorithmAnalysisAPI
from src.api.v1.algorithm import ViewDeleteAlgorithm, ViewGetAlgorithm


class Routes:
    list = [
        url(r'/healthcheck', ServiceAlgorithmAnalysisAPI),
        url(r'/v1/algorithm/([^/]*)', ViewDeleteAlgorithm),
        url(r'/v1/algorithm', ViewGetAlgorithm),
    ]
