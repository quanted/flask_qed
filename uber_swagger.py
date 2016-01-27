import re
from collections import defaultdict

import logging


def swagger(app):
    output = {
        "swagger": "2.0",
        "info": {
            "title": u"\u00FCbertool API Documentation",
            "description": "Welcome to the EPA's ubertool interactive RESTful API documentation.",
            # "termsOfService": "",
            "contact": {
                "name": u"\u00FCbertool Development Team",
                # "url": "",
                "email": "ubertool-dev@googlegroups.com",
            },
            # "license": {
            #     "name": "",
            #     "url": ""
            # },
            "version": "0.0.1"
        },
        "paths": defaultdict(dict),
        "definitions": defaultdict(dict)
    }

    paths = output['paths']
    definitions = output['definitions']
    ignore_verbs = {"HEAD", "OPTIONS"}
    # technically only responses is non-optional
    optional_fields = ['tags', 'consumes', 'produces', 'schemes', 'security',
                       'deprecated', 'operationId', 'externalDocs']

    # Loop over the Flask-RESTful endpoints being served (called "rules"...e.g. /terrplant/)
    for rule in app.url_map.iter_rules():
        # TODO: Remove print statement
        print "Endpoint: %s" % str(rule)
        endpoint = app.view_functions[rule.endpoint]
        try:
            class_name = endpoint.view_class()
            # model_obj = getattr(class_name)
        except AttributeError:
            continue  # skip to next iteration in for-loop ("rule" does not contain an ubertool REST endpoint)
        print "I'm an Endpoint: %s, %s: %s" % (str(class_name), type(class_name), class_name.__dict__)
        try:
            inputs = class_name.get_model_inputs().__dict__
            outputs = class_name.get_model_outputs().__dict__
        except AttributeError:
            # This endpoint does not have get_model_inputs()
            logging.exception(AttributeError.message)
            continue  # skip to next iteration

        # Rule = endpoint URL relative to hostname; needs to have special characters escaped to be defaultdict key
        rule = str(rule)
        for arg in re.findall('(<(.*?\:)?(.*?)>)', rule):
            rule = rule.replace(arg[0], '{%s}' % arg[2])

        # TODO: Make generic...
        path_json = {
            "post": {
                "tags": ["Terrplant"],
                "summary": "Testing this Swagger stuff out",
                "description": "Tasty Endpoints",
                "operationId": "terrplant",
                "consumes": [
                    "application/json",
                ],
                "produces": [
                    "application/json"
                ],
                "parameters": [
                    {
                        "in": "body",
                        "name": "body",
                        "description": "Pet object that needs to be added to the store",
                        "required": True,
                        "schema": {
                            "$ref": "#/definitions/TerrplantInputs"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "successful operation",
                        "schema": {
                            "$ref": "#/definitions/TerrplantOutputs"
                        }
                    },
                    "405": {
                        "description": "Invalid input"
                    }
                }
            }
        }
        paths[rule].update(path_json)

        # TODO: Definitions JSON
        definition_template_inputs = {
            'type': "object",
            'properties': {
                'inputs': {
                    "type": "object",
                    "properties": {}
                },
                'run_type': {
                    "type": 'string',
                    "example": "single"
                }
            }
        }

        definition_template_outputs = {
            'type': "object",
            'properties': {
                'user_id': {
                    'type': 'string',
                },
                'inputs': {
                    # inputs_json
                    'type': 'object',
                    'properties': {}
                },
                'outputs': {
                    # outputs_json
                    'type': 'object',
                    'properties': {}
                },
                'exp_out': {
                    # exp_out_json
                    'type': 'object',
                    'properties': {}
                },
                '_id': {
                    'type': 'string',
                },
                'run_type': {
                    'type': 'string',
                }
            }
        }

        terrplant_def = {
            'TerrplantInputs': definition_template_inputs,
            'TerrplantOutputs': definition_template_outputs
        }
        for k, v in inputs.items():
            # Set the inputs to the input and output definition template
            terrplant_def['TerrplantInputs']['properties']['inputs']['properties'][k] = \
                terrplant_def['TerrplantOutputs']['properties']['inputs']['properties'][k] = {
                    "type": "object",
                    "properties": {
                        "0": {
                            # 'type' is JSON data type (e.g. 'number' is a float; 'string' is a string or binary)
                            "type": 'string' if str(v.dtype) == 'object' else 'number',
                            # 'format' is an optional modifier for primitives
                            "format": 'string' if str(v.dtype) == 'object' else 'float'
                        }
                    }
            }

        for k, v in outputs.items():
            # Set the outputs to the output definition template
            terrplant_def['TerrplantOutputs']['properties']['outputs']['properties'][k] = {
                "type": "object",
                "properties": {
                    "0": {
                        "type": 'string' if str(v.dtype) == 'object' else 'number',
                        "format": 'string' if str(v.dtype) == 'object' else 'float'
                    }
                }
            }

        definitions.update(terrplant_def)

        methods = {}
        # for verb in rule.methods.difference(ignore_verbs):
        #     if hasattr(endpoint, 'methods') and verb in endpoint.methods:
        #         verb = verb.lower()
        #         methods[verb] = endpoint.view_class.__dict__.get(verb)
        #     else:
        #         methods[verb.lower()] = endpoint
        operations = {}
        # for verb, method in methods.items():
        #     """This is where the object parsing (introspection) occurs to generate the Swagger JSON"""
        #     print verb, method
        #     str(class_name)W

    return output
