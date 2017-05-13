import os.path
import logging
import logging.handlers

import requests
import boto
from boto.s3.key import Key
from celery import Celery

app = Celery('s3records', broker="redis://localhost")
logger = logging.getLogger('plivo-s3record-uploader')
logger.addHandler(logging.handlers.SysLogHandler())

@app.task(autoretry_for=(requests.exceptions.ConnectionError,), retry_kwargs={'max_retries': 5})
def record_upload(accesskey, secretkey, nbucket, region, params):

    if not os.path.exists(params['RecordFile']):
        raise RuntimeError("Not {} found".format(params['RecordFile']))

    if not params['callbackUrl']:
        params['callbackUrl'] = params['actionUrl']

    if not params['callbackUrl']:
        raise RuntimeError("callbackUrl not found in params")
    
    #upload to s3
    conn = boto.connect_s3(accesskey, secretkey)
    bucket = conn.get_bucket(nbucket)
    key = Key(bucket)
    key.key = os.path.basename(params['RecordFile'])
    key.set_contents_from_filename(params['RecordFile'])

    data = {}
    export_keys = ['RecordUrl',
                   'RecordingStartMs',
                   'RecordingEndMs',
                   'RecordDuration',
                   'RecordDurationMs',
                   'ConferenceUUID',
                   'ConferenceName',
                   'ConferenceAction']
    for ekey in export_keys:
        if params.has_key(ekey):
            data[ekey] = params[ekey]

    data['RecordUrl'] = "http://{}.s3.amazonaws.com/{}".format(nbucket, key.key)

    method = params['callbackMethod'] if params['callbackMethod'].upper() else 'POST'
    if method == 'GET':
        requests.get(params['callbackUrl'], params=data)
    else:
        requests.post(params['callbackUrl'], data=data)

    return True
