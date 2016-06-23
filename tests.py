from EmbeddedCI import app
import os
import unittest
import mock
import tempfile
import json

class EmbeddedCITestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_webhook_no_signature(self):
        response = self.app.post('/github/')
        self.assertEquals(
            json.loads(response.get_data()),
            {
                u'message':
                {
                    u'X-Hub-Signature': u'Missing required parameter in the HTTP headers'
                }
            }
        )

        self.assertEquals(
            response.status_code,
            400
        )

    def test_webhook_no_event(self):
        response = self.app.post(
            '/github/',
            headers={
                'X-Hub-Signature': 'sha1=asldkjlaskdj'
            }
        )
        self.assertEquals(
            json.loads(response.get_data()),
            {
                u'message':
                {
                    u'X-GitHub-Event': u'Missing required parameter in the HTTP headers'
                }
            }
        )

        self.assertEquals(
            response.status_code,
            400
        )

    @mock.patch('EmbeddedCI.github.views.Github.verify_signature')
    def test_webhook_bad_signature(self, m_verify_signature):
        m_verify_signature.return_value = False
        response = self.app.post(
            '/github/',
            headers={
                'X-Hub-Signature' : 'sha1=asldkjlaskdj',
                'X-GitHub-Event'  : 'ping'
            }
        )
        self.assertEquals(
            json.loads(response.get_data()),
            {
                u'msg': u'bad signature'
            }
        )

        self.assertEquals(
            response.status_code,
            401
        )

    @mock.patch('EmbeddedCI.github.views.Github.verify_signature')
    def test_webhook_ping_event(self, m_verify_signature):
        m_verify_signature.return_value = True
        response = self.app.post(
            '/github/',
            headers={
                'X-Hub-Signature' : 'sha1=asldkjlaskdj',
                'X-GitHub-Event'  : 'ping'
            }
        )
        self.assertEquals(
            json.loads(response.get_data()),
            {
                u'msg': u'ok'
            }
        )

        self.assertEquals(
            response.status_code,
            200
        )

    @mock.patch('EmbeddedCI.github.views.Github.verify_signature')
    def test_webhook_push_event(self, m_verify_signature):
        m_verify_signature.return_value = True
        response = self.app.post(
            '/github/',
            headers={
                'X-Hub-Signature' : 'sha1=asldkjlaskdj',
                'X-GitHub-Event'  : 'push'
            }
        )
        self.assertEquals(
            json.loads(response.get_data()),
            {
                u'msg': u'push'
            }
        )

        self.assertEquals(
            response.status_code,
            200
        )

    @mock.patch('EmbeddedCI.github.views.Github.verify_signature')
    def test_webhook_unsupported_event(self, m_verify_signature):
        m_verify_signature.return_value = True
        response = self.app.post(
            '/github/',
            headers={
                'X-Hub-Signature' : 'sha1=asldkjlaskdj',
                'X-GitHub-Event'  : 'other'
            }
        )
        self.assertEquals(
            json.loads(response.get_data()),
            {
                u'msg': u'unsupported event type: other'
            }
        )

        self.assertEquals(
            response.status_code,
            400
        )

if __name__ == '__main__':
    unittest.main()