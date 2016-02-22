import re
from collections import defaultdict
from REST_UBER.swagger_ui import ApiSpec
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
        "definitions": defaultdict(dict),
        "tags": []
    }
    paths = output['paths']
    definitions = output['definitions']
    tags = output['tags']

    # TODO: Are these needed (from 'flask_swagger')
    ignore_verbs = {"HEAD", "OPTIONS"}
    # technically only responses is non-optional
    optional_fields = ['tags', 'consumes', 'produces', 'schemes', 'security',
                       'deprecated', 'operationId', 'externalDocs']

    # Loop over the Flask-RESTful endpoints being served (called "rules"...e.g. /terrplant/)
    for rule in app.url_map.iter_rules():
        endpoint = app.view_functions[rule.endpoint]
        try:
            class_name = endpoint.view_class()
        except AttributeError:
            continue  # skip to next iteration in for-loop ("rule" does not contain an ubertool REST endpoint)
        try:
            inputs = class_name.get_model_inputs().__dict__
            outputs = class_name.get_model_outputs().__dict__
        except AttributeError:
            # This endpoint does not have get_model_inputs() or get_model_outputs()
            logging.exception(AttributeError.message)
            continue  # skip to next iteration, as this is not an ubertool endpoint

        # TODO: Logic for UBERTOOL API ENDPOINTS - Move to separate function for code clarity???
        methods = {}
        for verb in rule.methods.difference(ignore_verbs):
            if hasattr(endpoint, 'methods') and verb in endpoint.methods:
                verb = verb.lower()
                methods[verb] = endpoint.view_class.__dict__.get(verb)
            else:
                methods[verb.lower()] = endpoint
        for verb, method in methods.items():
            pass
            # TODO: Needed when multiple METHODS are used (e.g. POST and GET)
            # 'path' JSON is created here for each method in the endpoint (e.g. GET, POST)

        # This has to be at the end of the for-loop because it converts the 'rule' object to a string
        # Rule = endpoint URL relative to hostname; needs to have special characters escaped to be defaultdict key
        rule = str(rule)
        for arg in re.findall('(<(.*?\:)?(.*?)>)', rule):
            rule = rule.replace(arg[0], '{%s}' % arg[2])

        # Get model name
        model_name = class_name.name
        # Instantiate ApiSpec() class for current endpoint
        api_spec = ApiSpec(model_name)

        # Append the 'tag' (top-level) JSON for each rule/endpoint
        tag = api_spec.tag.json
        tags.append(tag)

        # Paths
        path = api_spec.path.path_item
        paths[rule].update(path)

        # TODO: Definitions JSON; move to separate class
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

        model_def = {
            model_name.capitalize() + "Inputs": definition_template_inputs,
            model_name.capitalize() + "Outputs": definition_template_outputs
        }
        for k, v in inputs.items():
            # Set the inputs to the input and output definition template
            model_def[model_name.capitalize() + "Inputs"]['properties']['inputs']['properties'][k] = \
                model_def[model_name.capitalize() + "Outputs"]['properties']['inputs']['properties'][k] = {
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
            model_def[model_name.capitalize() + "Outputs"]['properties']['outputs']['properties'][k] = {
                "type": "object",
                "properties": {
                    "0": {
                        "type": 'string' if str(v.dtype) == 'object' else 'number',
                        "format": 'string' if str(v.dtype) == 'object' else 'float'
                    }
                }
            }

        definitions.update(model_def)


        operations = {}
        # for verb, method in methods.items():
        #     """This is where the object parsing (introspection) occurs to generate the Swagger JSON"""
        #     print verb, method
        #     str(class_name)W

    return output
