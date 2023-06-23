from typing import List, Dict
from octokit import Octokit
from typing import List, Dict

from octokit import Octokit


class APIManager:
    @staticmethod
    def api_call(api_interface, url: str, req_options: Dict[str, str], url_options: Dict[str, str]) -> List[Dict[str, str]]:
        keyword = "github.com" if isinstance(api_interface, Octokit) else "api.clockify.me/api/v1"
        method = "POST" if url_options.get("report") else "GET"
        full_url = APIManager.construct_url(keyword, url, url_options)
        response = requests.request(method, full_url, headers=req_options.get("headers"))
        data = response.json()
        return data

    @staticmethod
    def construct_url(keyword: str, url: str, options: Dict[str, str]) -> str:
        initial_index = url.rfind(keyword) + len(keyword)
        final_index = url.rfind("{") if "{" in url else None
        basic_url = url[initial_index: final_index]
        return f"{options.get('front_path')}{basic_url}{options.get('back_path')}"