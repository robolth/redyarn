# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from redyarn_server.models.inline_object import InlineObject  # noqa: E501
from redyarn_server.models.metadata import Metadata  # noqa: E501
from redyarn_server.test import BaseTestCase


class TestFileController(BaseTestCase):
    """FileController integration test stubs"""

    @unittest.skip("multipart/form-data not supported by Connexion")
    def test_post_file(self):
        """Test case for post_file

        Upload a file
        """
        inline_object = {}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'multipart/form-data',
            'admin_passphrase': 'special-key',
            'passphrase': 'special-key',
        }
        response = self.client.open(
            '/openapi/file',
            method='POST',
            headers=headers,
            data=json.dumps(inline_object),
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
