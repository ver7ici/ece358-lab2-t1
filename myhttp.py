import os
import platform
from datetime import datetime

DATEF = "%a, %d %b %Y %H:%M:%S GMT"

class request:
    def parse(self, b):
        """parse HTTP request in bytes"""
        lines = b.decode().split("\r\n")

        # parse request line
        # assume relative URI
        self.method, self.uri, self.version = [lines[0].split(" ", 3)[i] for i in range(3)]

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
        """add file to body if file exists, otherwise add 404 body
        \n do not add body if HEAD request
        """
        try:
            if not path.endswith(".html"):
                # only support fetching html files
                raise PermissionError
            with open(path, "rb") as f:
                b = f.read()
                self.headers.update({
                    "Content-Length": str(len(b)), # length in bytes
                    "Content-Type": "text/html; charset=utf-8",
                    "Last-Modified": datetime.fromtimestamp(os.path.getmtime(path)).strftime(DATEF),
                })
                if not headersOnly:
                    self.body = b.decode()
                self.setStatus(200)
        except (PermissionError, FileNotFoundError):
            # FileNotFoundError when path doesn't exist
            # PermissionError when path cannot be opened (ex. points to a directory)
            self.addMessage("./notFound.html", headersOnly)
            self.setStatus(404)

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