import os
import socket
import select
import sys


BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class HTTPServer:
    def __init__(self, host, port):
        self.server_socket = None
        self.host = host
        self.port = port

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        input_socket = [self.server_socket]
        output_socket = []

        try:
            while True:
                read_ready, write_ready, exception = select.select(input_socket, output_socket, input_socket)

                for sock in read_ready:
                    if sock == self.server_socket:
                        conn, addr = sock.accept()
                        input_socket.append(conn)

                    else:
                        data = sock.recv(4096)
                        data = data.decode('utf-8')
                        
                        request_header = data.split('\r\n')
                        if request_header[0] == '':
                            sock.close()
                            input_socket.remove(sock)
                            continue

                        request_file = request_header[0].split()[1]
                        response_header = b''
                        response_data = b''


                        # ATTENTION: PLEASE DO NOT CHANGE CODE BELOW THIS LINE
                        if '/exit' in data:
                            sock.sendall(b'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n')
                            return
                        # ATTENTION: PLEASE DO NOT CHANGE CODE ABOVE THIS LINE


                        # this is a special case, where the server should return the index.html file
                        if request_file == 'index.html' or request_file == '/' or request_file == '/index.html':
                            f = open(os.path.join(BASE_DIR, 'index.html'), 'rb')
                            response_data = f.read()
                            f.close()

                            content_length = len(response_data)
                            response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' \
                                            + str(content_length) + '\r\n\r\n'

                            # send response header and data
                            sock.sendall(response_header.encode('utf-8') + response_data)

                        else:
                            # check request file
                            file_path = BASE_DIR + request_file
                            # file_path = os.path.join(BASE_DIR, request_file)
                            if os.path.isdir(file_path):
                                # Show directory contents
                                dir_contents = os.listdir(file_path)
                                
                                response_data = '<html><body><ul>'

                                for item in dir_contents:
                                    response_data += f'<li><a href="{request_file}/{item}">{item}</a></li>'
                                response_data += '</ul></body></html>'

                                content_len = len(response_data)
                                response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' \
                                            + str(content_len) + '\r\n\r\n'
                                sock.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))

                            elif os.path.exists(file_path):
                                if file_path.endswith('.html'):
                                    # Read html file and send to client
                                    with open(file_path, 'rb') as f:
                                        response_data = f.read()
                                    content_len = len(response_data)
                                    response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' \
                                            + str(content_len) + '\r\n\r\n'
                                    sock.sendall(response_header.encode('utf-8') + response_data)

                                else:
                                    # Read other file types and send to client as download
                                    with open(file_path, 'rb') as f:
                                        response_data = f.read()
                                    content_len = len(response_data)
                                    response_header = 'HTTP/1.1 200 OK\r\nContent-Dispotition: attachment; filename="' + \
                                            os.path.basename(file_path) + \
                                            '"\r\nContent-Type: application/octet-stream\r\nContent-Length:' \
                                            + str(content_len) + '\r\n\r\n'
                                    sock.sendall(response_header.encode('utf-8') + response_data)
                            else:
                                # Return 404
                                f = open(os.path.join(BASE_DIR, '404.html'), 'rb')
                                response_data = f.read()
                                f.close()

                                content_length = len(response_data)
                                response_header = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' \
                                    + str(content_length) + '\r\n\r\n'

                                # send response header and data
                                sock.sendall(response_header.encode('utf-8') + response_data)

                for sock in exception:
                    input_socket.remove(sock)
                    if sock in output_socket:
                        output_socket.remove(sock)
                    sock.close()

        except KeyboardInterrupt:
            self.server_socket.close()
            sys.exit(0)

    def stop(self):
        print("Shutting down server...")
        self.server_socket.close()
        sys.exit(0)

if __name__ == '__main__':
    # TODO: Parse and set the host and port from the config file
    conf_path = os.path.join(BASE_DIR, 'httpserver.conf')
    with open(conf_path) as config_file:
        config = dict(line.strip().split('=') for line in config_file)

    HOST = config.get("HOST")
    PORT = int(config.get("PORT", 8080))

    server = HTTPServer(HOST, PORT)
    server.start()
    server.stop()
