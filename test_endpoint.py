from flask import Flask, request

import json
import werkzeug

app = Flask(__name__)

methods = [
    "POST",
    "PUT",
    "GET",
    "DELETE",
    "PATCH",
    "OPTIONS"
]


def stringificate(obj, item):
    """Stringify objects recursively based on type."""
    if type(item) in [dict, werkzeug.datastructures.ImmutableMultiDict]:
        return stringificate_dict(obj, item)
    elif type(item) == list:
        return stringificate_list(obj, item)
    else:
        return str(item)


def stringificate_dict(obj, dictionary):
    """Stringify Dicts Recursively."""
    resp = {}
    for k, v in dictionary.items():
        resp[k] = stringificate(obj, v)
    return resp


def stringificate_list(obj, thelist):
    """Stringify Lists Recursively."""
    resp = []
    for i, x in enumerate(thelist):
        resp[i] = stringificate(obj, x)
    return resp


@app.route('/', defaults={'path': ''}, methods=methods)
@app.route('/<path:path>', methods=methods)
def test_endpoint(path):
    """Return Dict of the request sent."""
    dir_dict = {}
    for x in dir(request):
        print(x)
        obj_type = type(request.__getattr__(x))
        str_obj = stringificate(request, request.__getattr__(x))
        dir_dict[x] = [
            str(obj_type),
            str_obj
        ]
    resp = {
        "dir(request)": dir_dict,
        "request.get_json()": request.get_json(),
        "request.get_data()": request.get_data(),
        "path": path,
    }
    return json.dumps(resp, indent=4)

if __name__ == "__main__":
    app.run(debug=True)
