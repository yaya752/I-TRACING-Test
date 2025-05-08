import requests

class BaseClient:
    def __init__(self, base_url: str, headers: dict = {}):
        self.base_url = base_url
        self.headers = headers

    def http_request(self, method: str, endpoint: str, params: dict = {}, headers: dict = {}, verify_ssl: bool = True):
        url = f"{self.base_url}{endpoint}"
        combined_headers = {**self.headers, **headers}

        response = requests.request(method, url, params=params, headers=combined_headers, verify=verify_ssl)
        response.raise_for_status()
        return response.json()