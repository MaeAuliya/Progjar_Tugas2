import os
import sys
import unittest
from unittest.mock import patch, Mock

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
from src.htmlparser import HTMLParser

class TestClient(unittest.TestCase):
    def test_Panduan_Dosen(self):
        client = HTMLParser("its.ac.id", 443)

        with open(os.path.join(os.path.dirname(__file__), 'response.txt'), 'rb') as f:
            client.response = f.read().decode()

        client.separate_header()
        menu = client.get_menu()
        for item in menu:
            if 'Panduan Dosen' in item:
                is_exist = True
                break
        assert is_exist

    def test_Unduh_PDF(self):
        client = HTMLParser("its.ac.id", 443)

        with open(os.path.join(os.path.dirname(__file__), 'response.txt'), 'rb') as f:
            client.response = f.read().decode()

        client.separate_header()
        menu = client.get_menu()
        for item in menu:
            if 'Unduh PDF' in item:
                is_exist = True
                break
        assert is_exist

    def test_video_async(self):
        client = HTMLParser("its.ac.id", 443)

        with open(os.path.join(os.path.dirname(__file__), 'response.txt'), 'rb') as f:
            client.response = f.read().decode()

        client.separate_header()
        menu = client.get_menu()
        for item in menu:
            if '[Video] Panduan Membuat Video Asinkronus dengan Power Point' in item:
                is_exist = True
                break
        assert is_exist

    def test_panduan_mahasiswa(self):
        client = HTMLParser("its.ac.id", 443)

        with open(os.path.join(os.path.dirname(__file__), 'response.txt'), 'rb') as f:
            client.response = f.read().decode()

        client.separate_header()
        menu = client.get_menu()
        for item in menu:
            if 'Panduan Mahasiswa' in item:
                is_exist = True
                break
        assert is_exist
