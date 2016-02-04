from REST_UBER.swagger_ui import ApiSpec


class Documentation(ApiSpec):
    def __init__(self, model_name):
        """
        Provides the API documentation for Earthworm
        """
        description = "Earthworm Model"
        super(Documentation, self).__init__(model_name, description)
