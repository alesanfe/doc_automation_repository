from dataclasses import dataclass

import requests
import json

@dataclass
class Clockipy:
    """This object represents the Clockify API as a Python object"""
    token: str
    base_url: str = "https://api.clockify.me/api/v1"

    def __post_init__(self):
        self.headers = {"X-Api-Key": self.token}


    def request(self, url, options):
        method, path = url.split(" ")

        for key, value in options.items():
            path = path.replace("{" + key + "}", value) if isinstance(value, str) else path

        url = "%s%s" % (options.get("base_url") or self.base_url, path)
        headers = {**self.headers, **(options.get("headers") or {})}
        json_data = options.get("body")
        params = options.get("query")

        result = requests.request(method, url, headers=headers, json=json_data, params=params)

        try:
            response = json.loads(result.text)
        except ValueError:
            return result.text

        return response
