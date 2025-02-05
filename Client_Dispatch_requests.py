import requests
import itertools

# Define servers and ports
servers = [
    # ("45.149.76.168", [6000]),
    ("45.149.76.168", [6000, 6001, 6002,6003,6004,6005]),
    ("130.185.77.24", [6000, 6001, 6002,6003,6004,6005]),
    # ("185.252.31.31", [6000, 6001, 6002,6003,6004,6005])
]

# servers = [
#     ("45.149.76.168", [6000]),
#     # ("130.185.77.24", [6000, 6001, 6002])
# ]

# Create an iterator for round-robin selection
server_iterator = itertools.cycle([(server, port) for server, ports in servers for port in ports])


import json
# req = requests.post('https://www.booking.ir/fa/v2/signinbymobile/', headers=headers, data=data)
def executeRequest(method, url, params=None, cookies=None, headers=None, data=None, json_data=None):
    # Select the next server and port in a round-robin fashion
    server, port = next(server_iterator)
    full_url = f"http://{server}:{port}/remoteRequest"

    serverparams = {
        'url': url,
        'params': json.dumps(params) if params is not None else '{}',  # Ensure it's a JSON object
        'cookies': json.dumps(cookies) if cookies is not None else '{}',
        'headers': json.dumps(headers) if headers is not None else '{}',
        'method': method,
        'data': json.dumps(data) if data is not None else '{}',
        'json': json.dumps(json_data) if json_data is not None else '{}',
    }


    # round robin for server 45.149.76.168 with ports [6000,6001,6002] and server 130.185.77.24 with ports [6000,6001,6002]
    response = requests.get(full_url, params=serverparams)

    return response # Return the response object


