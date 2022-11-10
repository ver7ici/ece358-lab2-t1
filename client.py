from socket import *
import myhttp as http

HOST = "127.0.0.1"
PORT = 10420

def makeRequest(method, uri):
    with socket(AF_INET, SOCK_STREAM) as clientSocket:
        clientSocket.connect((HOST, PORT))
        request = http.request(method, HOST, PORT, uri)
        clientSocket.send(request.toString().encode())

        print("Sent request:")
        print(request.toString())

        response = clientSocket.recv(2048).decode()

        print("Received response:")
        print(response)

def main():
    makeRequest("HEAD", "/index.html")
    makeRequest("HEAD", "/not.exist")

if __name__ == "__main__":
    main()