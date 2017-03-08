from collections import OrderedDict
import json
from hashlib import sha256
import hmac
import requests


class Worthers(object):
    BASE_URL = 'https://cmsapi.cofeportal.org'
    DATE_FORMAT = '%Y-%m-%d %H:%M'

    def __init__(self, api_id, api_key, diocese_id=None):
        self._diocese_id = None

        self.api_id = api_id
        self.api_key = api_key

        if diocese_id:
            self.diocese_id = diocese_id

        self.session = None

    @property
    def diocese_id(self):
        if not self._diocese_id:
            raise NotImplementedError(
                'Must set diocese_id or specify the diocese_id when calling methods'
            )
        return self._diocese_id

    @diocese_id.setter
    def diocese_id(self, value):
        self._diocese_id = value

    def get_contacts(
        self, diocese_id=None, end_date=None, fields=None, limit=None, offset=None, start_date=None
    ):
        """
        https://cmsapi.cofeportal.org/get-contacts
        """
        endpoint_url = self.generate_endpoint_url('/v2/contacts')

        data = self._generate_default_data(diocese_id=diocese_id)

        request_params = self.generate_request_params(
            data, end_date=end_date, fields=fields, limit=limit, offset=offset,
            start_date=start_date,
        )

        result = self.do_request(endpoint_url, request_params)
        return result

    def _generate_default_data(self, diocese_id=None):
        data = OrderedDict()
        data['diocese_id'] = diocese_id or self.diocese_id
        return data

    def do_request(self, endpoint_url, request_params):
        session = self.get_session()
        return self._get_as_json(session, endpoint_url, request_params)

    def _get_as_json(self, session, endpoint_url, request_params):
        """
        Use the supplied session to run a get request and return the decoded JSON data.
        """
        result = session.get(endpoint_url, params=request_params)
        result.raise_for_status()
        return result.json()

    def get_session(self):
        """
        Returns a the current requests session.

        If one does not currently exist, then will create one.
        """
        if self.session is None:
            self.session = requests.Session()
        return self.session

    def generate_endpoint_url(self, endpoint):
        endpoint_url = '{base_url}{endpoint}'.format(base_url=Worthers.BASE_URL, endpoint=endpoint)
        return endpoint_url

    def generate_request_params(self, data, **extra_params):
        """
        https://cmsapi.cofeportal.org/request-parameters
        """
        json_data = self.encode_data(data)

        prepared_extra_params = self._prepare_extra_params(extra_params)

        # Uses an OrderedDict to ensure consistent results for testing & debug
        request_params = OrderedDict(prepared_extra_params)
        request_params['api_id'] = self.api_id
        request_params['data'] = json_data
        request_params['sig'] = self.generate_signature(json_data, **prepared_extra_params)

        return request_params

    def _prepare_extra_params(self, extra_params):
        # Filter out any None values
        extra_params_filtered = dict((k, v) for k, v in extra_params.items() if v is not None)

        # According to docs, only known Date fields are start_date and end_date
        if extra_params_filtered.get('start_date', False):
            extra_params_filtered['start_date'] = self.format_date(
                extra_params_filtered['start_date']
            )
        if extra_params_filtered.get('end_date', False):
            extra_params_filtered['end_date'] = self.format_date(
                extra_params_filtered['end_date']
            )

        return extra_params_filtered

    def format_date(self, python_datetime):
        return python_datetime.strftime(Worthers.DATE_FORMAT)

    def encode_data(self, data):
        """
        Returns a JSON representation of the supplied dict suitable for use in the 'data'
        parameter.
        """
        json_data = json.dumps(data)
        return json_data

    def generate_signature(self, json_data, **extra_params):
        """
        https://cmsapi.cofeportal.org/signing-requests
        """
        to_be_hashed = extra_params.copy()
        to_be_hashed['api_id'] = self.api_id
        to_be_hashed['data'] = json_data

        # The values to be hashed need to be sorted in alphabetical order by key
        hash_values = [str(value) for key, value in sorted(to_be_hashed.items())]

        msg = ''.join(hash_values).encode('utf-8')
        api_key = self.api_key.encode('utf-8')

        digest = hmac.new(api_key, msg=msg, digestmod=sha256).hexdigest()
        return digest
