from unittest.mock import MagicMock, patch
import unittest
import os
import sys

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
SERVER_DIR = os.path.join(os.path.dirname(BASE_DIR), 'src/server')
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
from src.htmlparser import HTMLParser


class TestClient(unittest.TestCase):
    def test_unduh_pdf(self):
        client = HTMLParser("its.ac.id", 443)
        with open(os.path.join(os.path.dirname(__file__), 'response.txt'), 'rb') as f:
            client.response = f.read().decode()

        client.separate_header()
        menu = client.get_menu()
        assert '\tUnduh PDF' in menu

    def test_video(self):
        client = HTMLParser("its.ac.id", 443)

        with open(os.path.join(os.path.dirname(__file__), 'response.txt'), 'rb') as f:
            client.response = f.read().decode()

        client.separate_header()
        menu = client.get_menu()
        assert '\t[Video] Panduan Membuat Video Asinkronus dengan Power Point' in menu