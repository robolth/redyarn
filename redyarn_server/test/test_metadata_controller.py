# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from redyarn_server.models.metadata import Metadata  # noqa: E501
from redyarn_server.test import BaseTestCase


class TestMetadataController(BaseTestCase):
    """MetadataController integration test stubs"""

    def test_delete_all_metadata(self):
        """Test case for delete_all_metadata

        Delete all metadata
        """
        headers = { 
            'admin_passphrase': 'special-key',
        }
        response = self.client.open(
            '/openapi/metadata/ls/',
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_metadata(self):
        """Test case for delete_metadata

        Delete a file metadata
        """
        query_string = [('idFile', 'id_file_example')]
        headers = { 
            'admin_passphrase': 'special-key',
        }
        response = self.client.open(
            '/openapi/metadata/',
            method='DELETE',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_all_metadata(self):
        """Test case for get_all_metadata

        List all metadata
        """
        headers = { 
            'Accept': 'text/html',
        }
        response = self.client.open(
            '/openapi/metadata/ls/',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_asciiart(self):
        """Test case for get_asciiart

        Get an image ascii-art conversion
        """
        query_string = [('idFile', 'id_file_example')]
        headers = { 
            'Accept': 'text/plain',
        }
        response = self.client.open(
            '/openapi/metadata/ascii-art/',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_metadata(self):
        """Test case for get_metadata

        Get a file metadata
        """
        query_string = [('idFile', 'id_file_example')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/openapi/metadata/',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
