# coding:utf-8
import unittest
import json
import base64
import mock
from app.utils.utils import get_enckey,decrypt_key
from app.store.store import Store
import requests
from six.moves import http_client

def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)

def _make_response(status=http_client.OK, content=b'', headers={}):
    response = requests.Response()
    response.status_code = status
    response._content = content
    response.headers = headers
    response.request = requests.Request()
    return response

def _make_json_response(data, status=http_client.OK, headers=None):
    headers = headers or {}
    headers['Content-Type'] = 'application/json'
    return _make_response(
        status=status,
        content=json.dumps(data).encode('utf-8'),
        headers=headers)


def _make_requests_session(responses):
    session = mock.create_autospec(requests.Session, instance=True)
    session.request.side_effect = responses
    return session


class TestDB(unittest.TestCase):
    def setUp(self):
        pass
        # app.config['TESTING'] = True
        # client = storage.Client('PROJECT')
        # print(client)


    def tearDown(self):
       pass

    def test_connection(self):
        pass

    def test_encrypt_key(self):
        enc_key = get_enckey()
        if not enc_key :
            enc_key = '3bXx72KXc3oWJ+CEDo7CM0anvBTryklFlOWAMp5QzNE='
        enc_key = base64.b64decode(enc_key)
        assert len(enc_key) == 32, 'Returned key should be 32 bytes'

    def test_decrypt_key(self):
        enc_key = get_enckey()
        key = decrypt_key(enc_key)
        assert len(key) == 32, 'Returned key should be 32 bytes'

    def test_write_gcs(self):
        store = Store()

if __name__ == '__main__':
    unittest.main()
