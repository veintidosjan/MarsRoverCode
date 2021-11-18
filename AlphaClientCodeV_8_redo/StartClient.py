from picamera import PiCamera
from time import sleep, strftime
import socket
import tqdm
import os
import threading
import datetime
from ClientSensors import GPS_Temp_Hum_Run
from ClientMovement import runMotors

#this part of the code will create the socket for comms
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


host = "192.168.0.15"
port2 = 5555
clientSocket.connect((host,port2))



def cameraLocalSave(clientFileName):
    with PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.start_preview()
        # Camera warm-up time
        sleep(2)
        # tells the camera where to store the file and the file name
        camera.capture(clientFileName)
            
def sendClientPhotos(filename, filesize):
    SEPARATOR = '<SEPARATOR>'
    # Send 500000 bytes each time
    BUFFER_SIZE = 20000
    # encode() function encodes the string to 'utf-8' for sending to server
    print('Let me be seen')
    print('filename: ' + str(filename))
    print('filesize: ' + str(filesize))
    print(SEPARATOR)
    clientSocket.send(f"{filename}{SEPARATOR}{filesize}".encode())
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    sleep(2)
    with open(filename, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            
            # we use sendall to assure transmission in busy networks
            clientSocket.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))
    print('made it out of sendFile loop')
            
def runProgram():
    i=0
    clientMovementThread = threading.Thread(target=runMotors)
    clientMovementThread.start()
    
    sensorsDataForClient = threading.Thread(target=GPS_Temp_Hum_Run)
    sensorsDataForClient.start()
    
    
    while True:
        filename = '/home/pi/clientPhotos/AlphaImage' + strftime('%Y%m%d-%H%M%S') + '.jpg'
        cameraLocalSave(filename)
        # get the file size 
        filesize = os.path.getsize(filename)
        #print('original file size: ' + str(filesize))
        print('let me also be seen')
        sendClientPhotos(filename, filesize)
        i+=1
        sleep(5)
        #clientSocket.close()      
            

def recordVideo():
    #make the Picamera a usable object
    camera = PiCamera()
    print("Camera is starting and will record the next ten seconds")
    camera.start_preview()
    #the path can be set inside of the () of recording
    camera.start_recording('/home/pi/Desktop/videoTestFile.h264')
    sleep(9)
    camera.stop_recording()


    
    
runProgram()
# close the socket
clientSocket.close()
