from socket import *
import threading

serverIP = input("Enter IP address: ")
serverPort = eval(input("Enter port number: "))

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverIP, serverPort))

userID = input("Enter your ID: ")
clientSocket.send(userID.encode())

def receive():
    while True:
        msg = clientSocket.recv(1024).decode()
        if msg == "/q":
            clientSocket.close()
            break
        print(msg)

t = threading.Thread(target = receive, args = ())
t.start()

while True:
    msg = input("")
    clientSocket.send(msg.encode())
    if msg == "/q":
        break
