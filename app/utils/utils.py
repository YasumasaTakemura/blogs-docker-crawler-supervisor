import os
import base64
import logging


logger = logging.getLogger('LoggingUnitTest')
logger.setLevel(logging.INFO)

def get_enckey():
    key = os.getenv('SECRET')
    if not key:
        return None
    return key


def decrypt_key(key):
    if not key:
        logger.error('No Key Passed')
        raise ValueError('No Key Passed')
    return base64.b64decode(key)
