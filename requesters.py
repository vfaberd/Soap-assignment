import requests


class AgregatorRequester():
    def __init__(self, request_body):
        self.url = ''
        self.headers = {
            'host': '',
            'Content-Type': 'application/soap+xml; charset=utf-8'
        }
        self.request_body = request_body

    def send_request(self):
        response = requests.post(
            self.url, data=self.request_body, headers=self.headers)
        return response
