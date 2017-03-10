import hmac
import json
import math
from collections import OrderedDict
from hashlib import sha256

import requests


class CofeCMS(object):
    BASE_URL = 'https://cmsapi.cofeportal.org'
    DATE_FORMAT = '%Y-%m-%d %H:%M'
    DEFAULT_LIMIT = 100

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
        self, diocese_id=None, search_params=None, end_date=None, fields=None, limit=None,
        offset=None, start_date=None,
    ):
        """
        https://cmsapi.cofeportal.org/get-contacts
        """
        endpoint_url = self.generate_endpoint_url('/v2/contacts')
        result = self.paged_get(
            endpoint_url=endpoint_url, diocese_id=diocese_id, search_params=search_params,
            end_date=end_date, fields=fields, limit=limit, offset=offset, start_date=start_date,
        )
        return result

    def get_contact(self, contact_id, diocese_id=None):
        """
        https://cmsapi.cofeportal.org/get-contacts-id
        """
        endpoint_url = self.generate_endpoint_url('/v2/contacts/{}'.format(contact_id))
        result = self.paged_get(endpoint_url, diocese_id)
        return result

    def get_deleted_contacts(
        self, diocese_id=None, search_params=None, end_date=None, fields=None, limit=None,
        offset=None, start_date=None,
    ):
        endpoint_url = self.generate_endpoint_url('/v2/contacts/deleted')
        result = self.paged_get(
            endpoint_url=endpoint_url, diocese_id=diocese_id, search_params=search_params,
            end_date=end_date, fields=fields, limit=limit, offset=offset, start_date=start_date,
        )
        return result

    def get_contact_fields(self, diocese_id=None):
        endpoint_url = self.generate_endpoint_url('/v2/contact-fields')
        result = self.get(endpoint_url, diocese_id)
        return result

    def get(self, endpoint_url, diocese_id=None, search_params=None, **basic_params):
        request_params = self.generate_request_params(diocese_id, search_params, **basic_params)
        response = self.do_request(endpoint_url, request_params)

        from_json = response.json()

        # Sometimes the response is a dict, but we want it to be a list of dicts
        if isinstance(from_json, dict):
            from_json = [from_json]

        result = CofeCMSResult(from_json)
        result.api_obj = self
        result.response = response
        result.headers = response.headers
        result.endpoint_url = endpoint_url
        result.diocese_id = diocese_id
        result.search_params = search_params
        result.basic_params = basic_params
        result.rate_limit = int(response.headers['X-Rate-Limit'])
        result.rate_limit_remaining = int(response.headers['X-Rate-Limit-Remaining'])
        return result

    def paged_get(self, endpoint_url, diocese_id=None, search_params=None, **basic_params):
        basic_params['offset'] = basic_params.get('offset', 0)
        basic_params['limit'] = basic_params.get('limit', CofeCMS.DEFAULT_LIMIT)

        result = self.get(endpoint_url, diocese_id, search_params, **basic_params)

        result.total_count = int(result.headers['X-Total-Count'])

        result.offset = basic_params['offset']
        if 'offset' in result.basic_params:
            del(result.basic_params['offset'])

        result.limit = basic_params['limit']
        if 'limit' in result.basic_params:
            del(result.basic_params['limit'])
        return result

    def do_request(self, endpoint_url, request_params):
        session = self._get_session()
        result = session.get(endpoint_url, params=request_params)
        result.raise_for_status()
        return result

    def generate_endpoint_url(self, endpoint):
        endpoint_url = '{base_url}{endpoint}'.format(base_url=CofeCMS.BASE_URL, endpoint=endpoint)
        return endpoint_url

    def generate_request_params(self, diocese_id, search_params, **basic_params):
        """
        https://cmsapi.cofeportal.org/request-parameters
        """
        search_params = search_params or {}
        prepared_search_params = self._prepare_search_params(
            diocese_id=diocese_id, **search_params,
        )

        json_search_params = self.encode_search_params(prepared_search_params)

        prepared_basic_params = self._prepare_basic_params(basic_params)

        # Uses an OrderedDict to ensure consistent results for testing & debug
        request_params = OrderedDict(prepared_basic_params)
        request_params['api_id'] = self.api_id
        request_params['data'] = json_search_params
        request_params['sig'] = self.generate_signature(
            json_search_params, **prepared_basic_params
        )

        return request_params

    def format_date(self, python_datetime):
        return python_datetime.strftime(CofeCMS.DATE_FORMAT)

    def encode_search_params(self, search_params):
        """
        Returns a JSON representation of the supplied dict suitable for use in the 'search_params'
        parameter.
        """
        json_search_params = json.dumps(search_params)
        return json_search_params

    def generate_signature(self, json_search_params, **basic_params):
        """
        https://cmsapi.cofeportal.org/signing-requests
        """
        to_be_hashed = basic_params.copy()
        to_be_hashed['api_id'] = self.api_id
        to_be_hashed['data'] = json_search_params

        # The values to be hashed need to be sorted in alphabetical order by key
        hash_values = [str(value) for key, value in sorted(to_be_hashed.items())]

        msg = ''.join(hash_values).encode('utf-8')
        api_key = self.api_key.encode('utf-8')

        digest = hmac.new(api_key, msg=msg, digestmod=sha256).hexdigest()
        return digest

    def _prepare_search_params(self, **search_param_kwargs):
        search_params = OrderedDict(search_param_kwargs)

        diocese_id = search_param_kwargs.get('diocese_id', False) or self.diocese_id
        search_params['diocese_id'] = diocese_id
        return search_params

    def _get_session(self):
        """
        Returns a the current requests session.

        If one does not currently exist, then will create one.
        """
        if self.session is None:
            self.session = requests.Session()
        return self.session

    def _prepare_basic_params(self, basic_params):
        # Filter out any None values
        basic_params_filtered = dict((k, v) for k, v in basic_params.items() if v is not None)

        # According to docs, only known Date fields are start_date and end_date
        if basic_params_filtered.get('start_date', False):
            basic_params_filtered['start_date'] = self.format_date(
                basic_params_filtered['start_date']
            )
        if basic_params_filtered.get('end_date', False):
            basic_params_filtered['end_date'] = self.format_date(
                basic_params_filtered['end_date']
            )

        # Json encode the fields dictionary
        if basic_params_filtered.get('fields', False):
            basic_params_filtered['fields'] = json.dumps(basic_params_filtered['fields'])

        return basic_params_filtered


class CofeCMSResult(list):
    def __new__(self, *args, **kwargs):
        return super().__new__(self, args, kwargs)

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and hasattr(args[0], '__iter__'):
            list.__init__(self, args[0])
        else:
            list.__init__(self, args)
        self.__dict__.update(kwargs)

    def all(self):
        data = []
        for page in self.pages_generator():
            data = data + page
        return data

    def pages_generator(self):
        for current_page_num in range(0, self.total_pages):
            if current_page_num == 0:
                # No need to get current results again
                current_page_data = self
            else:
                current_page_data = self.get_data_for_page(current_page_num)
            yield current_page_data

    def get_data_for_page(self, page_num):
        offset = page_num * self.limit
        result = self.api_obj.paged_get(
            endpoint_url=self.endpoint_url, diocese_id=self.diocese_id,
            search_params=self.search_params, offset=offset, limit=self.limit,
            **self.basic_params,
        )
        return result

    @property
    def total_pages(self):
        return math.floor(self.total_count / self.limit) + 1
