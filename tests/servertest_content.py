from mocket import mocketize
import unittest
import os
import requests

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
SERVER_DIR = os.path.join(os.path.dirname(BASE_DIR), 'src/server')

with open(os.path.join(SERVER_DIR, 'httpserver.conf')) as config_file:
    config = dict(line.strip().split('=') for line in config_file)

HOST = config.get("HOST")
PORT = int(config.get("PORT", 8080))


@mocketize
def test_index():
    r = requests.get(f"http://{HOST}:{PORT}/index.html")
    with open(os.path.join(SERVER_DIR, 'index.html'), 'rb') as f:
        assert r.content == f.read()


@mocketize
def test_dataset():
    r = requests.get(f"http://{HOST}:{PORT}/dataset")
    assert "<li><a href=" in r.content.decode('utf-8')


@mocketize
def test_file():
    r = requests.get(f"http://{HOST}:{PORT}/dataset/729.txt")
    with open(os.path.join(SERVER_DIR, 'dataset', '729.txt'), 'rb') as f:
        assert r.content == f.read()


@mocketize
def test_not_found():
    r = requests.get(f"http://{HOST}:{PORT}/non_existence.html")
    with open(os.path.join(SERVER_DIR, '404.html'), 'rb') as f:
        assert r.content == f.read()


@mocketize
def test_not_found_2():
    r = requests.get(f"http://{HOST}:{PORT}/not_exist")
    with open(os.path.join(SERVER_DIR, '404.html'), 'rb') as f:
        assert r.content == f.read()


@mocketize
def test_shutdown_server():
    r = requests.get(f"http://{HOST}:{PORT}/exit")
    assert r.status_code == 200
