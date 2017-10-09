from ..helpers import dicts_merge


class AdHoc:

    def __init__(self, client, reference):
        """
        Initialize the schedule type ad hoc resource

        :param client:
        :type client: agilepay.client.Client
        :param reference
        :type reference: str
        """
        self._client = client
        self._reference = reference

    def create(self, fields={}):
        """
        Create a new schedule type of ad hoc

        :param fields:
        :type fields: dict
        :return: agilepay.responses.Response
        """
        return self._client.post('schedules', {
            'body': dicts_merge(fields, {
                'type': 'ad_hoc'
            })
        })

class Schedule:

    def __init__(self, client, reference=None):
        """
        Initialize the schedule resource

        :param client:
        :type client: agilepay.client.Client
        :param reference
        :type reference str
        """
        self._client = client
        self._reference = reference

    def ad_hoc(self):
        """
        Access the ad hoc schedule type resource

        :return:
        :rtype: agilepay.resources.schedule.AdHoc
        """
        return AdHoc(self._client, self._reference)