import os

os.system("title Distribute Requests")
from flask import Flask, jsonify, request
import json
from lxml import etree
from io import StringIO
from concurrent.futures import ThreadPoolExecutor
import requests
from insert_influx import Influxdb
influx = Influxdb()

app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=10000)
# executor = ThreadPoolExecutor(max_workers=1)
# # response = requests.get('https://www.eghamat24.com/property-rooms/list-view', params=params, cookies=cookies, headers=headers)
class ExeRequest:
    def __init__(self, method, url, params=None, cookies=None, headers=None, data=None, json=None):
        self.url = url
        self.params = params
        self.cookies = cookies
        self.headers = headers
        self.method = method.lower()  # Convert to lowercase for consistency
        self.data = data
        self.json = json

    def execute(self):
        if self.method == "get":
            response = requests.get(self.url, params=self.params, cookies=self.cookies, headers=self.headers,
                                    data=self.data, json=self.json)
        elif self.method == "post":
            response = requests.post(self.url, params=self.params, cookies=self.cookies, headers=self.headers,
                                     data=self.data, json=self.json)
        else:
            raise ValueError(f"Unsupported HTTP method: {self.method}")

        return response  # Return the response object


@app.route('/remoteRequest', methods=['GET'])
def remoteRequest():
    url = request.args.get('url','')
    params = json.loads(request.args.get('params', '{}'))  # Parse params as JSON
    cookies = json.loads(request.args.get('cookies', '{}'))  # Parse cookies as JSON
    headers = json.loads(request.args.get('headers', '{}'))  # Parse headers as JSON
    method = request.args.get('method','GET')       # Convert to lowercase for consistency
    data = json.loads(request.args.get('data', '{}')) if method == "post" else None  # Parse data if POST
    json_data = json.loads(request.args.get('json', '{}')) if method == "post" else None  # Parse json if POST

    print(f'Get address == ')
    exeRequest = ExeRequest(method, url, params, cookies, headers, data, json_data)
    future = executor.submit(exeRequest.execute,)
    result = future.result()
    print(f'Send result == ')
    # Optionally, you can return a response immediately
    # return jsonify(result)

    # Extract the status code, text, and cookies
    status_code = result.status_code
    text = result.text
    cookies = result.cookies.get_dict()  # Convert cookies to a dictionary for easy access


    # Return the information as JSON
    return jsonify({
        'status_code': status_code,
        'text': text,
        'cookies': cookies
    })
    # return result

import sys
if __name__ == '__main__':
    port=int(sys.argv[1]) # Get port from command line
    # app.run(debug=True,host='0.0.0.0',port=6000)
    app.run(host='0.0.0.0',port=port)
