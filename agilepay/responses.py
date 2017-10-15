try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

from .errors import PaginatedResponseError
from .helpers import is_json, json_to_dict


class Response:

    def __init__(self, response):
        self._response = response

    def get_body(self):
        if is_json(self._response.text):
            return json_to_dict(self._response.text)
        return self._response.text

    def get_status_code(self):
        return self._response.status_code


class PaginatedResponse:

    def __init__(self, client, response):
        """
        Initialize the paginated response

        :param client:
        :type client: agilepay.client.Client
        :param response:
        :type response: agilepay.responses.Response
        """
        self._client = client
        self._response = response

    def get_response(self):
        """
        Get the raw response object
        :return:
        :rtype : agilepay.responses.Response
        """
        return self._response

    def get_data(self):
        """
        Get the paginated response data excluding pagination information

        :return:
        """
        return self._response.get_body()['data']

    def total_items(self):
        """
        Get the total number of items

        :return: int
        """
        return int(self._response.get_body()['total'])

    def current_page(self):
        """
        Retrieve the current page

        :return: int
        """
        return int(self._response.get_body()['current_page'])

    def is_last_page(self):
        """
        Whether the current page is the last page

        :return: bool
        """
        return self.current_page() == self.total_pages()

    def total_pages(self):
        """
        Get the total number of pages

        :return: int
        """
        return int(self._response.get_body()['last_page'])

    def next_page(self):
        """
        Fetch the next page data

        :return: self
        """
        if self.current_page() < self.total_pages() and 'next_page_url' in self._response.get_body():
            url = self._response.get_body()['next_page_url']
            if len(url) > 0:
                self._response = self._client.get(self._extrapolate_uri(url))
                return self
        else:
            raise PaginatedResponseError('You can\'t go forward any further')

    def previous_page(self):
        """
        Fetch the previous page data

        :return: self
        """
        if self.current_page() > 1 and 'prev_page_url' in self._response.get_body():
            url = self._response.get_body()['prev_page_url']
            if len(url) > 0:
                self._response = self._client.get(self._extrapolate_uri(url))
                return self
        else:
            raise PaginatedResponseError('You can\'t get back any further')

    def _extrapolate_uri(self, url):
        parsed = urlparse(url)
        # exclude api version from path [4:]
        uri, query = parsed.path[4:], parsed.query
        return "%s?%s" % (uri, query) if len(query) > 0 else uri

    def __iter__(self):
        for item in self.get_data():
            yield item
