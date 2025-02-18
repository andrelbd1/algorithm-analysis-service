from . import register_swagger_model


@register_swagger_model
class ResponseDeleteAlgorithmSuccessfully:
    """
    ---
    type: object
    description: Delete to Response Algorithm Successfully
    properties:
        msg:
            type: string
            example: "deleted success"
    """


@register_swagger_model
class ResponseListAlgorithmSuccessfully:
    """
    ---
    type: object
    description: Route used to return available algorithm.
    example: {
        "total_items": 1,
        "algorithms": [
            {
                "algorithm_id": "0192919b-2501-2fea-a93d-5d5541c4002b",
                "name": "Factorial",
                "description": "A function that multiplies a positive integer by all the positive integers that are less than or equal to it",
                "input": [
                    {
                        "input_id": "0192919b-2501-585f-1492-4f5d22c98267",
                        "name": "factorial number",
                        "input_type": integer,
                        "description": "number to calculate factorial",
                    }
                ]
            }
        ]
    }
    """
