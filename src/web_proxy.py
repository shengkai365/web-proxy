import socket
import time
import sys
import getopt
import select

class WebProxy(object):
    def __init__(self, host, port, server_host, server_port=80):
        '''
        initailising the web proxy
        host: proxy listen address
        port: proxy listen port
        server_host: target host domain name or address
        server_port: target host port, defualt is 80
        '''
        self.proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.proxy_socket.bind((host, port))
        self.proxy_socket.listen()
        self.proxy_host = host
        self.proxy_port = port
        self.server_host = server_host
        self.server_port = server_port

        self.client_info = self.proxy_host + ':' + str(self.proxy_port)
        self.server_info = self.server_host + ':' + str(self.server_port)
        self.text_changes = 0
        self.link_rewrite = 0

        
    def start(self):
        '''
        Main logic, listens and handles the proxy process
        return: None
        '''
        while True:
            client_socket, server_socket = self.get_client_socket(), self.get_server_socket()
            
            self.data_transfer(client_socket, server_socket)

    def get_client_socket(self):
        '''
        Get client connection socket
        return socket.socket
        '''
        client_socket, client_addr = self.proxy_socket.accept()
        print('timestamp of request:    ', time.time())
        return client_socket
    
    def get_server_socket(self):
        '''
        Get server-side connection socket
        return socket.socket
        '''
        family, sockettype, _, _, server_addr = socket.getaddrinfo(self.server_host, self.server_port)[0]
        server_socket = socket.socket(family, sockettype)
        server_socket.setblocking(0) 
        server_socket.settimeout(5)
        server_socket.connect(server_addr)
        return server_socket

    def get_client_request(self, client_socket):
    
        '''
        Obtaining and modifying client request data
        return -> Bytes
        '''
        request_data = client_socket.recv(4*1024).decode()
        idx = request_data.find('\r\n')
        print('client request:          ', request_data[:idx])
              
        
        request_data = request_data.replace(self.client_info, self.server_info)
        return request_data.encode()

    def request_to_server(self, client_socket, server_socket):
        '''
        Proxy side sends request to server side
        return: None
        '''
        request = self.get_client_request(client_socket)
        server_socket.send(request)
        
    def modify_html(self, data):
        '''
        Counting of links to html pages, modification of 'the'
        '''
        self.text_changes += data.count(b' the ')
        self.link_rewrite += data.count(b'href=')-data.count(b'href="http')

        return data.replace(b' the ', b' <b>eht</b> ')
    

    def data_transfer(self, client_socket, server_socket):
        '''
        Data exchange between client socket and server socket
        return None
        '''
        self.request_to_server(client_socket, server_socket)
        _rlist = [client_socket, server_socket]
        is_recv = True     # Availability of data to accept
        is_headers = True  # is it a request/response header
        is_html = False    # is it a html page
        while is_recv:
            try:
                rlist, _, elist = select.select(_rlist, [], [], 2)
                if elist:
                    break
                for tmp_socket in rlist:
                    is_recv = True
                    # receive data
                    data = tmp_socket.recv(4*1024)
                    if data == b'':
                        is_recv = False
                        continue
                    
                    # if state of socket_client is readable, current data received from the client
                    if tmp_socket is client_socket: 

                        server_socket.send(data)     # Sending client request data to the server

                    # if state of socket_server is readable, current data received from the server
                    elif tmp_socket is server_socket:
                        if is_headers:
                            is_headers = False
                            print('server status response:  ', data.decode().split("\r\n")[0][9:])

                            # check if the response is html
                            if b'Content-Type:' in data:
                                i = data.find(b'Content-Type:')
                                if b'html' in data[i:].split(b'\r\n')[0]:
                                    is_html = True
                        if is_html:
                            # if the response is html, modify the data
                            data = self.modify_html(data)

                        client_socket.send(data) # Sending server-side response data to the client    
            except Exception as e:
                break
            
        if is_html:
            print("count of text changes:   ", self.text_changes)
            print("count of link rewrites:  ", self.link_rewrite)
        client_socket.close()
        server_socket.close()


if __name__ == '__main__':
    
    host, port, server_host = '127.0.0.1', 12345, 'comp3310.ddns.net'
    
    opts, _ = getopt.getopt(sys.argv[1:], 'h:p:s:')

    for opt, arg in opts:
        if opt == '-h':
            host = arg
        elif opt == '-p':
            port = int(arg)
        elif opt == '-s':
            server_host = server_host
        else:
            print('input error, read the README.md first!')
            sys.exit()

    web_proxy = WebProxy(host, port, server_host)
    web_proxy.start()

