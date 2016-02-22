TAG_DESCRIPTION = "IEC Model"

SHORT_DESCRIPTION = "IECV1.1 (Individual Effect Chance Model Version 1.1) estimates potential effects at an " \
                    "individual level. Generally, available toxicity data provides an LC50 or an EC50, (the " \
                    "concentration at which 50% of the test population exhibits the designated endpoint, usually " \
                    "mortality)."

CONSUMES = ["application/json"]

PRODUCES = ["application/json"]

PARAMETERS = [
    {
        "description": "Run IEC model",
        "required": True,
    }
]

RESPONSES = {
    "200": {
        "description": "Successful Operation",
    }
}
