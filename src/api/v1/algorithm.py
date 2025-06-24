import logging

from webargs.tornadoparser import parser

from src.api import InternalRequestHandler
from src.api.v1.swagger.algorithm import register_swagger_model
from src.config import ApplicationConfig
from src.controllers.algorithm import ControllerAlgorithm

config_app = ApplicationConfig()

__all__ = [register_swagger_model]

logger = logging.getLogger(__file__)


class ViewAlgorithm(InternalRequestHandler):

    @property
    def _controller_algorithm(self):
        return ControllerAlgorithm()

    @property
    def _params(self):
        return parser.parse(self.__params_body, self.request, location="json")


class ViewDeleteAlgorithm(ViewAlgorithm):

    async def __delete_algorithm_by_id(self, p_id):
        self._controller_algorithm.delete(p_id)
        logger.info("Delete algorithm", extra=self._log_extra)
        return {"msg": "deleted success"}

    @InternalRequestHandler.api_method_wrapper
    async def delete(self, id):
        """
        ---
        tags:
        - Algorithm
        summary: Delete Algorithm
        description: ''
        produces:
        - application/json
        parameters:
          - in: header
            name: X-Individual-Id
          - in: header
            name: X-Request-Id
          - name: id
            in: path
            description: id
            required: true
            schema:
                type: string
                example: 859c1491-ce58-4eec-adae-28fa4b895d21
        responses:
            SyncApiDefaultResponse:
              description: response Sync Api Successfully
              schema:
                $ref: '#/definitions/ResponseDeleteAlgorithmSuccessfully'
            SyncApiError:
              description: request return known error
              schema:
                $ref: '#/definitions/DefaultExceptionError'
        """
        return await self.__delete_algorithm_by_id(id)


class ViewGetAlgorithm(ViewAlgorithm):

    async def __list_objects(self):
        params = parser.parse(
            self.param_search_by, self.request, location="querystring"
        )
        logger.info("list objects algorithm", extra=self._log_extra)
        params.update(self._log_extra)
        result = self._controller_algorithm.list_objects(params)
        logger.info("Get list objects", extra=self._log_extra)
        return result

    @InternalRequestHandler.api_method_wrapper
    async def get(self, *args):
        """
        ---
        tags:
        - Algorithm
        summary: List item of algorithms
        produces:
        - application/json
        parameters:
          - in: header
            name: X-Individual-Id
          - in: header
            name: X-Request-Id
          - name: amount
            in: query
            description: amount item
            required: true
            schema:
              type: number
              example: 20
          - name: page
            in: query
            description: page for search
            required: true
            schema:
              type: number
              example: 0
          - name: search_by
            in: query
            description: value to search "algorithm_id" and "name"
            required: false
            schema:
              type: string
              example: "algorithm_id"
          - name: value
            in: query
            description: value for search
            schema:
              type: string
              example: "0192919b-2501-2fea-a93d-5d5541c4002b"
        responses:
            SyncApiDefaultResponse:
              description: response Sync Api Successfully
              schema:
                $ref: '#/definitions/ResponseListAlgorithmSuccessfully'
            SyncApiError:
              description: request return known error
              schema:
                $ref: '#/definitions/DefaultExceptionError'
        """
        return await self.__list_objects()
