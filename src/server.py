import asyncio
import logging
import os
import typing

import tornado
# from elasticapm.contrib.tornado import ElasticAPM
from tornado.httpserver import HTTPServer
from tornado.netutil import bind_sockets
from tornado.web import Application
from tornado_swagger.setup import (API_SWAGGER_2, STATIC_PATH,
                                   SwaggerSpecHandler, SwaggerUiHandler,
                                   generate_doc_from_endpoints)

from src.config import ApplicationConfig
from src.routes import Routes

config_app = ApplicationConfig()
logger = logging.getLogger(__file__)


class OverwriteSetupSwagger:
    def setup_swagger(
        self,
        routes: typing.List[tornado.web.URLSpec],
        *,
        swagger_url: str = "/api/doc",
        api_base_url: str = "/",
        description: str = "Swagger API definition",
        api_version: str = "1.0.0",
        title: str = "Swagger API",
        contact: str = "",
        schemes: list = None,
        security_definitions: dict = None,
        security: list = None,
        display_models: bool = True,
        api_definition_version: str = API_SWAGGER_2
    ):
        """Inject swagger ui to application routes"""
        swagger_schema = generate_doc_from_endpoints(
            routes,
            api_base_url=api_base_url,
            description=description,
            api_version=api_version,
            title=title,
            contact=contact,
            schemes=schemes,
            security_definitions=security_definitions,
            security=security,
            api_definition_version=api_definition_version,
        )
        if swagger_url.startswith("/"):
            swagger_url = swagger_url[1:]
        if api_base_url.endswith("/"):
            api_base_url = api_base_url[:-1]
        _swagger_ui_url = "/{}".format(swagger_url) if not swagger_url.startswith("/") else swagger_url
        _base_swagger_ui_url = _swagger_ui_url.rstrip("/")
        _swagger_spec_url = "{}/swagger.json".format(_swagger_ui_url)
        url_json = "{base}/{swagger}/swagger.json".format(base=api_base_url, swagger=swagger_url)
        routes[:0] = [
            tornado.web.url(_swagger_ui_url, SwaggerUiHandler),
            tornado.web.url("{}/".format(_base_swagger_ui_url), SwaggerUiHandler),
            tornado.web.url(_swagger_spec_url, SwaggerSpecHandler),
        ]
        SwaggerSpecHandler.SWAGGER_SPEC = swagger_schema
        with open(os.path.join(STATIC_PATH, "ui.html"), "r", encoding="utf-8") as f:
            SwaggerUiHandler.SWAGGER_HOME_TEMPLATE = (
                f.read().replace("{{ SWAGGER_URL }}",
                                 url_json).replace("{{ DISPLAY_MODELS }}",
                                                   str(-1 if not display_models else 1))
            )


class ApiServer:
    __sockets = None

    # @staticmethod
    # def add_apm(app):
    #     if config_app.ELASTIC_APM_SERVER_URL:
    #         apm = ElasticAPM(app)
    #         app.settings.update({"apm_elastic": apm})

    def make_app(self):
        OverwriteSetupSwagger().setup_swagger(
            Routes.list,
            api_base_url=ApplicationConfig.BASE_PATH,
            swagger_url="/doc",
            description=ApplicationConfig.NAME,
            api_version=ApplicationConfig.VERSION,
            title=ApplicationConfig.NAME,
        )
        app = Application(Routes.list, **ApplicationConfig.APPLICATION_SETTINGS)
        # self.add_apm(app)
        return app

    def bind_port(self):
        self.__sockets = bind_sockets(config_app.PORT_API)
        tornado.process.fork_processes(config_app.AMOUNT_PROCESS_API)

    async def start(self):
        logger.info("starting server")
        app = self.make_app()
        server = HTTPServer(app, max_buffer_size=config_app.MAX_BUFFER_SIZE)
        server.add_sockets(self.__sockets)
        await asyncio.Event().wait()
