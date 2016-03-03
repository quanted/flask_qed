import yaml
import os


class ApiSpec(object):
    def __init__(self, model, http_methods):
        """
        Provides the API documentation JSON for Swagger UI front end.  Swagger JSON specifications can be found
        at: http://swagger.io/specification

        Example Swagger compliant JSON (http://petstore.swagger.io):

        {
            "swagger": "2.0",
            "info": {
                "description": "This is a sample server Petstore server.",
                "version": "1.0.0",
                "title": "Swagger Petstore",
                "termsOfService": "http://swagger.io/terms/",
                "contact": {
                    "email": "apiteam@swagger.io"
                },
                "license": {
                    "name": "Apache 2.0",
                    "url": "http://www.apache.org/licenses/LICENSE-2.0.html"
                }
            },
            "host": "www.example.com",
            "basePath": "/",
            "externalDocs": {
                "description": "Find out more about Swagger",
                "url": "http://swagger.io"
            }
            "tags": [{
                "name": "pet",
                "description": "Everything about your Pets",
            }, {
                "name": "store",
                "description": "Access to Petstore orders"
            }],
            "schemes": ["http"],
            "paths": {
                "/pet": {
                    "post": {
                        "tags": ["pet"],
                        "summary": "Add a new pet to the store",
                        "description": "",
                        "operationId": "addPet",
                        "consumes": ["application/json", "application/xml"],
                        "produces": ["application/xml", "application/json"],
                        "parameters": [{
                            "in": "body",
                            "name": "body",
                            "description": "Pet object that needs to be added to the store",
                            "required": true,
                            "schema": {
                                "$ref": "#/definitions/Pet"
                            }
                        }],
                        "responses": {
                            "405": {
                                "description": "Invalid input"
                            }
                        }
                    },
                },
                "/pet/findByStatus": {
                    "get": {
                        "tags": ["pet"],
                        "summary": "Finds Pets by status",
                        "description": "Multiple status values can be provided with comma separated strings",
                        "operationId": "findPetsByStatus",
                        "produces": ["application/xml", "application/json"],
                        "parameters": [{
                            "name": "status",
                            "in": "query",
                            "description": "Status values that need to be considered for filter",
                            "required": true,
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": ["available", "pending", "sold"],
                                "default": "available"
                            },
                            "collectionFormat": "multi"
                        }],
                        "responses": {
                            "200": {
                                "description": "successful operation",
                                "schema": {
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/definitions/Pet"
                                    }
                                }
                            },
                            "400": {
                                "description": "Invalid status value"
                            }
                        }
                    }
                },
            },
            "definitions": {
                "Pet": {
                    "type": "object",
                    "required": ["name", "photoUrls"],
                    "properties": {
                        "id": {
                            "type": "integer",
                            "format": "int64"
                        },
                        "category": {
                            "$ref": "#/definitions/Category"
                        },
                        "name": {
                            "type": "string",
                            "example": "doggie"
                        },
                        "photoUrls": {
                            "type": "array",
                            "xml": {
                                "name": "photoUrl",
                                "wrapped": true
                            },
                            "items": {
                                "type": "string"
                            }
                        },
                        "tags": {
                            "type": "array",
                            "xml": {
                                "name": "tag",
                                "wrapped": true
                            },
                            "items": {
                                "$ref": "#/definitions/Tag"
                            }
                        },
                        "status": {
                            "type": "string",
                            "description": "pet status in the store",
                            "enum": ["available", "pending", "sold"]
                        }
                    },
                    "xml": {
                        "name": "Pet"
                    }
                }
            }

        }
        """
        self.PROJECT_ROOT = os.environ['PROJECT_ROOT']
        self.model = model
        self.http_methods = http_methods
        self.summary = None
        self.description = None
        self.consumes = None
        self.produces = None
        self.parameters = None
        self.responses = None

        self.parse_yaml()

        # TODO: Add validation logic

        self.path = PathJSON(model, 'post')
        self.tag = TagJSON(model, self.summary)

        self.update()

    def parse_yaml(self):
        yaml_path = os.path.join(self.PROJECT_ROOT, 'REST_UBER', self.model + '_rest', 'apidoc.yaml')
        with open(yaml_path, 'r') as f:
            api_doc = yaml.load(f)

        self.summary = api_doc['summary']
        self.description = api_doc['description']
        self.consumes = api_doc['consumes']
        self.produces = api_doc['produces']
        self.parameters = api_doc['parameters']
        self.responses = api_doc['responses']

    def update(self):

        # Handle custom SCHEMA supplied in 'documentation.PARAMETERS'
        for i, param in enumerate(self.parameters):
            if 'schema' in param:
                print "SCHEMA is present"
                # TODO: Add custom schema AND validate its format
            else:
                print "SCHEMA is NOT present"
                self.parameters[i]['schema'] = {'$ref': '#/definitions/' + self.model.capitalize() + 'Inputs'}
                # TODO: Make 'in' and 'name' descriptors generic
                self.parameters[i]['in'] = 'body'
                self.parameters[i]['name'] = 'body'

        # Handle custom SCHEMA supplied in 'documentation.RESPONSES'
        for code, desc in self.responses.items():
            if 'schema' in desc:
                print "SCHEMA is present"
                # TODO: Add custom schema AND validate its format
            else:
                print "SCHEMA is NOT present"
                self.responses[code]['schema'] = {'$ref': '#/definitions/' + self.model.capitalize() + 'Outputs'}

        api_doc = dict(
            summary=self.summary,
            description=self.description,
            consumes=self.consumes,
            produces=self.produces,
            parameters=self.parameters,
            responses=self.responses
        )
        self.path.operation.json.update(api_doc)


class PathJSON(object):
    def __init__(self, model_name, method):
        """
        Paths Object
        :param model_name:
        :param method:
        """
        self.operation = OperationJSON(model_name)
        self.path_item = {
            method: self.operation.json
        }


class OperationJSON(object):
    def __init__(self, model_name):
        """
        Operation Object
        :param model_name:
        """
        self.type = OperationContentTypes()
        self.parameters = OperationParameters()
        self.responses = OperationResponses()
        self.json = dict(
            tags=[model_name],
            summary="",
            description="",
            consumes=[],
            produces=[],
            parameters=[],
            responses={}
        )


class OperationContentTypes(object):
    def __init__(self):
        self.json = "application/json"
        self.xml = "application/xml"


# TODO: Update this for other "in"s (e.g. Form Inputs)
class OperationParameters(object):
    def __init__(self):
        self.json = {
            'in': "body",
            'name': "body",
            'description': "",
            'required': True,
            'schema': {
                "$ref": "#/"
            }
        }

    def update(self, desc="", required=True, definition="#/"):
        self.json['description'] = desc
        self.json['required'] = required
        self.json['schema']['$ref'] = definition

        return self.json


class OperationResponses(object):
    def __init__(self, schema=None):
        # http://www.restapitutorial.com/httpstatuscodes.html - Using the Top 10 Response Codes*
        self.codes = {
            "200": "OK",
            "201": "Created",
            "204": "No Content",
            "304": "Not Modified",
            "400": "Bad Request",
            "401": "Unauthorized",
            "403": "Forbidden",
            "404": "Not Found",
            "409": "Conflict",
            "500": "Internal Server Error"
        }
        schema = {
            '$ref': '#/definitions/'
        }
        self.json = dict(
            schema=schema
        )


class TagJSON(object):
    def __init__(self, model_name, description):
        self.json = dict(
            name=model_name,
            description=description
        )
