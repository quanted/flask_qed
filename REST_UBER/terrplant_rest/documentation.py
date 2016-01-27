

class ApiSpec(object):
    def __init__(self, definitions):
        """
        Provides the API documentation for Terrplant
        :param definitions: REST_UBER.swagger_ui.JsonDefinitions class instance
        """
        self.definitions = definitions
        self.description = "Provide model inputs to return model output"

    def schema(self):
        return {
            "inputs": {
                "ec25_nonlisted_seedling_emergence_dicot": {"0": "0.034"},
                "use": {"0": "Corn"},
                "application_rate": {"0": "4"},
                "version_terrplant": {"0": "1.2.2"},
                "incorporation_depth": {"0": "1"},
                "noaec_listed_seedling_emergence_monocot": {"0": "0.0023"},
                "drift_fraction": {"0": "0.01"},
                "noaec_listed_seedling_emergence_dicot": {"0": "0.019"},
                "solubility": {"0": "240"},
                "chemical_name": {"0": "Terrplant Example"},
                "pc_code": {"0": "90501"},
                "noaec_listed_vegetative_vigor_monocot": {"0": "0.037"},
                "ec25_nonlisted_vegetative_vigor_monocot": {"0": "0.068"},
                "ec25_nonlisted_seedling_emergence_monocot": {"0": "0.0067"},
                "application_method": {"0": "Ground"},
                "ec25_nonlisted_vegetative_vigor_dicot": {"0": "1.4"},
                "application_form": {"0": "Spray"},
                "runoff_fraction": {"0": "0.05"},
                "noaec_listed_vegetative_vigor_dicot": {"0": "0.67"}},
            "run_type": "single"
        }
