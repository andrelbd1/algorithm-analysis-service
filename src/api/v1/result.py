import logging

from webargs import fields
from webargs.tornadoparser import parser

from src.api import InternalRequestHandler
from src.api.v1.swagger.result import register_swagger_model
from src.common.functions import validate_date, validate_uuid, validate_non_negative_integer
from src.config import ApplicationConfig
from src.controllers.result import ControllerResult

config_app = ApplicationConfig()

__all__ = [register_swagger_model]

logger = logging.getLogger(__file__)


class ViewResult(InternalRequestHandler):

    @property
    def __params_body(self):
        return {
          "algorithm_id": fields.Str(required=True, validate=validate_uuid),
          "alias": fields.Str()
        }

    @property
    def _controller_result(self):
        return ControllerResult()

    @property
    def _params(self):
        return parser.parse(self.__params_body, self.request, location="json")


class ViewGetReport(ViewResult):

    __param_search_by = {
        "alias": fields.Str(required=False),
        "request_date": fields.Str(required=False, validate=validate_date),
        "page": fields.Int(required=True, dump_default=0, validate=validate_non_negative_integer),
        "amount": fields.Int(required=True, dump_default=20, validate=validate_non_negative_integer),
    }

    async def __evaluation_report_list(self, algorithm_id, criteria_id, input_id):
        validate_uuid(algorithm_id)
        validate_uuid(criteria_id)
        validate_uuid(input_id)
        params = {
            "algorithm_id": algorithm_id,
            "criteria_id": criteria_id,
            "input_id": input_id
        }
        params_parse = parser.parse(
            self.__param_search_by, self.request, location="querystring"
        )
        params.update(params_parse)
        logger.info("list evaluation report", extra=self._log_extra)
        params.update(self._log_extra)
        result = self._controller_result.report(params)
        logger.info("Get list evaluation report", extra=self._log_extra)
        return result

    @InternalRequestHandler.api_method_wrapper
    async def get(self, algorithm_id, criteria_id, input_id):
        """
        ---
        tags:
        - Result
        summary: List of evaluation results
        description: ''
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
              minimum: 0
              maximum: 100
          - name: page
            in: query
            description: page for search
            required: true
            schema:
              type: number
              example: 0
              minimum: 0
          - name: algorithm_id
            in: path
            description: value to search by algorithm id.
            required: true
            schema:
              type: string
              example: "0192919b-2501-2fea-a93d-5d5541c4002b"
          - name: criteria_id
            in: path
            description: value for search by criteria id.
            required: true
            schema:
              type: string
              example: "001fe2d3-09a5-4bc0-b891-45d475a4b1bc"
          - name: input_id
            in: path
            description: value for search by input id.
            required: true
            schema:
              type: string
              example: "0192919b-2501-585f-1492-4f5d22c98267"
          - name: alias
            in: query
            description: value for search by alias
            schema:
              type: string
          - name: request_date
            in: query
            description: value for search by request date ("YYYY-MM-DD")
            schema:
              type: string
        responses:
            SyncApiDefaultResponse:
              description: response Sync Api Successfully
              schema:
                $ref: '#/definitions/ResponseGetEvaluationReportListSuccessfully'
            SyncApiError:
              description: request return known error
              schema:
                $ref: '#/definitions/DefaultExceptionError'
        """
        return await self.__evaluation_report_list(algorithm_id, criteria_id, input_id)
