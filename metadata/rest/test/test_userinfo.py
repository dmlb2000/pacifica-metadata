#!/usr/bin/python
"""Test the UserInfoAPI object."""
from json import loads
import requests
from cherrypy.test import helper
from test_files.loadit import main
from metadata.rest.test import CPCommonTest, DockerMetadata


class TestUserInfoAPI(CPCommonTest, helper.CPWebCase):
    """Test aspects of the UserInfoAPI class."""

    @classmethod
    def teardown_class(cls):
        """Tear down the services required by the server."""
        super(TestUserInfoAPI, cls).teardown_class()
        DockerMetadata.stop_services()

    def test_userinfo_api(self):
        """Test the GET method."""
        main()
        # test by user_id
        user_id = 10
        req = requests.get('{0}/userinfo/by_id/{1}'.format(self.url, user_id))
        self.assertEqual(req.status_code, 200)
        req_json = loads(req.text)
        self.assertEqual(req_json['person_id'], user_id)

        # test search with name fragment
        search_terms = 'd+brown'
        req = requests.get(
            '{0}/userinfo/search/{1}'.format(self.url, search_terms))
        self.assertEqual(req.status_code, 200)
        req_json = loads(req.text)
        self.assertEqual(len(req_json), 1)
        user = req_json.pop()
        self.assertEqual(user['person_id'], user_id)

        # test search with network_id
        search_terms = 'dmlb2001'
        req = requests.get(
            '{0}/userinfo/search/{1}'.format(self.url, search_terms))
        self.assertEqual(req.status_code, 200)
        req_json = loads(req.text)
        self.assertEqual(len(req_json), 1)
        user = req_json.pop()
        self.assertEqual(user['person_id'], user_id)

        # test search with eus id
        search_terms = '10'
        req = requests.get(
            '{0}/userinfo/search/{1}'.format(self.url, search_terms))
        self.assertEqual(req.status_code, 200)
        req_json = loads(req.text)
        self.assertEqual(len(req_json), 1)
        user = req_json.pop()
        self.assertEqual(user['person_id'], user_id)

    def test_bad_userinfo_api(self):
        """Test the GET method with bad data."""
        str_user_id = 'bob'
        req = requests.get('{0}/userinfo/by_id/{1}'.format(self.url, str_user_id))
        self.assertEqual(req.status_code, 400)
        self.assertTrue('Invalid Lookup Options' in req.text)

        user_id = 11
        req = requests.get('{0}/userinfo/by_id/{1}'.format(self.url, user_id))
        self.assertEqual(req.status_code, 404)
        self.assertTrue('Not Found' in req.text)

        req = requests.get('{0}/userinfo/by_id'.format(self.url))
        self.assertEqual(req.status_code, 400)
        self.assertTrue('Invalid Lookup Options' in req.text)

        search_terms = 'd+millard'
        req = requests.get(
            '{0}/userinfo/search/{1}'.format(self.url, search_terms))
        self.assertEqual(req.status_code, 404)
        self.assertTrue('No Valid Users Located' in req.text)

        # search with no terms
        req = requests.get(
            '{0}/userinfo/search'.format(self.url))
        self.assertEqual(req.status_code, 400)
        self.assertTrue('Invalid Request' in req.text)
