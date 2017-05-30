import datetime
from unittest import TestCase, mock

import httpretty
import requests

import cofecms
from cofecms.api import CofeCMS, CofeCMSResult, ContactData


class CofeCMSTest(TestCase):

    def setUp(self):
        self.cofecms = CofeCMS(api_id='test_api_id', api_key='test_api_key', diocese_id=123)

    def test_init(self):
        cofecms = CofeCMS(api_id='test_api_id', api_key='test_api_key')
        self.assertEqual(cofecms.api_id, 'test_api_id')
        self.assertEqual(cofecms.api_key, 'test_api_key')

        cofecms = CofeCMS(api_id='test_api_id', api_key='test_api_key', diocese_id=123)
        self.assertEqual(cofecms.api_id, 'test_api_id')
        self.assertEqual(cofecms.api_key, 'test_api_key')
        self.assertEqual(cofecms.diocese_id, 123)

    def test_diocese_id(self):
        cofecms = CofeCMS(api_id='test_api_id', api_key='test_api_key')
        with self.assertRaises(NotImplementedError):
            cofecms.diocese_id

        cofecms.diocese_id = 123
        self.assertEqual(cofecms.diocese_id, 123)

    def test_get_contacts(self):
        endpoint_url = 'https://cmsapi.cofeportal.org/v2/contacts'
        self.cofecms.generate_endpoint_url = mock.Mock(
            spec=self.cofecms.generate_endpoint_url,
            return_value=endpoint_url,
        )

        get_return = [{'wibble': 'wobble'}]
        self.cofecms.paged_get = mock.Mock(spec=self.cofecms.paged_get, return_value=get_return)

        result = self.cofecms.get_contacts()

        self.assertEqual(result, get_return)
        self.cofecms.generate_endpoint_url.assert_called_once_with('/v2/contacts')
        self.cofecms.paged_get.assert_called_once_with(
            endpoint_url,
            diocese_id=None,
            search_params=None,
            end_date=None,
            fields=None,
            limit=None,
            offset=None,
            start_date=None,
        )

    def test_get_contacts__with_args(self):
        endpoint_url = 'https://cmsapi.cofeportal.org/v2/contacts'
        self.cofecms.generate_endpoint_url = mock.Mock(
            spec=self.cofecms.generate_endpoint_url,
            return_value=endpoint_url,
        )

        get_return = [{'wibble': 'wobble'}]
        self.cofecms.paged_get = mock.Mock(spec=self.cofecms.paged_get, return_value=get_return)

        end_date = datetime.datetime.now()
        start_date = datetime.datetime.now()
        result = self.cofecms.get_contacts(
            diocese_id=123,
            search_params={'some_key': 'some_value'},
            end_date=end_date,
            fields={'contact': ['surname']},
            limit=10,
            offset=50,
            start_date=start_date,
        )

        self.assertEqual(result, get_return)
        self.cofecms.generate_endpoint_url.assert_called_once_with('/v2/contacts')
        self.cofecms.paged_get.assert_called_once_with(
            endpoint_url,
            diocese_id=123,
            search_params={'some_key': 'some_value'},
            end_date=end_date,
            fields={'contact': ['surname']},
            limit=10,
            offset=50,
            start_date=start_date,
        )

    def test_get_contact(self):
        endpoint_url = 'https://cmsapi.cofeportal.org/v2/contacts/123'
        self.cofecms.generate_endpoint_url = mock.Mock(
            spec=self.cofecms.generate_endpoint_url,
            return_value=endpoint_url,
        )

        get_return = [{'wibble': 'wobble'}]
        self.cofecms.paged_get = mock.Mock(spec=self.cofecms.get, return_value=get_return)

        result = self.cofecms.get_contact(123)

        self.assertEqual(result, get_return)
        self.cofecms.generate_endpoint_url.assert_called_once_with('/v2/contacts/123')
        self.cofecms.paged_get.assert_called_once_with(endpoint_url=endpoint_url, diocese_id=None)

    def test_get_deleted_contacts(self):
        endpoint_url = 'https://cmsapi.cofeportal.org/v2/contacts/deleted'
        self.cofecms.generate_endpoint_url = mock.Mock(
            spec=self.cofecms.generate_endpoint_url,
            return_value=endpoint_url,
        )

        get_return = [{'wibble': 'wobble'}]
        self.cofecms.paged_get = mock.Mock(spec=self.cofecms.get, return_value=get_return)

        result = self.cofecms.get_deleted_contacts(diocese_id=123, offset=50)

        self.assertEqual(result, get_return)
        self.cofecms.generate_endpoint_url.assert_called_once_with('/v2/contacts/deleted')
        self.cofecms.paged_get.assert_called_once_with(
            endpoint_url=endpoint_url,
            diocese_id=123,
            search_params=None,
            end_date=None,
            fields=None,
            limit=None,
            offset=50,
            start_date=None,
        )

    def test_get_posts(self):
        endpoint_url = 'https://cmsapi.cofeportal.org/v2/posts'
        self.cofecms.generate_endpoint_url = mock.Mock(
            spec=self.cofecms.generate_endpoint_url,
            return_value=endpoint_url,
        )

        get_return = [{'wibble': 'wobble'}]
        self.cofecms.paged_get = mock.Mock(spec=self.cofecms.paged_get, return_value=get_return)

        result = self.cofecms.get_posts()

        self.assertEqual(result, get_return)
        self.cofecms.generate_endpoint_url.assert_called_once_with('/v2/posts')
        self.cofecms.paged_get.assert_called_once_with(
            endpoint_url,
            diocese_id=None,
            search_params=None,
            end_date=None,
            fields=None,
            limit=None,
            offset=None,
            start_date=None,
        )

    def test_get_post(self):
        endpoint_url = 'https://cmsapi.cofeportal.org/v2/posts/123'
        self.cofecms.generate_endpoint_url = mock.Mock(
            spec=self.cofecms.generate_endpoint_url,
            return_value=endpoint_url,
        )

        get_return = [{'wibble': 'wobble'}]
        self.cofecms.paged_get = mock.Mock(spec=self.cofecms.get, return_value=get_return)

        result = self.cofecms.get_post(123)

        self.assertEqual(result, get_return)
        self.cofecms.generate_endpoint_url.assert_called_once_with('/v2/posts/123')
        self.cofecms.paged_get.assert_called_once_with(endpoint_url=endpoint_url, diocese_id=None)

    def test_get_deleted_posts(self):
        endpoint_url = 'https://cmsapi.cofeportal.org/v2/posts/deleted'
        self.cofecms.generate_endpoint_url = mock.Mock(
            spec=self.cofecms.generate_endpoint_url,
            return_value=endpoint_url,
        )

        get_return = [{'wibble': 'wobble'}]
        self.cofecms.paged_get = mock.Mock(spec=self.cofecms.get, return_value=get_return)

        result = self.cofecms.get_deleted_posts(diocese_id=123, offset=50)

        self.assertEqual(result, get_return)
        self.cofecms.generate_endpoint_url.assert_called_once_with('/v2/posts/deleted')
        self.cofecms.paged_get.assert_called_once_with(
            endpoint_url=endpoint_url,
            diocese_id=123,
            search_params=None,
            end_date=None,
            fields=None,
            limit=None,
            offset=50,
            start_date=None,
        )

    def test_get_places(self):
        endpoint_url = 'https://cmsapi.cofeportal.org/v2/places'
        self.cofecms.generate_endpoint_url = mock.Mock(
            spec=self.cofecms.generate_endpoint_url,
            return_value=endpoint_url,
        )

        get_return = [{'wibble': 'wobble'}]
        self.cofecms.paged_get = mock.Mock(spec=self.cofecms.paged_get, return_value=get_return)

        result = self.cofecms.get_places()

        self.assertEqual(result, get_return)
        self.cofecms.generate_endpoint_url.assert_called_once_with('/v2/places')
        self.cofecms.paged_get.assert_called_once_with(
            endpoint_url,
            diocese_id=None,
            search_params=None,
            end_date=None,
            fields=None,
            limit=None,
            offset=None,
            start_date=None,
        )

    def test_get_place(self):
        endpoint_url = 'https://cmsapi.cofeportal.org/v2/places/123'
        self.cofecms.generate_endpoint_url = mock.Mock(
            spec=self.cofecms.generate_endpoint_url,
            return_value=endpoint_url,
        )

        get_return = [{'wibble': 'wobble'}]
        self.cofecms.paged_get = mock.Mock(spec=self.cofecms.get, return_value=get_return)

        result = self.cofecms.get_place(123)

        self.assertEqual(result, get_return)
        self.cofecms.generate_endpoint_url.assert_called_once_with('/v2/places/123')
        self.cofecms.paged_get.assert_called_once_with(endpoint_url=endpoint_url, diocese_id=None)

    def test_get_deleted_places(self):
        endpoint_url = 'https://cmsapi.cofeportal.org/v2/places/deleted'
        self.cofecms.generate_endpoint_url = mock.Mock(
            spec=self.cofecms.generate_endpoint_url,
            return_value=endpoint_url,
        )

        get_return = [{'wibble': 'wobble'}]
        self.cofecms.paged_get = mock.Mock(spec=self.cofecms.get, return_value=get_return)

        result = self.cofecms.get_deleted_places(diocese_id=123, offset=50)

        self.assertEqual(result, get_return)
        self.cofecms.generate_endpoint_url.assert_called_once_with('/v2/places/deleted')
        self.cofecms.paged_get.assert_called_once_with(
            endpoint_url=endpoint_url,
            diocese_id=123,
            search_params=None,
            end_date=None,
            fields=None,
            limit=None,
            offset=50,
            start_date=None,
        )

    def test_get_contact_fields(self):
        endpoint_url = 'https://cmsapi.cofeportal.org/v2/contact-fields'
        self.cofecms.generate_endpoint_url = mock.Mock(
            spec=self.cofecms.generate_endpoint_url,
            return_value=endpoint_url,
        )

        get_return = [{'contact': ['id', 'surname']}]
        self.cofecms.get = mock.Mock(spec=self.cofecms.get, return_value=get_return)

        result = self.cofecms.get_contact_fields(123)

        self.assertEqual(result, get_return)
        self.cofecms.generate_endpoint_url.assert_called_once_with('/v2/contact-fields')
        self.cofecms.get.assert_called_once_with(endpoint_url=endpoint_url, diocese_id=123)

    def test_get_post_fields(self):
        endpoint_url = 'https://cmsapi.cofeportal.org/v2/post-fields'
        self.cofecms.generate_endpoint_url = mock.Mock(
            spec=self.cofecms.generate_endpoint_url,
            return_value=endpoint_url,
        )

        get_return = [{'contact': ['id', 'surname'], 'place': ['id', 'name']}]
        self.cofecms.get = mock.Mock(spec=self.cofecms.get, return_value=get_return)

        result = self.cofecms.get_post_fields(123)

        self.assertEqual(result, get_return)
        self.cofecms.generate_endpoint_url.assert_called_once_with('/v2/post-fields')
        self.cofecms.get.assert_called_once_with(endpoint_url=endpoint_url, diocese_id=123)

    def test_get_place_fields(self):
        endpoint_url = 'https://cmsapi.cofeportal.org/v2/place-fields'
        self.cofecms.generate_endpoint_url = mock.Mock(
            spec=self.cofecms.generate_endpoint_url,
            return_value=endpoint_url,
        )

        get_return = [{'place': ['id', 'name']}]
        self.cofecms.get = mock.Mock(spec=self.cofecms.get, return_value=get_return)

        result = self.cofecms.get_place_fields(123)

        self.assertEqual(result, get_return)
        self.cofecms.generate_endpoint_url.assert_called_once_with('/v2/place-fields')
        self.cofecms.get.assert_called_once_with(endpoint_url=endpoint_url, diocese_id=123)

    def test_get_roles(self):
        endpoint_url = 'https://cmsapi.cofeportal.org/v2/roles'
        self.cofecms.generate_endpoint_url = mock.Mock(
            spec=self.cofecms.generate_endpoint_url,
            return_value=endpoint_url,
        )

        get_return = [{'id': 6714, 'name': '*No ID card'}, {'id': 6682, 'name': 'AA Review'}]
        self.cofecms.get = mock.Mock(spec=self.cofecms.get, return_value=get_return)

        result = self.cofecms.get_roles(123)

        self.assertEqual(result, get_return)
        self.cofecms.generate_endpoint_url.assert_called_once_with('/v2/roles')
        self.cofecms.get.assert_called_once_with(endpoint_url=endpoint_url, diocese_id=123)

    def test_get__list_response(self):
        request_params = {'api_id': 'some_api_id', 'data': '{"json_key": "json_value"}'}
        self.cofecms.generate_request_params = mock.Mock(
            spec=self.cofecms.generate_request_params,
            return_value=request_params,
        )

        headers = {
            'X-Total-Count': '678',
            'X-Rate-Limit': '60',
            'X-Rate-Limit-Remaining': '59',
        }
        mock_response = mock.Mock(spec=requests.Response)
        mock_response.headers = headers
        mock_response.json.return_value = [{'some_key': 'some_value'}]
        self.cofecms.do_request = mock.Mock(
            spec=self.cofecms.do_request, return_value=mock_response
        )

        result = self.cofecms.get(
            'https://cmsapi.cofeportal.org/v2/some_end_point',
            diocese_id=123,
            search_params={'postcode': 'cv1 1aa'},
            wibble='wobble',
            limit=10,
        )

        self.assertEqual(result, [{'some_key': 'some_value'}])

        self.assertEqual(result.api_obj, self.cofecms)
        self.assertEqual(result.headers, headers)
        self.assertEqual(result.rate_limit, 60)
        self.assertEqual(result.rate_limit_remaining, 59)
        self.assertEqual(result.response, mock_response)
        self.assertEqual(result.endpoint_url, 'https://cmsapi.cofeportal.org/v2/some_end_point')
        self.assertEqual(result.diocese_id, 123)
        self.assertEqual(result.search_params, {'postcode': 'cv1 1aa'})
        self.assertEqual(result.basic_params, {'wibble': 'wobble', 'limit': 10})

        self.cofecms.generate_request_params.assert_called_once_with(
            diocese_id=123,
            search_params={'postcode': 'cv1 1aa'},
            wibble='wobble',
            limit=10,
        )
        self.cofecms.do_request.assert_called_once_with(
            endpoint_url='https://cmsapi.cofeportal.org/v2/some_end_point',
            request_params=request_params,
        )

    def test_get__dict_response(self):
        request_params = {'api_id': 'some_api_id', 'data': '{"json_key": "json_value"}'}
        self.cofecms.generate_request_params = mock.Mock(
            spec=self.cofecms.generate_request_params,
            return_value=request_params,
        )

        headers = {'X-Total-Count': '678', 'X-Rate-Limit': '60', 'X-Rate-Limit-Remaining': '59'}
        mock_response = mock.Mock(spec=requests.Response)
        mock_response.headers = headers
        mock_response.json.return_value = {'a_list': ['some_value']}
        self.cofecms.do_request = mock.Mock(
            spec=self.cofecms.do_request, return_value=mock_response
        )

        result = self.cofecms.get(
            'https://cmsapi.cofeportal.org/v2/some_end_point',
            diocese_id=123,
            search_params={'postcode': 'cv1 1aa'},
            wibble='wobble',
            limit=10,
        )

        self.assertEqual(result, [{'a_list': ['some_value']}])
        self.assertEqual(result.response, mock_response)
        self.cofecms.generate_request_params.assert_called_once_with(
            diocese_id=123,
            search_params={'postcode': 'cv1 1aa'},
            wibble='wobble',
            limit=10,
        )
        self.cofecms.do_request.assert_called_once_with(
            endpoint_url='https://cmsapi.cofeportal.org/v2/some_end_point',
            request_params=request_params,
        )

    def test_paged_get(self):
        endpoint_url = 'https://cmsapi.cofeportal.org/v2/contacts'

        get_return = CofeCMSResult([{'contact': ['id', 'surname']}])
        get_return.headers = {
            'X-Total-Count': '678',
            'X-Rate-Limit': '60',
            'X-Rate-Limit-Remaining': '59',
        }
        get_return.basic_params = {'limit': 100, 'offset': 0}
        self.cofecms.get = mock.Mock(spec=self.cofecms.get, return_value=get_return)

        result = self.cofecms.paged_get(endpoint_url=endpoint_url, diocese_id=123)

        self.assertEqual(result, get_return)
        self.assertEqual(result.total_count, 678)
        self.assertEqual(result.offset, 0)
        self.assertEqual(result.limit, 100)
        self.cofecms.get.assert_called_once_with(
            endpoint_url=endpoint_url,
            diocese_id=123,
            search_params=None,
            offset=0,
            limit=100,
        )

    def test_paged_get__with_offset(self):
        endpoint_url = 'https://cmsapi.cofeportal.org/v2/contacts'

        get_return = CofeCMSResult([{'contact': ['id', 'surname']}])
        get_return.headers = {
            'X-Total-Count': '678',
            'X-Rate-Limit': '60',
            'X-Rate-Limit-Remaining': '59',
        }
        get_return.basic_params = {}
        self.cofecms.get = mock.Mock(spec=self.cofecms.get, return_value=get_return)

        result = self.cofecms.paged_get(
            endpoint_url=endpoint_url,
            diocese_id=123,
            offset=100,
            limit=500,
        )

        self.assertEqual(result, get_return)
        self.assertEqual(result.total_count, 678)
        self.assertEqual(result.offset, 100)
        self.assertEqual(result.limit, 500)
        self.cofecms.get.assert_called_once_with(
            endpoint_url=endpoint_url,
            diocese_id=123,
            search_params=None,
            offset=100,
            limit=500,
        )

    def test_make_endpoint_url(self):
        result = self.cofecms.generate_endpoint_url('/v2/contacts')
        self.assertEqual(result, 'https://cmsapi.cofeportal.org/v2/contacts')

    def test_generate_request_params(self):
        prepared_search_params = {'diocese_id': 123}
        self.cofecms._prepare_search_params = mock.Mock(
            spec=self.cofecms._prepare_search_params, return_value=prepared_search_params
        )

        encode_search_params_return = '{"wibble": "wobble"}'
        self.cofecms.encode_search_params = mock.Mock(spec=self.cofecms.encode_search_params)
        self.cofecms.encode_search_params.return_value = encode_search_params_return

        prepare_extra_params_return = {'an_extra_param': 'param_value'}
        self.cofecms._prepare_basic_params = mock.Mock(spec=self.cofecms._prepare_basic_params)
        self.cofecms._prepare_basic_params.return_value = prepare_extra_params_return

        generate_signature_return = (
            '63f00f7c1a63b52d235d9c59cfcf14e2a5a85b09c896ffcb59087c334c042a05'
        )
        self.cofecms.generate_signature = mock.Mock(spec=self.cofecms.generate_signature)
        self.cofecms.generate_signature.return_value = generate_signature_return

        result = self.cofecms.generate_request_params(
            diocese_id=123,
            search_params={'wibble': 'wobble'},
            an_extra_param='param_value',
        )

        expected_result = {
            'api_id': 'test_api_id',
            'data': encode_search_params_return,
            'sig': generate_signature_return,
            'an_extra_param': 'param_value',
        }
        self.assertEqual(result, expected_result)
        self.cofecms._prepare_search_params.assert_called_once_with(
            diocese_id=123,
            wibble='wobble',
        )
        self.cofecms.generate_signature.assert_called_once_with(
            encode_search_params_return,
            an_extra_param='param_value',
        )
        self.cofecms._prepare_basic_params.assert_called_once_with({
            'an_extra_param': 'param_value'
        })

    def test__prepare_basic_params__remove_nones(self):
        params = {'good': 'good_value', 'none_value': None}
        result = self.cofecms._prepare_basic_params(params)

        expected_result = {'good': 'good_value'}
        self.assertEqual(result, expected_result)

    def test__prepare_basic_params__format_dates(self):
        params = {
            'good': 'good_value',
            'start_date': datetime.datetime(2017, 6, 9, 22, 30, 15),
            'end_date': datetime.datetime(2017, 8, 2, 9, 5, 1),
        }
        result = self.cofecms._prepare_basic_params(params)

        expected_result = {
            'good': 'good_value',
            'start_date': '2017-06-09 22:30',
            'end_date': '2017-08-02 09:05',
        }
        self.assertEqual(result, expected_result)

    def test__prepare_basic_params__encode_fields(self):
        params = {'good': 'good_value', 'fields': {'contact': ['forenames', 'surname']}}
        result = self.cofecms._prepare_basic_params(params)

        expected_result = {'good': 'good_value', 'fields': '{"contact": ["forenames", "surname"]}'}
        self.assertEqual(result, expected_result)

    def test_format_date(self):
        result = self.cofecms.format_date(datetime.datetime(2017, 6, 9, 22, 30, 15))
        self.assertEqual(result, '2017-06-09 22:30')

    def test_encode_search_params(self):
        result = self.cofecms.encode_search_params({'w i"b#b&le': 'w"o\'b&b[l/e'})
        self.assertEqual(result, '{"w i\\"b#b&le": "w\\"o\'b&b[l/e"}')

    def test_generate_signature(self):
        result = self.cofecms.generate_signature('simple_string_for_test', limit=1)
        self.assertEqual(
            result,
            '0247f853074bcfca97e05b5a7889eb612795fd525258cb04aad0ea2e578528e0',
        )

    def test__prepare_search_params(self):
        search_params = {'some_search_param': 'some_value'}
        result = self.cofecms._prepare_search_params(**search_params)
        expected_result = {'some_search_param': 'some_value', 'diocese_id': 123}
        self.assertEqual(result, expected_result)

        result = self.cofecms._prepare_search_params(diocese_id=456)
        self.assertEqual(result, {'diocese_id': 456})

        self.cofecms.diocese_id = 789
        result = self.cofecms._prepare_search_params()
        self.assertEqual(result, {'diocese_id': 789})

    @httpretty.activate
    def test_do_request(self):
        mock_session = mock.Mock(spec=requests.Session)
        self.cofecms._get_session = mock.Mock(spec=self.cofecms._get_session)
        self.cofecms._get_session.return_value = mock_session

        mock_response = mock.Mock(spec=requests.Response)
        mock_session.get.return_value = mock_response

        endpoint_url = 'http://example.com/endpoint'
        request_params = {'wibble': 'wobble'}

        result = self.cofecms.do_request(endpoint_url, request_params)

        self.assertEqual(result, mock_response)
        self.cofecms._get_session.assert_called_once_with()
        mock_session.get.assert_called_once_with(endpoint_url, params=request_params)
        mock_response.raise_for_status.assert_called_once_with()

    def test__get_session(self):
        self.assertIsNone(self.cofecms.session)
        session = self.cofecms._get_session()

        self.assertIsInstance(session, requests.Session)

        session_2 = self.cofecms._get_session()
        self.assertEqual(session, session_2)


