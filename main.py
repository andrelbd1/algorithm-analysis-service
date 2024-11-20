import asyncio
import sys

from src.server import ApiServer
# from src.tasks import celery_app


def server():
    server = ApiServer()
    server.bind_port()
    asyncio.run(server.start())


def main(p_params):
    """Principal function."""
    if "server" in p_params:
        server()


if __name__ == '__main__':
    main(sys.argv[1:])
