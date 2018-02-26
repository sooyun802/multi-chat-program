from socket import *
import threading

serverPort = eval(input("Enter port number: "))

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('localhost', serverPort))
serverSocket.listen(1000)
userList = []
print("\n--- The TCP server is ready to receive. ---\n")

def userInstance(user):
    while True:
        msg = user.getSocket().recv(1024).decode().split(' ', 1)
        if msg[0] == "/q":
            user.getSocket().send("/q".encode())
            user.getSocket().close()
            for tmp in userList:
                if tmp != user:
                    message = "\nUSER_ID [" + user.getId() + "] has exited.\n"
                    tmp.getSocket().send(message.encode())
            userList.remove(user)
            print('CURRENT NUMBER OF USERS:', len(userList), end="\n\n")
            break
        if(len(msg) == 1):
            msg.append("")
        user.messageHandle(msg[0], msg[1])


class User:
    def __init__(self, userSocket, id=""):
        self._userSocket = userSocket
        self._id = id

    def getSocket(self):
        return self._userSocket

    def getId(self):
        return self._id

    def messageHandle(self, userAction="", msg=""):
        if userAction == "/who":
            self.showCurrentUsers(msg)
        elif userAction == "/m":
            msg = msg.split(' ', 1)
            self.deliverMessage(msg[0], msg[1])
        elif userAction == "/b":
            self.broadcastMessage(msg)

    def showCurrentUsers(self, msg=""):
        message = "\n------- CURRENT USERS -------\n"
        for user in userList:
            message = message + " - " + user.getId() + "\n"
        self.getSocket().send(message.encode())

    def deliverMessage(self, id="", msg=""):
        userExists = 0
        for user in userList:
            if user.getId() == id:
                userExists = 1
                message = "\n[MESSAGE FROM: " + self.getId() + "]\n"
                message = message + msg + "\n"
                user.getSocket().send(message.encode())
        if userExists == 0:
            message = "\nUSER_ID [" + id + "] does not EXIST."
            self.getSocket().send(message.encode())

    def broadcastMessage(self, msg=""):
        message = "\n[MESSAGE FROM: " + self.getId() + "]\n"
        message = message + msg + "\n"
        for user in userList:
            if user != self:
                user.getSocket().send(message.encode())


while True:
    connectionSocket, addr = serverSocket.accept()
    clientId = connectionSocket.recv(1024).decode()
    newUser = User(connectionSocket, clientId)
    userList.append(newUser)
    print('CURRENT NUMBER OF USERS:', len(userList), end="\n\n")
    for user in userList:
        message = "\nUSER_ID [" + newUser.getId() + "] has entered.\n"
        user.getSocket().send(message.encode())
    t = threading.Thread(target = userInstance, args = (newUser,))
    t.start()

