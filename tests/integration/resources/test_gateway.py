from ..integration import ResourceTestCase

from agilepay.resources.gateway import Gateway


class GatewayTest(ResourceTestCase):

    def setUp(self):
        """
        :type gateway: agilepay.resources.gateway.Gateway
        :return:
        """
        super(GatewayTest, self).setUp()
        self.gateway = Gateway(self.client)

    def test_get(self):
        reference = self.create_dummy_gateway().get_body()['reference']
        get = self.gateway.set_reference(reference).get()
        self.assertEqual(get.get_status_code(), 200)
        self.assertEqual(get.get_body()['reference'], reference)

    def test_get_list(self):
        list = self.gateway.get_list()
        self.assertEqual(list.get_response().get_status_code(), 200)

    def test_create(self):
        created = self.create_dummy_gateway()
        self.assertEqual(created.get_status_code(), 200)
        self.assertTrue('reference' in created.get_body())

    def test_update(self):
        reference = self.create_dummy_gateway().get_body()['reference']
        updated = self.gateway.set_reference(reference).update({
            'fields': {
                'dummy_key': 'dummy'
            }
        })
        self.assertEqual(updated.get_status_code(), 200)