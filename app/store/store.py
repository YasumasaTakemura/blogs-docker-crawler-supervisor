import base64
import bz2
import logging
from flask import abort
from google.cloud import storage
from google.api_core.exceptions import Forbidden
from google.api_core.exceptions import Conflict

logger = logging.getLogger('Store_model')


class Store(object):
    """singleton"""
    _instance = None

    def __init__(self):
        self.connect()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def connect(self):
        try:
            self.client = storage.Client()
        except Exception as e:
            logger.error(str(e))

    def create_bucket(self, bucket_name):
        try:
            bucket = self.client.create_bucket(bucket_name)
            return bucket.name
        except Conflict as e:
            logger.error(e)
            abort(400, '')

    def delete_bucket(self, bucket_name):
        """Deletes a bucket. The bucket must be empty."""
        bucket = self.client.get_bucket(bucket_name)
        bucket.delete()
        logger.error('Bucket {} deleted'.format(bucket.name))
        print('Bucket {} deleted'.format(bucket.name))

    def list_blobs(self, bucket_name):
        """Lists all the blobs in the bucket."""
        # type : (str)=> (list)
        try:
            bucket = self.client.get_bucket(bucket_name)
        except Exception as e:
            logger.error(e)
            raise Exception(str(e))

        blobs = bucket.list_blobs()
        res = []
        for blob in blobs:
            res.append(blob.name)
        return res

    def list_blobs_with_prefix(self, bucket_name, prefix, delimiter='/'):
        """Lists all the blobs in the bucket."""
        # type : (str)=> (list)
        bucket = self.client.get_bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=prefix, delimiter=delimiter)
        res = []
        for blob in blobs:
            res.append(blob.name)
        if delimiter:
            for prefix in blobs.prefixes:
                res.append(prefix)
        return res

    def write(self, bucket_name, filename, data, enc_key=None):
        try:
            bucket = self.client.get_bucket(bucket_name)
        except Forbidden as e:
            logger.error(e)
            raise Forbidden(str(e))
        blob = storage.Blob(filename, bucket, encryption_key=enc_key)
        data = bz2.compress(data.encode(), 9)
        try:
            blob.upload_from_string(data, content_type='application/gzip')
            return '/{}/{}'.format(bucket_name, filename)
        except Exception as e:
            logger.error(e)

    def read(self, bucket_name, enc_key, filename):
        bucket = self.client.get_bucket(bucket_name)
        encryption_key = base64.b64decode(enc_key)
        blob = storage.Blob(filename, bucket, encryption_key=encryption_key)
        data = blob.download_to_filename(filename)
        return bz2.decompress(data)
