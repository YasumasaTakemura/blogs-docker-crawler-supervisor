# coding:utf-8
import unittest
import logging
from main import app
import os


logger = logging.getLogger('LoggingUnitTest')
logger.setLevel(logging.INFO)

class TestVIew(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        pass


    def test_upload_file(self):
        url='upload_file'
        bucket_name = os.getenv('BUCKET_NAME')
        if not bucket_name:
            bucket_name = 'test-bucket-name'
        filename = 'Hotel_Review-g308257-d2071436-Reviews-Mana_Lagoon_Backpackers-Mana_Island_Mamanuca_Islands'
        data = 'hello,world!!'
        payload = {
            'bucket_name':bucket_name,
            'filename':filename,
            'data':data,
        }
        res = self.app.post(url,data=payload)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, '/{}/{}'.format(bucket_name,filename).encode())


    def test_upload(self):
        url='upload_file'
        bucket_name = os.getenv('BUCKET_NAME')
        if not bucket_name:
            bucket_name = 'test-bucket-name'
        filename = 'Hotel_Review-g308257-d2071436-Reviews-Mana_Lagoon_Backpackers-Mana_Island_Mamanuca_Islands'
        data = 'hello,world!!'
        payload = {
            'bucket_name':bucket_name,
            'filename':filename,
            'data':data,
        }
        res = self.app.post(url,data=payload)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, '/{}/{}'.format(bucket_name,filename).encode())

if __name__ == '__main__':
    unittest.main()
