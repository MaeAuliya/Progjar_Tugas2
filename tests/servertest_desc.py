from mocket import mocketize
import requests
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
SERVER_DIR = os.path.join(os.path.dirname(BASE_DIR), 'src/server')

with open(os.path.join(SERVER_DIR, 'httpserver.conf')) as config_file:
    config = dict(line.strip().split('=') for line in config_file)

HOST = config.get("HOST")
PORT = int(config.get("PORT", 8080))


@mocketize
def test_code_200():
    r = requests.get(f"http://{HOST}:{PORT}/index.html")
    assert r.reason == "OK"


@mocketize
def test_code_200_2():
    r = requests.get(f"http://{HOST}:{PORT}/dataset")
    assert r.reason == "OK"


@mocketize
def test_code_200_3():
    r = requests.get(f"http://{HOST}:{PORT}/dataset/729.txt")
    assert r.reason == "OK"


@mocketize
def test_code_404():
    r = requests.get(f"http://{HOST}:{PORT}/non_existence.html")
    assert r.reason == "Not Found"


@mocketize
def test_code_404_2():
    r = requests.get(f"http://{HOST}:{PORT}/not_exist")
    assert r.reason == "Not Found"

@mocketize
def test_shutdown_server():
    r = requests.get(f"http://{HOST}:{PORT}/exit")
    assert r.status_code == 200
