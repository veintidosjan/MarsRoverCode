from ClientThreadBuilder import createSocketThread
from CameraThreadBuilder import CameraThreadBuilder

import socket
from threading import *
import threading
#from socketserver import ThreadingMixIn
import signal
from time import sleep
import datetime
from ServerSensors import GPS_Temp_Hum_Run
from serverCamera import cameraLocalSave
from ServerMovement import runMotors


#setting up server connection
serversocket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#host = socket.gethostbyname(socket.gethostname())
host = '0.0.0.0'
#host = '192.168.0.9'
port1 = 5554
port2 = 5555

#error checking to make sure that the socket actually binded to the address
try:
    serversocket1.bind((host,port1))
    serversocket2.bind((host,port2))

except socket.error as e:
    print(str(e))

# When ctl+c is pressed, the server will immediately jump to this function.
# The purpose of this function will be to manually disconnect a client from the server.
def keyboardInterruptHandler(signal, frame):
    pass

#this function will be used to start the communications for the server/client
def serverComms():    
    #Starting messages
    print("The Rover Server is Starting:......")
    print("The Host IP is: " + host)
    #print("Port that is listening: " + str(port))
    print(socket.gethostname())
    
    #this is listening for the clients to connect 
    threads = []
    #This loop will use the class to build the threading for the rover
    # --Note: need to create additional statement to address if connection fails
    while True:
        serversocket1.listen()
        print("First Thread is working")
        clientsocket,address = serversocket1.accept()
         
        print('active threads: ' + str(active_count()))

        newThread = createSocketThread(clientsocket,address)
        newThread.start()
        threads.append(newThread)
        print(threads)
        
    #important need to close files!!
    for t in threads:
        print('hello there World')
        t.join()
        print(t)
    #serversocket.close()

def serverCommsDos():    
    #Starting messages
    print("The second socket is Starting:......")
    print("The Host IP is: " + host)
    #print("Port that is listening: " + str(port))
    print(socket.gethostname())
    
    #this is listening for the clients to connect 
    threads = []
    #This loop will use the class to build the threading for the rover
    # --Note: need to create additional statement to address if connection fails
    while True:
        serversocket2.listen()
        print("Second Thread is working")
        clientsocket,address = serversocket2.accept()
         
        print('active threads: ' + str(active_count()))

        newThread2 = CameraThreadBuilder(clientsocket,address)
        newThread2.start()
        threads.append(newThread2)
        print(threads)
        
    #important need to close files!!
    for t in threads:
        print('hello there World')
        t.join()
        print(t)
    #serversocket.close()


    
#function that starts the camera
def serverCamera():
    cameraLocalSave()
    pass

#function that calls the sensor data for the rover 
def sensorsForServer():
    GPS_Temp_Hum_Run()
    #pass


#function to handle
def main():
    print("Program is starting....")
    print("Threads will be active after this message")

    communicationThread = threading.Thread(target=serverComms)
    communicationThread.start()
    
    communicationThread2 = threading.Thread(target=serverCommsDos)
    communicationThread2.start()

    sensorsDataForServer = threading.Thread(target=sensorsForServer)
    sensorsDataForServer.start()
    

    cameraStreamingThread = threading.Thread(target=serverCamera)
    cameraStreamingThread.start()
    
    serverMovementThread = threading.Thread(target=runMotors)
    serverMovementThread.start()
        
    
    signal.signal(signal.SIGINT, keyboardInterruptHandler)
    
main()
