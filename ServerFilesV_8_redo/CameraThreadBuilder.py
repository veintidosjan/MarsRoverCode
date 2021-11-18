import socket
from threading import *
import threading
import datetime
from time import sleep
import tqdm
import os

class CameraThreadBuilder(Thread):
    #function that build the thread and identifies the rover name
    def __init__(self,socket,address):
        Thread.__init__(self)
        self.socket = socket
        self.address = address
        #self.start()
        
    # This function builds a dictionary of lists for each Mar k, which is used to extract to individual excel files
    def run(self):
        #loop that will handle deciding which rover is who then dealing with the data
        i=0
        BUFFER_SIZE = 20000
        SEPARATOR = '<SEPARATOR>'
        
        while True:
            
            # receive the file info (name and size)
            # receive using client socket, not server socket
            received = self.socket.recv(BUFFER_SIZE).decode()
            print(received)
            filename, filesize = received.split(SEPARATOR)
            
            # remove absolute path if there is one
            #filename = os.path.basename(filename)
            
            # convert to integer
            filesize = int(filesize)
            #start receiving the file from the socket and writing to the file stream
            #progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)

            with open(filename, "wb") as f:
                totalBytes = 0
                while True:
                    #print('filesize: ' + str(filesize))
                    # read 1024 bytes from the socket (receive)
                    bytes_read = self.socket.recv(BUFFER_SIZE)
                    totalBytes += len(bytes_read)
                    #print(totalBytes)
                    #print('bytes_read size: ' + str(len(bytes_read)))
                    #print('BUFFER_SIZE size: ' + str(BUFFER_SIZE))
                    # write to the file the bytes just received
                    f.write(bytes_read)
                    # update the progess bar
                    #progress.update(len(bytes_read))
                    if totalBytes == filesize:
                        print('Here I am')
                        # nothing is received
                        # file transmitting is done
                        break
                print('made it out of the loop')
            print('made it out of with statement')
            i+=1