class CofeCMSResultTest(TestCase):

    def test_init(self):
        cofecms_result = CofeCMSResult([1, 2, 3])
        self.assertEqual(cofecms_result, [1, 2, 3])

    def test_works_as_list(self):
        cofecms_result = CofeCMSResult()
        cofecms_result.append('wibble')
        cofecms_result.append('wobble')
        self.assertEqual(cofecms_result, ['wibble', 'wobble'])
        self.assertIn('wibble', cofecms_result)
        self.assertIn('wobble', cofecms_result)

        pop_result = cofecms_result.pop()
        self.assertEqual(pop_result, 'wobble')
        self.assertEqual(cofecms_result, ['wibble'])

    def test_getattr(self):
        cofecms_result = CofeCMSResult()
        cofecms_result.some_attr = 'wibble'
        self.assertEqual(cofecms_result.some_attr, 'wibble')

    def test_total_pages(self):
        cofecms_result = CofeCMSResult()
        cofecms_result.total_count = 1
        cofecms_result.limit = 100
        self.assertEqual(cofecms_result.total_pages, 1)

        cofecms_result.total_count = 9
        cofecms_result.limit = 7
        self.assertEqual(cofecms_result.total_pages, 2)

    def test_all(self):
        cofecms_result = CofeCMSResult()
        cofecms_result.pages_generator = mock.Mock(
            spec=cofecms_result.pages_generator, return_value=[[{'a': 'aa'}], [{'b': 'bb'}]]
        )

        result = cofecms_result.all()

        self.assertEqual(result, [{'a': 'aa'}, {'b': 'bb'}])

    def test_pages_generator(self):
        with mock.patch(
                'cofecms.api.CofeCMSResult.total_pages',
                new_callable=mock.PropertyMock,
        ) as mock_total_pages:
            mock_total_pages.return_value = 2

            cofecms_result = CofeCMSResult([{'a': 'aa'}])

            cofecms_result.get_data_for_page = mock.Mock(
                spec=cofecms_result.get_data_for_page,
                return_value=[{'b': 'bb'}],
            )

            results = []
            for result in cofecms_result.pages_generator():
                results.append(result)

            self.assertEqual(results, [[{'a': 'aa'}], [{'b': 'bb'}]])
            cofecms_result.get_data_for_page.assert_called_once_with(1)

    def test_get_data_for_page(self):
        cofecms_result = CofeCMSResult()
        cofecms_result.endpoint_url = 'http://example.com/some_end_point'
        cofecms_result.diocese_id = 123
        cofecms_result.search_params = {'keyword': 'smith'}
        cofecms_result.offset = 10
        cofecms_result.limit = 5
        cofecms_result.basic_params = {'fields': ['forenames', 'surname']}

        mock_api_obj = mock.Mock(spec=CofeCMS)
        cofecms_result.api_obj = mock_api_obj

        mock_result = mock.Mock(spec=CofeCMS)
        mock_api_obj.paged_get.return_value = mock_result

        result = cofecms_result.get_data_for_page(3)

        self.assertEqual(result, mock_result)

        mock_api_obj.paged_get.assert_called_once_with(
            endpoint_url='http://example.com/some_end_point',
            diocese_id=123,
            search_params={'keyword': 'smith'},
            offset=15,
            limit=5,
            fields=['forenames', 'surname'],
        )


