# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from redyarn_server.test import BaseTestCase


class TestApiKeyController(BaseTestCase):
    """ApiKeyController integration test stubs"""

    def test_add_api_key(self):
        """Test case for add_api_key

        Create an api key with a new passphrase
        """
        query_string = [('new_passphrase', 'new_passphrase_example')]
        headers = { 
            'Accept': 'application/json',
            'admin_passphrase': 'special-key',
        }
        response = self.client.open(
            '/openapi/api_key',
            method='POST',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_api_key(self):
        """Test case for delete_api_key

        Revoke an api key
        """
        query_string = [('uid', 'uid_example')]
        headers = { 
            'admin_passphrase': 'special-key',
        }
        response = self.client.open(
            '/openapi/api_key',
            method='DELETE',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
