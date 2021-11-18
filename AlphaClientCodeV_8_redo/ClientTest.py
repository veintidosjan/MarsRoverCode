import socket
import time
from datetime import date, datetime

roverSocket = socket.socket()
host = "192.168.1.93"
port = 5558
roverSocket.connect((host,port))

connected = True

def sendData(message):
    roverSocket.send(message.encode())
    data = ""
    data = roverSocket.recv(1024).decode()
    print("Server sent :", data)

while True:
    try:
        data = input("Enter the data: ")
        sendData(data)
    except socket.error:
        # reconnect to the server here
        connected = False
        roverSocket = socket.socket()
        print("connection lost... reconnecting")
        while not connected:
            #attempt to reconnect, otherwise sleep for 2 seconds
            try:
                roverSocket.connect((host,port))
                connected = True
                print("reconnection successful")
            except socket.error:
                time.sleep(2)
    
roverSocket.close()
