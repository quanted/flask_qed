import json


def parse_inputs(request):
    # Ensure a request body was POSTed
    if request is not None:
        try:
            request = json.loads(request)
        except TypeError:
            if type(request) is dict:
                pass
            else:
                return None
    else:
        raise TypeError

    # Ensure the request body has an 'inputs' key in the JSON
    try:
        inputs = request['inputs']
    except TypeError:
        return None

    return inputs
