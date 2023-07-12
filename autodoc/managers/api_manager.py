from typing import List, Dict

import requests as requests
from github import Github


class APIManager:
    @staticmethod
    def api_call(url: str) -> List[Dict[str, str]]:
        print(url)
        response = requests.request("GET", url)
        data = response.json()
        print(data)
        return data