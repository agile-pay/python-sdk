from ..integration import ResourceTestCase

from agilepay.resources import Transaction


class TransactionTest(ResourceTestCase):

    def setUp(self):
        """
        :type transaction: agilepay.resources.Transaction
        :return:
        """
        super(TransactionTest, self).setUp()
        self.transaction = Transaction(self.client)
        self.transaction.set_gateway(self.create_dummy_gateway().get_body()['reference'])
        self.transaction.set_payment_method(self.create_dummy_payment_method_card().get_body()['token'])

    def test_get_list(self):
        list = self.transaction.get_list()
        self.assertEqual(list.get_response().get_status_code(), 200)
        # testing retrieving by pages as well
        list = self.transaction.get_list({'page': 2})
        self.assertEqual(list.get_response().get_status_code(), 200)
        self.assertEqual(list.current_page(), 2)

    def test_get(self):
        reference = self.transaction.auth(500, 'EUR').get_body()['reference']
        get = Transaction(self.client, reference).get()
        self.assertEqual(get.get_body()['reference'], reference)

    def test_auth(self):
        created = self.transaction.auth(500, 'EUR')
        self.assertEqual(created.get_status_code(), 200)
        self.assertTrue('reference' in created.get_body())

    def test_void(self):
        reference = self.transaction.auth(500, 'EUR').get_body()['reference']
        created = Transaction(self.client, reference).void()
        self.assertEqual(created.get_status_code(), 200)
        self.assertEqual(created.get_body()['type'], 'void')
        self.assertTrue('reference' in created.get_body())
        self.assertTrue('parent_reference' in created.get_body())

    def test_capture(self):
        reference = self.transaction.auth(500, 'EUR').get_body()['reference']
        created = Transaction(self.client, reference).capture()
        self.assertEqual(created.get_status_code(), 200)
        self.assertEqual(created.get_body()['type'], 'capture')
        self.assertTrue('reference' in created.get_body())
        self.assertTrue('parent_reference' in created.get_body())
        # testing by providing a different amount and currency
        reference = self.transaction.auth(500, 'EUR').get_body()['reference']
        created = Transaction(self.client, reference).capture(100, 'GBP')
        self.assertEqual(created.get_status_code(), 200)
        self.assertEqual(created.get_body()['type'], 'capture')
        self.assertTrue('reference' in created.get_body())
        self.assertTrue('parent_reference' in created.get_body())
        self.assertEqual(created.get_body()['details']['amount'], '100')
        self.assertEqual(created.get_body()['details']['currency_code'], 'GBP')

    def test_credit(self):
        reference = self.transaction.auth(500, 'EUR').get_body()['reference']
        Transaction(self.client, reference).capture().get_body()['reference']
        created = Transaction(self.client, reference).credit()
        self.assertEqual(created.get_status_code(), 200)
        self.assertEqual(created.get_body()['type'], 'credit')
        self.assertTrue('reference' in created.get_body())
        self.assertTrue('parent_reference' in created.get_body())
        # testing by providing a different amount and currency
        reference = self.transaction.auth(500, 'EUR').get_body()['reference']
        Transaction(self.client, reference).capture().get_body()['reference']
        created = Transaction(self.client, reference).credit(100, 'GBP')
        self.assertEqual(created.get_status_code(), 200)
        self.assertEqual(created.get_body()['type'], 'credit')
        self.assertTrue('reference' in created.get_body())
        self.assertTrue('parent_reference' in created.get_body())
        self.assertEqual(created.get_body()['details']['amount'], '100')
        self.assertEqual(created.get_body()['details']['currency_code'], 'GBP')

