import hmac
import json
import math
from collections import OrderedDict
from hashlib import sha256

import requests

PLACE_TYPE_ARCHDEACONRY = 1
PLACE_TYPE_BENEFICE = 2
PLACE_TYPE_CHURCH = 3
PLACE_TYPE_DEANERY = 4
PLACE_TYPE_DIOCESE = 5
PLACE_TYPE_EXTRA_PAROCHIAL = 6
PLACE_TYPE_NONPAROCHIAL = 7
PLACE_TYPE_PARISH = 8
PLACE_TYPE_SCHOOL = 9
PLACE_TYPE_DISTRICT = 10
PLACE_TYPE_OFFICE = 12
PLACE_TYPE_CLERGY_RESIDENCE = 13
PLACE_TYPE_GROUP = 14
PLACE_TYPE_HALL = 15

PRIVACY_SETTING_PRIVATE = 2
PRIVACY_SETTING_DIOCESE_ONLY = 1
PRIVACY_SETTING_PUBLIC = 0


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
            self,
            diocese_id=None,
            search_params=None,
            end_date=None,
            fields=None,
            limit=None,
            offset=None,
            start_date=None,
    ):
        """
        Retrieve a collection of contact records.

        API docs: https://cmsapi.cofeportal.org/get-contacts

        Args:
            diocese_id: Optionally supply the diocese_id.
            search_params: Optionally provide a dict of search params. See the API docs for more
                information.
            end_date: Optional datetime to only return records that were updated on or before this
                date.
            fields: Optional list of fields to be included in the response. See output of
                get_contact_fields() for a list of valid fields.
            limit: The maximum number of records to return at once. Maximum of 1000.
            offset: The number of records to skip. Used for getting paged results. Defaults to 0.
            start_date: Optional datetime to only return records that were updated on or after this
                date.

        Returns:
            A CofeCMSResult with the results of the query.
        """
        endpoint_url = self.generate_endpoint_url('/v2/contacts')
        result = self.paged_get(
            endpoint_url=endpoint_url,
            diocese_id=diocese_id,
            search_params=search_params,
            end_date=end_date,
            fields=fields,
            limit=limit,
            offset=offset,
            start_date=start_date,
        )
        return result

    def get_contact(self, contact_id, diocese_id=None):
        """
        Retrieve data on a single contact.

        API docs: https://cmsapi.cofeportal.org/get-contacts-id

        Args:
            contact_id: The ID of the requested contact
            diocese_id: Optionally supply the diocese_id.

        Returns:
            A CofeCMSResult with the results of the query.
        """
        endpoint_url = self.generate_endpoint_url('/v2/contacts/{}'.format(contact_id))
        result = self.paged_get(endpoint_url, diocese_id)
        return result

    def get_deleted_contacts(
            self,
            diocese_id=None,
            search_params=None,
            end_date=None,
            fields=None,
            limit=None,
            offset=None,
            start_date=None,
    ):
        """
        Retrieve a collection of deleted contact records.

        API docs: https://cmsapi.cofeportal.org/get-contacts-deleted

        Args:
            diocese_id: Optionally supply the diocese_id.
            search_params: Optionally provide a dict of search params. See the API docs for more
                information.
            end_date: Optional datetime to only return records that were updated on or before this
                date.
            fields: Optional list of fields to be included in the response. See output of
                get_contact_fields() for a list of valid fields.
            limit: The maximum number of records to return at once. Maximum of 1000.
            offset: The number of records to skip. Used for getting paged results. Defaults to 0.
            start_date: Optional datetime to only return records that were updated on or after this
                date.
        Returns:
            A CofeCMSResult with the results of the query.
        """
        endpoint_url = self.generate_endpoint_url('/v2/contacts/deleted')
        result = self.paged_get(
            endpoint_url=endpoint_url,
            diocese_id=diocese_id,
            search_params=search_params,
            end_date=end_date,
            fields=fields,
            limit=limit,
            offset=offset,
            start_date=start_date,
        )
        return result

    def get_posts(
            self,
            diocese_id=None,
            search_params=None,
            end_date=None,
            fields=None,
            limit=None,
            offset=None,
            start_date=None,
    ):
        """
        Retrieve a collection of records containing post, place, contact and role fields.

        API docs: https://cmsapi.cofeportal.org/get-posts

        Args:
            diocese_id: Optionally supply the diocese_id.
            search_params: Optionally provide a dict of search params. See the API docs for more
                information.
            end_date: Optional datetime to only return records that were updated on or before this
                date.
            fields: Optional list of fields to be included in the response. See output of
                get_contact_fields() for a list of valid fields.
            limit: The maximum number of records to return at once. Maximum of 1000.
            offset: The number of records to skip. Used for getting paged results. Defaults to 0.
            start_date: Optional datetime to only return records that were updated on or after this
                date.

        Returns:
            A CofeCMSResult with the results of the query.
        """
        endpoint_url = self.generate_endpoint_url('/v2/posts')
        result = self.paged_get(
            endpoint_url=endpoint_url,
            diocese_id=diocese_id,
            search_params=search_params,
            end_date=end_date,
            fields=fields,
            limit=limit,
            offset=offset,
            start_date=start_date,
        )
        return result

    def get_post(self, post_id, diocese_id=None):
        """
        Retrieve a single records containing post, place, contact and role fields.

        API docs: https://cmsapi.cofeportal.org/get-posts-id

        Args:
            post_id: The ID of the requested post
            diocese_id: Optionally supply the diocese_id.

        Returns:
            A CofeCMSResult with the results of the query.
        """
        endpoint_url = self.generate_endpoint_url('/v2/posts/{}'.format(post_id))
        result = self.paged_get(endpoint_url, diocese_id)
        return result

    def get_deleted_posts(
            self,
            diocese_id=None,
            search_params=None,
            end_date=None,
            fields=None,
            limit=None,
            offset=None,
            start_date=None,
    ):
        """
        Retrieve a collection of deleted records containing post, place, contact and role fields.

        API docs: https://cmsapi.cofeportal.org/get-posts-deleted

        Args:
            diocese_id: Optionally supply the diocese_id.
            search_params: Optionally provide a dict of search params. See the API docs for more
                information.
            end_date: Optional datetime to only return records that were updated on or before this
                date.
            fields: Optional list of fields to be included in the response. See output of
                get_contact_fields() for a list of valid fields.
            limit: The maximum number of records to return at once. Maximum of 1000.
            offset: The number of records to skip. Used for getting paged results. Defaults to 0.
            start_date: Optional datetime to only return records that were updated on or after this
                date.
        Returns:
            A CofeCMSResult with the results of the query.
        """
        endpoint_url = self.generate_endpoint_url('/v2/posts/deleted')
        result = self.paged_get(
            endpoint_url=endpoint_url,
            diocese_id=diocese_id,
            search_params=search_params,
            end_date=end_date,
            fields=fields,
            limit=limit,
            offset=offset,
            start_date=start_date,
        )
        return result

    def get_places(
            self,
            diocese_id=None,
            search_params=None,
            end_date=None,
            fields=None,
            limit=None,
            offset=None,
            start_date=None,
    ):
        """
        Retrieve a collection of place records.

        API docs: https://cmsapi.cofeportal.org/get-places

        Args:
            diocese_id: Optionally supply the diocese_id.
            search_params: Optionally provide a dict of search params. See the API docs for more
                information.
            end_date: Optional datetime to only return records that were updated on or before this
                date.
            fields: Optional list of fields to be included in the response. See output of
                get_contact_fields() for a list of valid fields.
            limit: The maximum number of records to return at once. Maximum of 1000.
            offset: The number of records to skip. Used for getting paged results. Defaults to 0.
            start_date: Optional datetime to only return records that were updated on or after this
                date.

        Returns:
            A CofeCMSResult with the results of the query.
        """
        endpoint_url = self.generate_endpoint_url('/v2/places')
        result = self.paged_get(
            endpoint_url=endpoint_url,
            diocese_id=diocese_id,
            search_params=search_params,
            end_date=end_date,
            fields=fields,
            limit=limit,
            offset=offset,
            start_date=start_date,
        )
        return result

    def get_place(self, place_id, diocese_id=None):
        """
        Retrieve a single place record.

        API docs: https://cmsapi.cofeportal.org/get-places-id

        Args:
            place_id: The ID of the requested place
            diocese_id: Optionally supply the diocese_id.

        Returns:
            A CofeCMSResult with the results of the query.
        """
        endpoint_url = self.generate_endpoint_url('/v2/places/{}'.format(place_id))
        result = self.paged_get(endpoint_url, diocese_id)
        return result

    def get_deleted_places(
            self,
            diocese_id=None,
            search_params=None,
            end_date=None,
            fields=None,
            limit=None,
            offset=None,
            start_date=None,
    ):
        """
        Retrieve a collection of deleted place records.

        API docs: https://cmsapi.cofeportal.org/get-places-deleted

        Args:
            diocese_id: Optionally supply the diocese_id.
            search_params: Optionally provide a dict of search params. See the API docs for more
                information.
            end_date: Optional datetime to only return records that were updated on or before this
                date.
            fields: Optional list of fields to be included in the response. See output of
                get_contact_fields() for a list of valid fields.
            limit: The maximum number of records to return at once. Maximum of 1000.
            offset: The number of records to skip. Used for getting paged results. Defaults to 0.
            start_date: Optional datetime to only return records that were updated on or after this
                date.
        Returns:
            A CofeCMSResult with the results of the query.
        """
        endpoint_url = self.generate_endpoint_url('/v2/places/deleted')
        result = self.paged_get(
            endpoint_url=endpoint_url,
            diocese_id=diocese_id,
            search_params=search_params,
            end_date=end_date,
            fields=fields,
            limit=limit,
            offset=offset,
            start_date=start_date,
        )
        return result

    def get_contact_fields(self, diocese_id=None):
        """
        Retrieves all possible fields for contacts.

        API docs: https://cmsapi.cofeportal.org/get-contact-fields

        Args:
            diocese_id: Optionally supply the diocese_id.

        Returns:
            A CofeCMSResult with the results of the query.
        """
        endpoint_url = self.generate_endpoint_url('/v2/contact-fields')
        result = self.get(endpoint_url, diocese_id)
        return result

    def get_post_fields(self, diocese_id=None):
        """
        Retrieves all possible fields for posts.

        API docs: https://cmsapi.cofeportal.org/get-post-fields

        Args:
            diocese_id: Optionally supply the diocese_id.

        Returns:
            A CofeCMSResult with the results of the query.
        """
        endpoint_url = self.generate_endpoint_url('/v2/post-fields')
        result = self.get(endpoint_url, diocese_id)
        return result

    def get_place_fields(self, diocese_id=None):
        """
        Retrieves all possible fields for places.

        API docs: https://cmsapi.cofeportal.org/get-place-fields

        Args:
            diocese_id: Optionally supply the diocese_id.

        Returns:
            A CofeCMSResult with the results of the query.
        """
        endpoint_url = self.generate_endpoint_url('/v2/place-fields')
        result = self.get(endpoint_url, diocese_id)
        return result

    def get_roles(self, diocese_id=None):
        """
        Retrieves all defined role names and their ID.

        API docs: https://cmsapi.cofeportal.org/get-roles

        Args:
            diocese_id: Optionally supply the diocese_id.

        Returns:
            A CofeCMSResult with the results of the query.
        """
        endpoint_url = self.generate_endpoint_url('/v2/roles')
        result = self.get(endpoint_url, diocese_id)
        return result

    def get(self, endpoint_url, diocese_id=None, search_params=None, **basic_params):
        """
        Perform a generic request against the API and retrieves the results.

        Note: This is a fairly raw way of requesting data from the API and will not hold your hand
        for dealing with paged results. See 'paged_get' for a better way of doing raw queries
        with paged results.

        Args:
            endpoint_url: The absolute URL for the endpoint to use. For example:
                https://cmsapi.cofeportal.org/v2/contacts
            diocese_id: Optionally supply the diocese_id.
            search_params: A dict containing search params. The API docs contain more information
                on this: https://cmsapi.cofeportal.org/json-data-string.
            **basic_params: Pass general request parameters as needed by the endpoint. 'api_id',
                'data' and 'sig' params are automatically added for you. The API docs give more
                information on what params can be used:
                https://cmsapi.cofeportal.org/request-parameters

        Returns:
            A CofeCMSResult with the results and details of the query.
        """
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
        """
        Similar to 'get', however it also populates the result object with the necessary
        information to make requests for more pages of data easier.

        Args:
            endpoint_url: The absolute URL for the endpoint to use. For example:
                https://cmsapi.cofeportal.org/v2/contacts
            diocese_id: Optionally supply the diocese_id.
            search_params: A dict containing search params. The API docs contain more information
                on this: https://cmsapi.cofeportal.org/json-data-string.
            **basic_params: Pass general request parameters as needed by the endpoint. 'api_id',
                'data' and 'sig' params are automatically added for you. The API docs give more
                information on what params can be used:
                https://cmsapi.cofeportal.org/request-parameters

        Returns:
            A CofeCMSResult with the results and details of the query.

            The CofeCMSResult will be populated with the used offset, limit used in the request,
            and will also add the total_count attribute from the 'X-Total-Count' header.
        """
        basic_params['offset'] = basic_params.get('offset', 0)
        basic_params['limit'] = basic_params.get('limit', False) or CofeCMS.DEFAULT_LIMIT

        result = self.get(endpoint_url, diocese_id, search_params, **basic_params)

        result.total_count = int(result.headers['X-Total-Count'])

        result.offset = basic_params['offset']
        if 'offset' in result.basic_params:
            del (result.basic_params['offset'])

        result.limit = basic_params['limit']
        if 'limit' in result.basic_params:
            del (result.basic_params['limit'])
        return result

    def do_request(self, endpoint_url, request_params):
        """
        Performs a request to the given endpoint_url with the supplied request params.

        Args:
            endpoint_url: The absolute URL for the endpoint to use. For example:
                https://cmsapi.cofeportal.org/v2/contacts
            request_params: A dict containing the GET params for this request. Will be URL encoded
                for you.

        Returns:
            An unmolested requests.Result object.

        Raises:
            Will raise the appropriate HTTP exception for any non-200 HTTP response.
        """
        session = self._get_session()
        result = session.get(endpoint_url, params=request_params)
        result.raise_for_status()
        return result

    def generate_endpoint_url(self, endpoint):
        """
        Generate an absolute URL for a given endpoint.

        Uses the BASE_URL constant.

        Args:
            endpoint: The endpoint to use, as defined in the specs. For example: '/v2/contacts'.

        Returns:
            The absolute URL for the given endpoint.
        """
        endpoint_url = '{base_url}{endpoint}'.format(base_url=CofeCMS.BASE_URL, endpoint=endpoint)
        return endpoint_url

    def generate_request_params(self, diocese_id, search_params, **basic_params):
        """
        Generate a dict containing the GET request parameters for a request.

        The required 'api_id', 'data' and 'sig' params are always added.

        API docs: https://cmsapi.cofeportal.org/request-parameters

        Args:
            diocese_id: Optionally supply the diocese_id.
            search_params: A dict of search params. The API docs have more information on this:
                https://cmsapi.cofeportal.org/json-data-string.
            **basic_params: Any extra params for the API call, for example to set a limit on.

        Returns:
            A dict containing the final requst params, including the calculated signing 'sig'.
        """
        search_params = search_params or {}
        prepared_search_params = self._prepare_search_params(
            diocese_id=diocese_id, **search_params
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
        """
        Format the given Python datetime to the format used by the API.

        Args:
            python_datetime: The datetime to format

        Returns:
            A string representation of the date which can be used by the API.
        """
        return python_datetime.strftime(CofeCMS.DATE_FORMAT)

    def encode_search_params(self, search_params):
        """
        Generate a JSON representation of the supplied dict suitable for use in the 'search_params'
        parameter.

        Args:
            search_params: A dict of search params. The API docs contain more information:
                https://cmsapi.cofeportal.org/json-data-string.

        Returns:
            A JSON string of the provided search_params.
        """
        json_search_params = json.dumps(search_params)
        return json_search_params

    def generate_signature(self, json_search_params, **basic_params):
        """
        Generate a signature used for signing each request.

        The process is described here: https://cmsapi.cofeportal.org/signing-requests

        Args:
            json_search_params: The JSON encoded search_params.
            **basic_params: Any extra params for the request.

        Returns:
            A string containing the hexadecimal signature for the request.
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
            basic_params_filtered['start_date'
                                  ] = self.format_date(basic_params_filtered['start_date'])
        if basic_params_filtered.get('end_date', False):
            basic_params_filtered['end_date'] = self.format_date(basic_params_filtered['end_date'])

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
        """
        Retrieve the data for all pages of results from the inital query.

        Warning: Can be quite slow to run as a request will be made for each page. Suggest reducing
        the number of pages by increasing the "limit" when performing the initial query.

        Returns:
            A list of result data (which are usually dicts).
        """
        data = []
        for page in self.pages_generator():
            data = data + page
        return data

    def pages_generator(self):
        """
        A generator to iterate through all the pages in the initial query.

        Warning: Can be quite slow to run as a request will be made for each page. Suggest reducing
        the number of pages by increasing the "limit" when performing the initial query.
        """
        for current_page_num in range(0, self.total_pages):
            if current_page_num == 0:
                # No need to get current results again
                current_page_data = self
            else:
                current_page_data = self.get_data_for_page(current_page_num)
            yield current_page_data

    def get_data_for_page(self, page_num):
        """
        Retrieve the data for a specific page in the initial query.

        Args:
            page_num: The number of the page to get. Zero indexed.

        Returns:
            A CofeCMSResult object, populated with data for the requested page.
        """
        offset = page_num * self.limit
        result = self.api_obj.paged_get(
            endpoint_url=self.endpoint_url,
            diocese_id=self.diocese_id,
            search_params=self.search_params,
            offset=offset,
            limit=self.limit,
            **self.basic_params
        )
        return result

    @property
    def total_pages(self):
        """
        Calculate how many pages of results are in the entire result set.

        The COFE CMS API tends to not give an accurate "total_count" of results. So this should be
        seen as calculating the maximum number of pages.

        Returns:
            An int of of the number of pages.
        """
        return math.floor(self.total_count / self.limit) + 1


class ContactData(object):
    """
    A wrapper to provide easy access to Worthers contact data, whilst taking into account privacy
    settings.
    """

    def __init__(self, contact_data, max_access_level=PRIVACY_SETTING_PUBLIC):
        self.contact_data = contact_data
        self.max_access_level = max_access_level

    def __getitem__(self, key):
        """
        Will return the value if there's no privacy settings found, or if the privacy settings
        allow it.

        If privacy settings say no, then will return None.

        If the key is not found, will raise a KeyError.
        """
        privacy_key = '{key}_privacy_setting'.format(key=key)

        if privacy_key not in self.contact_data.keys():
            # Not a value which has privacy settings
            return self.contact_data[key]

        if self.contact_data[privacy_key] <= self.max_access_level:
            return self.contact_data[key]

        return None
