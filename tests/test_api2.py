from unittest import TestCase, mock

from digitaldiocese_worthers.api2 import Worthers
import requests
import datetime


class WorthersTest(TestCase):

    def setUp(self):
        self.worthers = Worthers(api_id='test_api_id', api_key='test_api_key', diocese_id=123)

    def test_init(self):
        worthers = Worthers(api_id='test_api_id', api_key='test_api_key')
        self.assertEqual(worthers.api_id, 'test_api_id')
        self.assertEqual(worthers.api_key, 'test_api_key')

        worthers = Worthers(api_id='test_api_id', api_key='test_api_key', diocese_id=123)
        self.assertEqual(worthers.api_id, 'test_api_id')
        self.assertEqual(worthers.api_key, 'test_api_key')
        self.assertEqual(worthers.diocese_id, 123)

    def test_diocese_id(self):
        worthers = Worthers(api_id='test_api_id', api_key='test_api_key')
        with self.assertRaises(NotImplementedError):
            worthers.diocese_id

        worthers.diocese_id = 123
        self.assertEqual(worthers.diocese_id, 123)

    def test_make_endpoint_url(self):
        result = self.worthers.generate_endpoint_url('/v2/contacts')
        self.assertEqual(result, 'https://cmsapi.cofeportal.org/v2/contacts')

    def test_generate_request_params(self):
        encode_search_params_return = '{"wibble": "wobble"}'
        self.worthers.encode_search_params = mock.Mock(spec=self.worthers.encode_search_params)
        self.worthers.encode_search_params.return_value = encode_search_params_return

        prepare_extra_params_return = {'an_extra_param': 'param_value'}
        self.worthers._prepare_basic_params = mock.Mock(spec=self.worthers._prepare_basic_params)
        self.worthers._prepare_basic_params.return_value = prepare_extra_params_return

        generate_signature_return = (
            '63f00f7c1a63b52d235d9c59cfcf14e2a5a85b09c896ffcb59087c334c042a05'
        )
        self.worthers.generate_signature = mock.Mock(spec=self.worthers.generate_signature)
        self.worthers.generate_signature.return_value = generate_signature_return

        result = self.worthers.generate_request_params(
            {'wibble': 'wobble'}, an_extra_param='param_value',
        )

        expected_result = {
            'api_id': 'test_api_id', 'data': encode_search_params_return,
            'sig': generate_signature_return, 'an_extra_param': 'param_value',
        }
        self.assertEqual(result, expected_result)
        self.worthers.generate_signature.assert_called_once_with(
            encode_search_params_return, an_extra_param='param_value',
        )
        self.worthers._prepare_basic_params.assert_called_once_with(
            {'an_extra_param': 'param_value'}
        )

    def test__prepare_basic_params__remove_nones(self):
        params = {'good': 'good_value', 'none_value': None}
        result = self.worthers._prepare_basic_params(params)

        expected_result = {'good': 'good_value'}
        self.assertEqual(result, expected_result)

    def test__prepare_basic_params__format_dates(self):
        params = {
            'good': 'good_value',
            'start_date': datetime.datetime(2017, 6, 9, 22, 30, 15),
            'end_date': datetime.datetime(2017, 8, 2, 9, 5, 1),
        }
        result = self.worthers._prepare_basic_params(params)

        expected_result = {
            'good': 'good_value', 'start_date': '2017-06-09 22:30', 'end_date': '2017-08-02 09:05'
        }
        self.assertEqual(result, expected_result)

    def test_format_date(self):
        result = self.worthers.format_date(datetime.datetime(2017, 6, 9, 22, 30, 15))
        self.assertEqual(result, '2017-06-09 22:30')

    def test_encode_search_params(self):
        result = self.worthers.encode_search_params({'w i"b#b&le': 'w"o\'b&b[l/e'})
        self.assertEqual(
            result, '{"w i\\"b#b&le": "w\\"o\'b&b[l/e"}'
        )

    def test_generate_signature(self):
        result = self.worthers.generate_signature('simple_string_for_test', limit=1)
        self.assertEqual(
            result, '0247f853074bcfca97e05b5a7889eb612795fd525258cb04aad0ea2e578528e0'
        )

    def test_get_contacts(self):
        pass

    def test__prepare_search_params(self):
        search_params = {'some_search_param': 'some_value'}
        result = self.worthers._prepare_search_params(search_params)

        expected_result = {'some_search_param': 'some_value', 'diocese_id': 123}
        self.assertEqual(result, expected_result)

        result = self.worthers._prepare_search_params({}, 456)
        self.assertEqual(result, {'diocese_id': 456})

        self.worthers.diocese_id = 789
        result = self.worthers._prepare_search_params({})
        self.assertEqual(result, {'diocese_id': 789})

    def test_do_request(self):
        mock_session = mock.Mock(spec=requests.Session)
        self.worthers.get_session = mock.Mock(spec=self.worthers.get_session)
        self.worthers.get_session.return_value = mock_session

        expected_data = [{'some_key': 'some value'}]
        self.worthers._get_as_json = mock.Mock(spec=self.worthers._get_as_json)
        self.worthers._get_as_json.return_value = expected_data

        endpoint_url = 'http://example.com/endpoint'
        request_params = {'wibble': 'wobble'}

        result = self.worthers.do_request(endpoint_url, request_params)

        self.assertEqual(result, expected_data)
        self.worthers._get_as_json.assert_called_once_with(
            mock_session, endpoint_url, request_params
        )

    def test__get_as_json(self):
        expected_data = [{'some_key': 'some value'}]

        mock_response = mock.Mock(spec=requests.Response)
        mock_response.json.return_value = expected_data
        session = mock.Mock(spec=requests.Session)
        session.get.return_value = mock_response

        endpoint_url = 'http://example.com/endpoint'
        request_params = {'wibble': 'wobble'}

        result = self.worthers._get_as_json(session, endpoint_url, request_params)

        self.assertEqual(result, expected_data)
        session.get.assert_called_once_with(endpoint_url, params=request_params)
        mock_response.raise_for_status.assert_called_once_with()
        mock_response.json.assert_called_once_with()

    def test__get_as_json__exceptions(self):
        mock_response = mock.Mock(spec=requests.Response)
        mock_response.raise_for_status.side_effect = requests.HTTPError
        session = mock.Mock(spec=requests.Session)
        session.get.return_value = mock_response

        endpoint_url = 'http://example.com/endpoint'
        request_params = {'wibble': 'wobble'}

        with self.assertRaises(requests.HTTPError):
            self.worthers._get_as_json(session, endpoint_url, request_params)

    def test_get_session(self):
        self.assertIsNone(self.worthers.session)
        session = self.worthers.get_session()

        self.assertIsInstance(session, requests.Session)

        session_2 = self.worthers.get_session()
        self.assertEqual(session, session_2)
