

# TODO: Remove JsonDefinitions, as it is not used
class JsonDefinitions(object):
    def __init__(self):
        """
        'Definitions' key for JSON schema.  Definitions are reusable JSON code segments.
        http://spacetelescope.github.io/understanding-json-schema/structuring.html
        """
        self.definitions = {
            "definitions": {}
        }

    def chemical_name(self):
        return {
            'chemical_name': {
                'type': 'string',
                'example': 'Chemical X'
            }
        }


class ApiSpec(object):
    def __init__(self, model_name, description):
        """
        Provides the API documentation JSON for Swagger
        """
        self.path = PathJSON(model_name, 'method')
        self.tag = TagJSON(model_name, description)


class PathJSON(object):
    def __init__(self, model_name, method):
        """
        Paths Object
        :param model_name:
        :param method:
        """
        self.path_item = {
            method: OperationJSON(model_name)
        }
        # self.json = dict(method=self.method.json)


class OperationJSON(object):
    def __init__(self, model_name):
        """
        Operation Object
        :param model_name:
        """
        self.json = dict(
            tags=[model_name],
            summary=""
        )


class TagJSON(object):
    def __init__(self, model_name, description):
        self.json = {
            'name': model_name,
            'description': description
        }
