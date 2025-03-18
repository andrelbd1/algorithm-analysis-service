import logging

from webargs import fields
from webargs.tornadoparser import parser

from src.api import InternalRequestHandler
from src.api.v1.swagger.report import register_swagger_model
# from src.common.functions import validate_date
from src.config import ApplicationConfig
from src.controllers.report import ControllerReport
from src.exceptions import ParamInvalid
# from src.tasks.process_report import queue_process_report

config_app = ApplicationConfig()

__all__ = [register_swagger_model]

logger = logging.getLogger(__file__)


class ViewReport(InternalRequestHandler):

    @property
    def __params_body(self):
        return {
          "algorithm_id": fields.Str(required=True),
          "input": fields.List(fields.Dict(), required=True),
          "report_alias": fields.Str()
        }

    @property
    def _controller_report(self):
        return ControllerReport()

    @property
    def _params(self):
        return parser.parse(self.__params_body, self.request, location="json")


class ViewGetReport(ViewReport):

    # async def __get_report_by_id(self, p_id):
        # result = self._controller_report.get(p_id)
        # logger.info("Get report", extra=self._log_extra)
        # return result

    async def __delete_report_by_id(self, p_id):
        # self._controller_report.set_enabled_to_false(p_id)
        logger.info("Delete report", extra=self._log_extra)
        return {"msg": "deleted success"}

    @InternalRequestHandler.api_method_wrapper
    async def get(self, id):
        """
        ---
        tags:
        - Report
        summary: Get result report
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
                $ref: '#/definitions/ResponseGetReportSuccessfully'
            SyncApiError:
              description: request return known error
              schema:
                $ref: '#/definitions/DefaultExceptionError'
        """
        return await self.__get_report_by_id(id)

    @InternalRequestHandler.api_method_wrapper
    async def delete(self, id):
        """
        ---
        tags:
        - Report
        summary: Delete report
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
                $ref: '#/definitions/ResponseDeleteReportSuccessfully'
            SyncApiError:
              description: request return known error
              schema:
                $ref: '#/definitions/DefaultExceptionError'
        """
        return await self.__delete_report_by_id(id)


class ViewPostReport(ViewReport):

    # async def __list_objects(self):
    #     params = parser.parse(
    #         self.param_search_by, self.request, location="querystring"
    #     )
    #     logger.info("list objects report", extra=self._log_extra)
    #     params.update(self._log_extra)
    #     # result = self._controller_report.list_objects(params)
    #     logger.info("Get list objects", extra=self._log_extra)
    #     return result

    async def __create_report(self):
        params = self._params
        logger.info("request create report", extra=self._log_extra)
        params.update(self._log_extra)
        report_id = self._controller_report.add(params)
        params_queue = {"report_id": report_id}
        params_queue.update(self._log_extra)
        # queue_process_report(params_queue)
        return {"id": str(report_id)}

    # @InternalRequestHandler.api_method_wrapper
    # async def get(self, *args):
    #     """
    #     ---
    #     tags:
    #     - Report
    #     summary: List of reports
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
    #         description: value to search "report_id", "origin_dbName", "status", "alias", "tenant_id", "is_scheduled", "result"
    #         required: true
    #         schema:
    #           type: string
    #           example: "origin_dbName"
    #     responses:
    #         SyncApiDefaultResponse:
    #           description: response Sync Api Successfully
    #           schema:
    #             $ref: '#/definitions/ResponseListReportSuccessfully'
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
        - Report
        summary: Request Create Report
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
              $ref: '#/definitions/PostCreateReport'
        responses:
            SyncApiDefaultResponse:
              description: response Sync Api Successfully
              schema:
                $ref: '#/definitions/PostCreateReportSuccess'
            SyncApiError:
              description: request return known error
              schema:
                $ref: '#/definitions/DefaultExceptionError'
        """
        return await self.__create_report()
