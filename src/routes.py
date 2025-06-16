from tornado.web import url

from src.api.healthcheck import AlgorithmAnalysisService
from src.api.v1.algorithm import ViewDeleteAlgorithm, ViewGetAlgorithm
from src.api.v1.execution import ViewGetExecution, ViewPostExecution
from src.api.v1.result import ViewGetReport


class Routes:
    list = [
        url(r'/healthcheck', AlgorithmAnalysisService),
        url(r'/v1/algorithm/([^/]*)', ViewDeleteAlgorithm),
        url(r'/v1/algorithm', ViewGetAlgorithm),
        url(r'/v1/execution/([^/]*)', ViewGetExecution),
        url(r'/v1/execution', ViewPostExecution),
        url(r'/v1/result/evaluation-report/algorithm/([^/]*)/criteria/([^/]*)/input/([^/]*)', ViewGetReport),
    ]
