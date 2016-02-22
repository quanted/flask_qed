TAG_DESCRIPTION = "Earthworm Model"

SHORT_DESCRIPTION = 'Earthworm Fugacity Modeling is a simple fugacity approach was employed to estimate pesticides ' \
                    'concentrations in earthworms. Fugacity is most often regarded as the "escaping tendency" of a ' \
                    'chemical from a particular phase. Fugacity has units of presure, generally pascals (Pa), and ' \
                    'can be related to phase concentratons.'

CONSUMES = ["application/json"]

PRODUCES = ["application/json"]

PARAMETERS = [
    {
        "description": "Run Earthworm model",
        "required": True,
    }
]

RESPONSES = {
    "200": {
        "description": "Successful Operation",
    }
}
