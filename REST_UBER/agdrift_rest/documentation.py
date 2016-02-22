TAG_DESCRIPTION = "AgDrift Model"

SHORT_DESCRIPTION = "The primary function of AgDRIFT is to calculate the downward drift and deposition of pesticides " \
                    "and the magnitude of buffer zones needed to protect sensitive aquatic and terrestrial habitats. " \
                    "The Tier I model methodology uses different application type and drop size distributions to " \
                    "yield a conservative exposure estimate."

CONSUMES = ["application/json"]

PRODUCES = ["application/json"]

PARAMETERS = [
    {
        "description": "Run AgDrift model",
        "required": True,
    }
]

RESPONSES = {
    "200": {
        "description": "Successful Operation",
    }
}
