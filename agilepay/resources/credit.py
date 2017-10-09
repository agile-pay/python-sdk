class Credit:

    def __init__(self, client):
        """
        Initialize the credit resource

        :param client:
        :type client agilepay.client.Client
        """
        self._client = client

    def get(self):
        """
        Get the credit information

        :return:
        :rtype: agilepay.responses.Response
        """
        return self._client.get('credit')

    def top_up(self, amount, card, billing=None):
        """
        Top up the user credit

        :param amount: the amount to top up, 20 = pounds 20.00
        :type amount: int
        :param card: the card reference or a new card
        :type card: str
        :type card: dict
        :param billing:
        :type billing: dict
        :return:
        :rtype: agilepay.responses.Response
        """
        return self._client.put('credit', {
            'body': {
                'amount': amount,
                'billing': billing,
                'payment_method' if type(card) == 'str' else 'card': card
            }
        })
