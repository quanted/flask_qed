

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
