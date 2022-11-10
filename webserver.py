import os
from socket import *
import myhttp as http

HOST = "127.0.0.1"
PORT = 10420

def main():
    # create TCP welcoming socket
    with socket(AF_INET, SOCK_STREAM) as serverSocket:
        serverSocket.bind((HOST, PORT))
        serverSocket.listen(1)
        print("The server is ready to receive")

        while True:
            # wait for client contact, then open new socket
            connectionSocket, _ = serverSocket.accept()
            with connectionSocket:
                data = connectionSocket.recv(2048)
                if data:
                    # read request
                    request = http.request()
                    request.parse(data)
                    isHEAD = request.method == "HEAD"

                    print("Received request:")
                    print(request.toString())

                    response = http.response()
                    # add body if file exists, else 404
                    # do not add body if HEAD request
                    if os.path.exists("." + request.uri):
                        response.addMessage("." + request.uri, isHEAD)
                        response.setStatus(200)
                    else:
                        response.addMessage("./error/notFound.html", isHEAD)
                        response.setStatus(404)
                    
                    print("Sent response:")
                    print(response.toString())
                    
                    connectionSocket.send(response.toString().encode())
                    # connection closed after single request

if __name__ == "__main__":
    main()