class ContactDataTest(TestCase):

    def test_init(self):
        raw_contact_data = {'wibble': 'wobble'}
        contact_data = ContactData(raw_contact_data)
        self.assertEqual(contact_data.contact_data, raw_contact_data)
        self.assertEqual(contact_data.max_access_level, cofecms.PRIVACY_SETTING_PUBLIC)

        contact_data = ContactData(
            raw_contact_data,
            max_access_level=cofecms.PRIVACY_SETTING_PRIVATE,
        )
        self.assertEqual(contact_data.max_access_level, cofecms.PRIVACY_SETTING_PRIVATE)

    def test_get_item__public(self):
        raw_contact_data = {
            'wibble': 'wobble',  # No privacy settings
            'public': 'a',
            'public_privacy_setting': cofecms.PRIVACY_SETTING_PUBLIC,
            'diocese': 'b',
            'diocese_privacy_setting': cofecms.PRIVACY_SETTING_DIOCESE_ONLY,
            'private': 'c',
            'private_privacy_setting': cofecms.PRIVACY_SETTING_PRIVATE,
        }
        contact_data = ContactData(
            raw_contact_data,
            max_access_level=cofecms.PRIVACY_SETTING_PUBLIC,
        )

        self.assertEqual(contact_data['wibble'], 'wobble')
        with self.assertRaises(KeyError):
            self.assertEqual(contact_data['bad_key'], None)
        self.assertEqual(contact_data['public'], 'a')
        self.assertEqual(contact_data['diocese'], None)
        self.assertEqual(contact_data['private'], None)

    def test_get_item__diocese(self):
        raw_contact_data = {
            'wibble': 'wobble',  # No privacy settings
            'public': 'a',
            'public_privacy_setting': cofecms.PRIVACY_SETTING_PUBLIC,
            'diocese': 'b',
            'diocese_privacy_setting': cofecms.PRIVACY_SETTING_DIOCESE_ONLY,
            'private': 'c',
            'private_privacy_setting': cofecms.PRIVACY_SETTING_PRIVATE,
        }
        contact_data = ContactData(
            raw_contact_data,
            max_access_level=cofecms.PRIVACY_SETTING_DIOCESE_ONLY,
        )

        self.assertEqual(contact_data['wibble'], 'wobble')
        with self.assertRaises(KeyError):
            self.assertEqual(contact_data['bad_key'], None)
        self.assertEqual(contact_data['public'], 'a')
        self.assertEqual(contact_data['diocese'], 'b')
        self.assertEqual(contact_data['private'], None)

    def test_get_item__private(self):
        raw_contact_data = {
            'wibble': 'wobble',  # No privacy settings
            'public': 'a',
            'public_privacy_setting': cofecms.PRIVACY_SETTING_PUBLIC,
            'diocese': 'b',
            'diocese_privacy_setting': cofecms.PRIVACY_SETTING_DIOCESE_ONLY,
            'private': 'c',
            'private_privacy_setting': cofecms.PRIVACY_SETTING_PRIVATE,
        }
        contact_data = ContactData(
            raw_contact_data,
            max_access_level=cofecms.PRIVACY_SETTING_PRIVATE,
        )

        self.assertEqual(contact_data['wibble'], 'wobble')
        with self.assertRaises(KeyError):
            self.assertEqual(contact_data['bad_key'], None)
        self.assertEqual(contact_data['public'], 'a')
        self.assertEqual(contact_data['diocese'], 'b')
        self.assertEqual(contact_data['private'], 'c')
