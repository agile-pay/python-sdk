from ..responses import PaginatedResponse


class Customer:

    def __init__(self, client, reference=None):
        """
        Initialize the Customer resource

        :param client:
        :param reference:
        """
        self._client = client
        self._reference = reference

    def set_reference(self, reference):
        """
        Set the customer reference

        :param reference:
        :type reference: str
        :return: self
        """
        self._reference = reference
        return self

    def get(self):
        """
        Get a customer

        :return: Response
        :rtype: agilepay.responses.Response
        """
        return self._client.get('customers/%s' % self._reference)

    def get_list(self, options={}):
        """
       Get the list of customers owned by the user

       :param options:
       :return:PaginatedResponse
       """
        response = self._client.get('customers', {
            'query': options
        })

        return PaginatedResponse(self._client, response)

    def create(self, customer={}):
        """
        Create a new customer

        visit http://docs.agilepay.io/#!/customer

        :param customer: the customer data
        :type customer: dict
        :return: the response
        :rtype: agilepay.responses.Response
        """
        return self._client.post('customers', {
            'body': customer
        })

    def update(self, customer={}):
        """
        Update an existing customer

        visit http://docs.agilepay.io/#!/customer-update

        :param customer:
        :return: Response
        :rtype: agilepay.responses.Response
        """
        return self._client.put('customers/%s' % self._reference, {
            'body': customer
        })

    def attach_payment_method(self, payment_method):
        """
        Attach a payment method to a customer

        :param payment_method:
        :return: the response
        :rtype: agilepay.responses.Response
        """
        return self._client.put('customers/%s/payment-methods/%s' % (self._reference, payment_method))
