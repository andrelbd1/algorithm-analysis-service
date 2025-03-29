from . import register_swagger_model


@register_swagger_model
class ResponseDeleteExecutionSuccessfully:
    """
    ---
    type: object
    description: Post To Response Successfully
    properties:
        msg:
            type: string
            example: "deleted success"
    """


@register_swagger_model
class ResponseGetExecutionSuccessfully:
    """
    ---
    type: object
    description: Route used to return report status.
    example: {
        "executions": [
            {
                "execution_id": "0192919b-2501-2fea-a93d-5d5541c4002b",
                "payload": {
                    "algorithm_id": "0192919b-2501-2fea-a93d-5d5541c4002b",
                    "algorithm_name": "Dijkstra",
                    "input": [
                        {
                            "id": "0192919b-2501-585f-1492-4f5d22c98267",
                            "name": "factorial number",
                            "value": "20"
                        }
                    ],
                    "alias": "Execution_2024_07_18_11_27_07",
                },
                "status": "DONE",
                "message": null,
                "request_date": "2024-03-28T15:13:39.995092",
                "result": [
                    {
                        "criteria": "",
                        "value": "",
                        "unit": "",
                        "message": null,
                        "status": "DONE"
                    }
                ]
            }
        ]
    }
    """


@register_swagger_model
class PostCreateExecution:
    """
    ---
    type: object
    description: Route used to request executions
    properties:
        algorithm_id:
            type: string
            example: "0192919b-2501-2fea-a93d-5d5541c4002b"
            required: true
        input:
            type: array
            items:
                type: object
                properties:
                    id:
                        type: string
                        example: "0192919b-2501-585f-1492-4f5d22c98267"
                        required: true
                        description: Input id
                    value:
                        type: string
                        description: A string representing any value (e.g., an integer to calculate factorial, graph set as a list of nodes, and edges)
                        example: "20"
            required: true
        alias:
            type: string
            example: "Execution_2025_01_01_16_06_41"
            description: Alias to search executions
            required: false
    """


@register_swagger_model
class PostCreateExecutionSuccess:
    """
    ---
    type: object
    description: ID of process alerts
    properties:
        id:
            type: string
            example: "21d88834-5021-5fff-a66f-0069f40ec3e7"
        alias:
            type: string
            example: "Execution_2025_01_01_16_06_41"
    """
