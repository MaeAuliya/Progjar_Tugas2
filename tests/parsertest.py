import os
import sys
import unittest
from unittest.mock import patch, Mock

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
from src.htmlparser import HTMLParser

class TestClient(unittest.TestCase):
    def test_200(self):
        client = HTMLParser("its.ac.id", 443)

        with open(os.path.join(os.path.dirname(__file__), 'response.txt'), 'rb') as f:
            client.response = f.read().decode()

        client.separate_header()
        assert client.get_status_code() == "200 OK"
        assert client.get_http_version() == "HTTP/1.1"
        assert client.get_charset() == "utf-8"

    
    def test_404(self):
        client = HTMLParser("its.ac.id", 443)

        with open(os.path.join(os.path.dirname(__file__), 'response_404.txt'), 'rb') as f:
            client.response = f.read().decode()

        client.separate_header()
        assert client.get_status_code().rstrip() == "404 Not Found"
        assert client.get_http_version() == "HTTP/1.1"
        assert client.get_charset().rstrip() == "iso-8859-1"

