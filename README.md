## An annoying web-proxy

### 1. Introduction

This is a simple web proxy implemented in Python that allows you to access the http page you need to access by typing the proxy address into your browser

### 2. Parameters

```
-h: specify the proxy host, the default is '127.0.0.1'
-p: specify the listening port of the proxy host, the default is 12345
-s: specify the server-side domain name or host, the default is 'comp3310.ddns.net'
```

### 3. How to use

#### 3.1 For proxy

using a standard Linux environment, open the terminal, run:

```bash
# defult parameters, proxy address: 127.0.0.1:12345
python web_proxy.py

# or run with your parameters
python web_proxy.py -h host -p port -s server_host
```



#### 3.2 For client

Open any browser and enter the host and port number of the proxy, such as `127.0.0.1:12345`