import unittest
from main import app
import os
import json
from env.settings import load_dotenv

load_dotenv()


class TestDBConnection(unittest.TestCase):
    test_table = os.environ['DATABASE_NAME']

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_connection(self):
        res = self.app.get('/v2/')
        self.assertEqual(b'working', res.data)

    # def create_table(self):
    #     res = self.app.post('/create_table')
    #     self.assertEqual(b'table created' or b'no tables created', res.data)

    def test_get_next(self):
        res = self.app.get('/v2/get_next')
        self.assertEqual('hello-world', res.data.decode())

    def test_insert(self):
        path = ['hello-world']
        res = self.app.post('/v2/push_paths', data={'path': path})
        res = json.loads(res.data)
        self.assertTrue(res['data'][0]['path'])

    def test_bulk_insert(self):
        paths = ['hello-world', 'hello-world2', 'hello-world3']
        res = self.app.post('/v2/push_paths', data={'path': paths})
        for i, val in enumerate(json.loads(res.data)['data']):
            # print(val)
            self.assertTrue(val['path'] in paths[i])

    def test_upload(self):
        url = '/v2/upload'
        bucket_name = os.getenv('BUCKET_NAME')
        if not bucket_name:
            bucket_name = 'test-bucket'
        path = 'hello-world'
        data = 'hello,world!!'
        payload = {
            'bucket_name': bucket_name,
            'path': path,
            'data': data,
        }
        res = self.app.post(url, data=payload)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, '/{}/{}'.format(bucket_name, path).encode())
