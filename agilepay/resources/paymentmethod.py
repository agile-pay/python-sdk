from ..responses import PaginatedResponse


class PaymentMethod:

    def __init__(self, client, token=None):
        """
        Initialize the payment method resource

        visit http://docs.agilepay.io/#!/payment-method

        :param client:
        :param token:string
        """
        self._token = token
        self._client = client
        self._options = {
            'keep': False
        }

    def keep(self, val=True):
        """
        Retain the payment method in agilepay

        :param val:
        :return: self
        """
        self._options['keep'] = val
        return self

    def get(self):
        """
        Get a payment method

        :return: Response
        """
        return self._client.get('payment-method/%s' % self._token)

    def get_list(self, options={}):
        """
        Get the list of payment methods owned by the user

        :param options:
        :return:PaginatedResponse
        """
        response = self._client.get('payment-methods', {
            'query': options
        })

        return PaginatedResponse(self._client, response)

    def create_card(self, data={}):
        """
        Create a new payment method type of card

        visit http://docs.agilepay.io/#!/payment-method-create-card

        :param data:
        :return: Response
        """
        return self._client.post('payment-methods', {
            'body': {
                'type': 'card',
                'details': data,
                'options': self._options
            }
        })

    def create_gateway_token(self, gateway, card={}):
        """
        Create a new payment method type of gateway_token

        visit http://docs.agilepay.io/#!/payment-method-create-gateway-token

        :param gateway:
        :param card:
        :return:
        :rtype: agilepay.responses.Response
        """
        details = {'gateway': gateway}
        if len(card) > 0:
            details['card'] = card
        else:
            details['payment_method'] = self._token

        return self._client.post('payment-methods', {
            'body': {
                'type': 'gateway_token',
                'details': details,
                'options': self._options
            }
        })
