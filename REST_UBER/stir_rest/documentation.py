TAG_DESCRIPTION = "STIR Model"

SHORT_DESCRIPTION = "The STIR model was developed as a screening model to estimate inhalation risk of chemicals to " \
                    "birds and mammals. Chemical specific physical properties are required for executing the model. " \
                    "Vapor phase and droplet-spray exposure risks are estimated in STIR and then compared to avian " \
                    "inhalation or mammalian inhalation and oral toxicity data. Inhalation exposure routes addressed " \
                    "by the model include directly applied spray, volatilization of residues on plant canopy and " \
                    "volatilization of residues in soil."

CONSUMES = ["application/json"]

PRODUCES = ["application/json"]

PARAMETERS = [
    {
        "description": "Run STIR model",
        "required": True,
    }
]

RESPONSES = {
    "200": {
        "description": "Successful Operation",
    }
}
