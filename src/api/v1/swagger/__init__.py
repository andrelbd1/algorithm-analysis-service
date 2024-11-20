
from tornado_swagger.model import register_swagger_model


__all__ = [register_swagger_model]


@register_swagger_model
class DefaultExceptionError:
    """
    ---
    type: object
    description: Default Response Error
    properties:
        message:
            type: string
            example: Error Internal Server
        status:
            type: string
            example: fail
    """
