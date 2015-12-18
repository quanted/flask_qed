from collections import defaultdict


def swagger(app):

    output = {
            "swagger": "2.0",
            "info": {
                "version": "0.0.0",
                "title": "Cool product name",
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

    # Loop over the Flask-RESTful endpoints being served
    for rule in app.url_map.iter_rules():
        # TODO: Remove print statement
        print "Endpoint: %s" % str(rule)
        endpoint = app.view_functions[rule.endpoint]
        # class_name = endpoint.view_class
        try:
            class_name = endpoint.view_class()
            # model_obj = getattr(class_name)
        except AttributeError:
            continue  # skip to next iteration in for-loop ("rule" does not contain an ubertool REST endpoint)
        print "I'm an Endpoint: %s, %s: %s" % (str(class_name), type(class_name), class_name.__dict__)
        try:
            test = class_name.get_model_inputs()
        except AttributeError:
            pass
        methods = dict()
        for verb in rule.methods.difference(ignore_verbs):
            if hasattr(endpoint, 'methods') and verb in endpoint.methods:
                verb = verb.lower()
                methods[verb] = endpoint.view_class.__dict__.get(verb)
            else:
                methods[verb.lower()] = endpoint
        operations = dict()
        for verb, method in methods.items():
            """This is where the object parsing (introspection) occurs to generate the Swagger JSON"""
            print verb, method

    return output


