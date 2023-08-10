import os
import socket
import sys
import ssl
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class HTMLParser:
    # TODO:
    # 1. Assign semua value yang diperlukan
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.response = ''
        self.header = ''
        self.content = ''

    def connect(self):
        # 2. Connect socket
        self.socket.connect((self.host, self.port))
        

    def SSL(self):
        # 3. Connect SSL
        context = ssl.create_default_context()
        self.socket = context.wrap_socket(self.socket, server_hostname=self.host)

    def separate_header(self):
        # 4. Pisahkan header dan content
        self.header = self.response.split('<!DOCTYPE', maxsplit=1)[0]
        self.content = self.response.split('<!DOCTYPE', maxsplit=1)[1]

    def send_message(self, message):
        # 5. Kirim message dan terima response
        self.socket.send(f"GET / HTTP/1.1\r\nHost:{self.host}\r\n\r\n".encode())
        while True:
            data = self.socket.recv(4096)
            self.response += data.decode('utf-8')
            if not data:
                self.socket.close()
                break
        self.separate_header()
    
    def get_status_code(self):
        # 6. Ambil status code
        return self.header.split("\n", 1)[0].split(maxsplit=1)[1]
    
    def get_content_encoding(self):
        # 7. Ambil content encoding
        partition_header = self.header.split("\n")
        con_encoding = list(filter(lambda a: 'Content-Encoding' in a, partition_header))[0]
        con_encoding = con_encoding.split()[1]

        return con_encoding
    
    def get_http_version(self):
        # 8. Ambil http version
        return self.header.split("\n", 1)[0].split(maxsplit=1)[0]
    
    def get_charset(self):
        # 9. Ambil charset
        partition_header = self.header.split("\n")
        charset = list(filter(lambda a: 'charset' in a, partition_header))[0].split()[2]
        charset = charset.split("=",1)[1]

        return charset
    
    def get_menu(self):
        res = []

        doc = BeautifulSoup(self.response, "html.parser")
        masuk_ul = doc.find("ul", {"class": "navbar-nav h-100 wdm-custom-menus links"})
        try:
            list_li = masuk_ul.find_all('li')
            for menu in list_li:
                panduan = menu.find('a')
                if panduan:
                    res.append(panduan.text.strip())
                masuk_div = menu.find('div')
                dropdown = masuk_div.find_all('a')
                for dropDown in dropdown:
                    res.append('\t' + dropDown.text.strip())
        except AttributeError:
            pass

        return res

    def disconnect(self):
        self.socket.close()


if __name__ == "__main__":
    client = HTMLParser("classroom.its.ac.id", 443)
    client.connect()
    client.SSL()

    client.send_message(f"GET / HTTP/1.1\r\nHost: {client.host}\r\n\r\n")
    print(client.get_status_code())
    print(client.get_content_encoding())
    print(client.get_http_version())
    print(client.get_charset())
    print(client.get_menu())
