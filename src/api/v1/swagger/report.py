from . import register_swagger_model


@register_swagger_model
class ResponseDeleteReportSuccessfully:
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
class PostCreateReport:
    """
    ---
    type: object
    description: Route used to request reports
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
                        description: A string representing any value (e.g., an integer to calculate factorial, graph set as a list of nodes and edges)
                        example: "20"
            required: true
        report_alias:
            type: string
            example: "Report_2025_01_01_16_06_41"
            description: Alias to search reports
            required: false
    """


@register_swagger_model
class PostCreateReportSuccess:
    """
    ---
    type: object
    description: ID of process alerts
    properties:
        id:
            type: string
            example: "21d88834-5021-5fff-a66f-0069f40ec3e7"
        report_alias:
            type: string
            example: "Report_2025_01_01_16_06_41"
    """
