from api.exceptions import OmdbApiResponseException
from api.externalapihandler.external_api_handler import ExternalApiHandler


class OmdbApiHandler(ExternalApiHandler):

    def __init__(self, api_key):
        self.base_url = 'http://www.omdbapi.com/'
        self.poster_url = 'http://img.omdbapi.com/'
        super().__init__(api_key)

    def get_movie(self, title):
        parameters = {'apikey': self.api_key, 't': title}
        result = self._get(self.base_url, parameters)
        if result.get('Error'):
            raise OmdbApiResponseException('Error encountered when getting movie from OMDb'.format(result.get('Error')))
        return result
