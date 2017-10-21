from ..responses import PaginatedResponse


class Gateway:

    def __init__(self, client, reference=None):
        """
        Initialize the Gateway resource

        :param client:
        :param reference:
        """
        self._client = client
        self._reference = reference

    def set_reference(self, reference):
        """
        Set the gateway reference

        :param reference:
        :type reference: str
        :return: self
        """
        self._reference = reference
        return self

    def get(self):
        """
        Get a gateway

        :return: Response
        :rtype: agilepay.responses.Response
        """
        return self._client.get('gateways/%s' % self._reference)

    def get_list(self, options={}):
        """
       Get the list of gateways owned by the user

       :param options:
       :return:PaginatedResponse
       """
        response = self._client.get('gateways', {
            'query': options
        })

        return PaginatedResponse(self._client, response)

    def create(self, type, fields={}):
        """
        Create a new gateway

        visit http://docs.agilepay.io/#!/gateway

        :param type: the gateway type
        :param fields:
        :return: the response
        :rtype: agilepay.responses.Response
        """
        return self._client.post('gateways', {
            'body': {
                'type': type,
                'fields': fields
            }
        })

    def update(self, body={}):
        """
        Update an existing gateway

        visit http://docs.agilepay.io/#!/gateway-update

        Example:

        >>> update({
        ...    'fields': {
        ...        'key': 'new-value'
        ...    }
        ... })

        :param body:
        :return: Response
        """
        return self._client.put('gateways/%s' % self._reference, {
            'body': body
        })
