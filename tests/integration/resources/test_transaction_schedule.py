import datetime

from ..integration import ResourceTestCase

from agilepay.resources import TransactionSchedule


class TransactionScheduleTest(ResourceTestCase):

    def setUp(self):
        """
        :type transaction_schedule: agilepay.resources.TransactionSchedule
        :return:
        """
        super(TransactionScheduleTest, self).setUp()
        self.transaction_schedule = TransactionSchedule(self.client)
        self.transaction_schedule.set_payment_method(self.create_dummy_payment_method_gateway_token().get_body()['token'])

    def test_schedule_auth(self):
        created = self._schedule_auth()
        self.assertTrue('reference' in created.get_body())
        self.assertTrue('retries' in created.get_body())

    def test_delete(self):
        scheduled = self._schedule_auth().get_body()['reference']
        deleted = TransactionSchedule(self.client, scheduled).delete()
        self.assertEqual(deleted.get_status_code(), 204)

    def _schedule_auth(self):
        at = datetime.datetime.now() + datetime.timedelta(days=15)
        type = 'auth'
        timezone = 'Europe/Rome'

        return self.transaction_schedule.schedule(
            type,
            at.strftime('%Y-%m-%d %H:%M:%S'),
            timezone,
            data={'amount': 500, 'currency_code': 'GBP'},
            retries=[
                (at + datetime.timedelta(days=5)).strftime('%Y-%m-%d %H:%M:%S'),
                (at + datetime.timedelta(days=10)).strftime('%Y-%m-%d %H:%M:%S'),
                (at + datetime.timedelta(days=15)).strftime('%Y-%m-%d %H:%M:%S'),
            ]
        )
