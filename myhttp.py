import os
import platform
from datetime import datetime

DATEF = "%a, %d %b %Y %H:%M:%S GMT"

class request:
    def parse(self, b):
        lines = b.decode().split("\r\n")

        # parse request line
        # assume relative URI
        self.method, self.uri, self.version = [lines[0].split(" ")[i] for i in range(3)]

        # parse header lines
        self.headers = dict()
        for line in lines[1:]:
            if line:
                k, v = line.split(":", 1)
                self.headers.update({ k: v.strip() })

    def toString(self):
        string = " ".join([self.method, self.uri, self.version]) + "\r\n"
        for k, v in self.headers.items():
            string += (": ".join([k, v])) + "\r\n"
        string += "\r\n"
        return string

    def __init__(self, method="", host="127.0.0.1", port=80, uri="/", headers=dict()):
        self.headers = {
            "User-Agent": "Python/" + platform.python_version(),
            "Host": host + ":" + str(port),
            "Accept-Language": "en-us",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "Keep-Alive",
        }
        self.headers.update(headers)
        self.method = method
        self.uri = uri
        self.version = "HTTP/1.1"

class response:
    def addMessage(self, path, headersOnly=False):
        with open(path, "rb") as f:
            b = f.read()
            self.headers.update({
                "Content-Length": str(len(b)),
                "Content-Type": "text/html; charset=utf-8",
                "Last-Modified": datetime.fromtimestamp(os.path.getmtime(path)).strftime(DATEF),
            })
            if not headersOnly:
                self.body = b.decode()

    def setStatus(self, status):
        self.status = status
        if status == 200:
            self.reason = "OK"
        elif status == 404:
            self.reason = "Not Found"
        # other statuses not required

    def toString(self):
        string = " ".join([self.version, str(self.status), self.reason]) + "\r\n"
        for k, v in self.headers.items():
            string += ": ".join([k, v]) + "\r\n"
        string += "\r\n" + self.body
        return string

    def __init__(self):
        self.version = "HTTP/1.1"
        self.status = 500
        self.reason = "Internal Server Error"
        self.headers = {
            "Connection": "Closed",
            "Date": datetime.utcnow().strftime(DATEF),
            "Server": "Python/" + platform.python_version(),
        }
        self.body = ""