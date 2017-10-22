from ..integration import ResourceTestCase

from agilepay.resources.customer import Customer


class CustomerTest(ResourceTestCase):

    def setUp(self):
        """
        :type customer: agilepay.resources.customer.Customer
        :return:
        """
        super(CustomerTest, self).setUp()
        self.customer = Customer(self.client)

    def test_get(self):
        reference = self.create_dummy_customer().get_body()['reference']
        get = self.customer.set_reference(reference).get()
        self.assertEqual(get.get_status_code(), 200)
        self.assertEqual(get.get_body()['reference'], reference)

    def test_get_list(self):
        list = self.customer.get_list()
        self.assertEqual(list.get_response().get_status_code(), 200)

    def test_create(self):
        created = self.create_dummy_customer()
        self.assertEqual(created.get_status_code(), 200)
        self.assertTrue('reference' in created.get_body())

    def test_update(self):
        reference = self.create_dummy_customer().get_body()['reference']
        new_email = 'updatedemail@test.com'
        updated = self.customer.set_reference(reference).update({
            'email': new_email
        })
        self.assertEqual(updated.get_status_code(), 200)
        self.assertEqual(new_email, updated.get_body()['email'])