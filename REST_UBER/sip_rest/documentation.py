TAG_DESCRIPTION = "SIP Model"

SHORT_DESCRIPTION = "The SIP model is designed to estimate chemical exposure from drinking water alone in birds " \
                    "and mammals."

CONSUMES = ["application/json"]

PRODUCES = ["application/json"]

PARAMETERS = [
    {
        "description": "Run SIP model",
        "required": True,
    }
]

RESPONSES = {
    "200": {
        "description": "Successful Operation",
    }
}
