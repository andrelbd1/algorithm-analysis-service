import logging

from src.api import InternalRequestHandler
from src.config import ApplicationConfig
from src.models.src_orm import OrmConnect

config_app = ApplicationConfig()
logger = logging.getLogger(__name__)


class AlgorithmAnalysisService(InternalRequestHandler):
    def __check_postgresql(self):
        try:
            orm_connect = OrmConnect()
            orm_connect.orm.test_connection_database()
            status = True
        except Exception as error:
            status = False
            logger.exception(str(error))
        return status

    @InternalRequestHandler.api_method_wrapper
    async def get(self):
        """
        ---
        tags:
        - HealthCheck
        summary: Get HealthCheck
        description: 'validate api dependencies'
        produces:
        - application/json
        responses:
            200:
              description: list of dependencies
              schema:
                type: object
                properties:
                    database:
                        type: boolean
                        example: true
        """

        data = {"database": self.__check_postgresql()}
        logger.health("response healthcheck {}".format(data))
        return data
