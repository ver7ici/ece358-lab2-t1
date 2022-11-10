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
        print("The server is ready to receive\n")

        while True:
            # wait for client contact, then open new socket
            connectionSocket, _ = serverSocket.accept()
            with connectionSocket:
                data = connectionSocket.recv(2048)
                if data:
                    # read request
                    request = http.request()
                    request.parse(data)

                    print("Received request:")
                    print(request.toString())

                    # assume only GET and HEAD requests
                    response = http.response()
                    response.addMessage("." + request.uri, request.method == "HEAD")
                    
                    print("Sent response:")
                    print(response.toString())
                    
                    connectionSocket.send(response.toString().encode())
                    # connection closed after single request

if __name__ == "__main__":
    main()

