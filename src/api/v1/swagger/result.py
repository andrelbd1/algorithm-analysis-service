from . import register_swagger_model


@register_swagger_model
class ResponseGetEvaluationReportListSuccessfully:
    """
    ---
    type: object
    description: Route used to return a report grouping evaluation results by algorithm, input, and criteria.
    example: {
        "total_items": 1,
        "report": [
            {
                "input_value": "5",
                "average": "0.000002165000000000000000",
                "unit": "secs"
            }
        ]
    }
    """
