import requests


class ExternalApiHandler:

    def __init__(self, api_key):
        self.api_key = api_key

    @staticmethod
    def _get(uri, parameters=None):
        response = requests.get(uri, params=parameters)
        response.raise_for_status()
        return response.json()

    # TODO: Implement other request types to external API
