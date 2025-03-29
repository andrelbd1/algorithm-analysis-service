import logging

from webargs import fields
from webargs.tornadoparser import parser

from src.api import InternalRequestHandler
from src.api.v1.swagger.execution import register_swagger_model
from src.config import ApplicationConfig
from src.controllers.execution import ControllerExecution
from src.tasks.execution import queue_execution

config_app = ApplicationConfig()

__all__ = [register_swagger_model]

logger = logging.getLogger(__file__)


class ViewExecution(InternalRequestHandler):

    @property
    def __params_body(self):
        return {
          "algorithm_id": fields.Str(required=True),
          "input": fields.List(fields.Dict(), required=True),
          "alias": fields.Str()
        }

    @property
    def _controller_execution(self):
        return ControllerExecution()

    @property
    def _params(self):
        return parser.parse(self.__params_body, self.request, location="json")


class ViewGetExecution(ViewExecution):

    async def __get_execution_by_id(self, p_id):
        result = self._controller_execution.get(p_id)
        logger.info("Get execution", extra=self._log_extra)
        return result

    async def __delete_execution_by_id(self, p_id):
        self._controller_execution.set_enabled_to_false(p_id)
        logger.info("Delete execution", extra=self._log_extra)
        return {"msg": "deleted success"}

    @InternalRequestHandler.api_method_wrapper
    async def get(self, id):
        """
        ---
        tags:
        - Execution
        summary: Get result execution
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
                example: 0195dfda-3263-82cc-6b25-9a302b1df9b5
        responses:
            SyncApiDefaultResponse:
              description: response Sync Api Successfully
              schema:
                $ref: '#/definitions/ResponseGetExecutionSuccessfully'
            SyncApiError:
              description: request return known error
              schema:
                $ref: '#/definitions/DefaultExceptionError'
        """
        return await self.__get_execution_by_id(id)

    @InternalRequestHandler.api_method_wrapper
    async def delete(self, id):
        """
        ---
        tags:
        - Execution
        summary: Delete execution
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
                example: 21d88834-5021-5fff-a66f-0069f40ec3e7
        responses:
            SyncApiDefaultResponse:
              description: response Sync Api Successfully
              schema:
                $ref: '#/definitions/ResponseDeleteExecutionSuccessfully'
            SyncApiError:
              description: request return known error
              schema:
                $ref: '#/definitions/DefaultExceptionError'
        """
        return await self.__delete_execution_by_id(id)


class ViewPostExecution(ViewExecution):

    # async def __list_objects(self):
    #     params = parser.parse(
    #         self.param_search_by, self.request, location="querystring"
    #     )
    #     logger.info("list objects execution", extra=self._log_extra)
    #     params.update(self._log_extra)
    #     # result = self._controller_execution.list_objects(params)
    #     logger.info("Get list objects", extra=self._log_extra)
    #     return result

    async def __create_execution(self):
        params = self._params
        logger.info("request create execution", extra=self._log_extra)
        params.update(self._log_extra)
        execution_id = self._controller_execution.add(params)
        params_queue = {"execution_id": execution_id}
        params_queue.update(self._log_extra)
        queue_execution(params_queue)
        return {"id": str(execution_id)}

    # @InternalRequestHandler.api_method_wrapper
    # async def get(self, *args):
    #     """
    #     ---
    #     tags:
    #     - Execution
    #     summary: List of executions
    #     produces:
    #     - application/json
    #     parameters:
    #       - in: header
    #         name: X-Individual-Id
    #       - in: header
    #         name: X-Request-Id
    #       - name: amount
    #         in: query
    #         description: amount item
    #         required: true
    #         schema:
    #           type: number
    #           example: 20
    #       - name: page
    #         in: query
    #         description: page for search
    #         required: true
    #         schema:
    #           type: number
    #           example: 0
    #       - name: value
    #         in: query
    #         description: value for search
    #         schema:
    #           type: string
    #           example: "DynamoDB-4931d97b-27bc-483a-90ff-20a63c69627c"
    #       - name: search_by
    #         in: query
    #         description: value to search "execution_id", "origin_dbName", "status", "alias", "tenant_id", "is_scheduled", "result"
    #         required: true
    #         schema:
    #           type: string
    #           example: "origin_dbName"
    #     responses:
    #         SyncApiDefaultResponse:
    #           description: response Sync Api Successfully
    #           schema:
    #             $ref: '#/definitions/ResponseListExecutionSuccessfully'
    #         SyncApiError:
    #           description: request return known error
    #           schema:
    #             $ref: '#/definitions/DefaultExceptionError'
    #     """
    #     return await self.__list_objects()

    @InternalRequestHandler.api_method_wrapper
    async def post(self, *body):
        """
        ---
        tags:
        - Execution
        summary: Request Create Execution
        produces:
        - application/json
        parameters:
          - in: header
            name: X-Individual-Id
          - in: header
            name: X-Request-Id
          - in: body
            name: params
            description: Params
            required: true
            schema:
              $ref: '#/definitions/PostCreateExecution'
        responses:
            SyncApiDefaultResponse:
              description: response Sync Api Successfully
              schema:
                $ref: '#/definitions/PostCreateExecutionSuccess'
            SyncApiError:
              description: request return known error
              schema:
                $ref: '#/definitions/DefaultExceptionError'
        """
        return await self.__create_execution()
