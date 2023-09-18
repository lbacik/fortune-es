import requests


class FortuneClient:

    def __init__(self, url: str) -> None:
        self.url: str = url

    def request(self, item: str|None = None) -> list:
        response: requests.Response
        if item is None:
            response = requests.get(f"{self.url}?explore=1")
        else:
            response = requests.get(f"{self.url}/{item}?explore=1")
        return response.json()

