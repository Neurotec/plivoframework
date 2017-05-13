from unittest import TestCase

import os
import mock
from cgi import parse_qs

import boto
import boto.s3


from plivo.worker.s3record import record_upload

import gevent
from gevent.pywsgi import WSGIServer
from gevent import monkey; monkey.patch_all()

class TestRESTCallback(object):

    def __init__(self):
        self.server = WSGIServer(('127.0.0.1', 48123), self.app)
        
    def start(self):
        self.server.serve_forever()

    def app(self, env, start_response):
        request_body = env['wsgi.input'].read(int(env.get('CONTENT_LENGTH', 0)))
        data = parse_qs(request_body)
        assert data.get('RecordingStartMs')[0] == '99'
        assert data.get('RecordingEndMs')[0] == '99'
        assert data.get('RecordDuration')[0] == '99'
        assert data.get('RecordDurationMs')[0] == '99'
        assert data.get('ConferenceUUID')[0] == '99'
        assert data.get('ConferenceName')[0] == '99'
        assert data.get('ConferenceAction')[0] == 'record'
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b"<b>OK</b>"]
    
class TestS3Record(TestCase):
    """
    Test worker uploader
    """

    def setUp(self):

        self.accesskey = os.environ.get('AWS_ACCESS_KEY', '')
        self.secretkey = os.environ.get('AWS_SECRET_KEY', '')
        if not self.secretkey:
            raise RuntimeError('Need env AWS_SECRET_KEY')
        if not self.accesskey:
           raise RuntimeError('Need ENV AWS_ACCESS_KEY')
       
        self.bucket = os.environ.get('AWS_BUCKET', '')

        if not self.bucket:
            raise RuntimeError('Need ENV AWS_BUCKET')

        s = TestRESTCallback()
        self.server_proc = gevent.spawn(s.start)
        gevent.sleep(0.2)

    def tearDown(self):
        try:
            self.server_proc.kill()
        except:
            pass

        
    def test_record_upload_not_file_found(self):
        data = {
            'RecordFile': ''
        }
        with self.assertRaises(RuntimeError):
            record_upload('', '', '', '', data)

    @mock.patch('plivo.worker.s3record.record_upload.retry')
    def test_record_upload_and_notify_failed(self, record_upload_retry):
        with open('/tmp/private', 'w') as fp:
            fp.write('testing')
        data = {
            'callbackUrl': 'http://localhost:4800',
            'callbackMethod': 'POST',
            'RecordFile': '/tmp/private',
            'RecordingStartMs': 99,
            'RecordingEndMs': 99,
            'RecordDuration': 99,
            'RecordDurationMs': 99,
            'ConferenceUUID': 99,
            'ConferenceName': 99,
            'ConferenceAction': 'record',
        }
        #this really must raise Retry
        with self.assertRaises(TypeError):
            record_upload(self.accesskey, self.secretkey, self.bucket, None, data)


    @mock.patch('plivo.worker.s3record.record_upload.retry')
    def test_record_upload_and_notify(self, record_upload_retry):
        with open('/tmp/private', 'w') as fp:
            fp.write('testing')
        data = {
            'callbackUrl': 'http://localhost:48123',
            'callbackMethod': 'POST',
            'RecordFile': '/tmp/private',
            'RecordingStartMs': 99,
            'RecordingEndMs': 99,
            'RecordDuration': 99,
            'RecordDurationMs': 99,
            'ConferenceUUID': 99,
            'ConferenceName': 99,
            'ConferenceAction': 'record',
        }
        record_upload(self.accesskey, self.secretkey, self.bucket, None, data)

    
    
