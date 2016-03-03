import json


def parse_inputs(request):
    # Ensure a request body was POSTed
    if request is not None:
        if type(request) is str:
            request = json.loads(request)
    else:
        raise TypeError

    # Ensure the request body has an 'inputs' key in the JSON
    try:
        inputs = request['inputs']
    except TypeError, e:
        return e

    return inputs
