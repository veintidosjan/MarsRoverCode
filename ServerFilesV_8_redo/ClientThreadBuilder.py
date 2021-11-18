import socket
from threading import *
import threading
import datetime
import dht11
import RPi.GPIO as GPIO
import serial
from time import sleep
import sys
import sqlite3

class createSocketThread(Thread):
    #function that build the thread and identifies the rover name
    def __init__(self,socket,address):
        Thread.__init__(self)
        self.socket = socket
        self.address = address
        #self.start()
        
    # This function builds a dictionary of lists for each Mar k, which is used to extract to individual excel files
    def run(self):
        
        #create the connection....if DB doesn't exist, it will create the DB
        db = sqlite3.connect('ClientDataBase.db')

        #prepare a cursor obj using cursor() method
        c = db.cursor()

        #create the table
        c.execute('''CREATE TABLE IF NOT EXISTS dhtreadings(id INTEGER PRIMARY KEY, name TEXT, currentdate TEXT, temperature REAL, humidity REAL, lat REAL, long REAL)''')
        db.commit()
        
        #loop that will handle deciding which rover is who then dealing with the data
        while True:
            client_msg = self.socket.recv(1024).decode()
            print(client_msg)
            self.socket.send(b'Message was received.')
            
            #slpits the data by a comma then makes an array somehow 
            dataFromClientArray = client_msg.split(",")
                    
            #execute the SQL statement
            c.execute('''INSERT INTO dhtreadings(name,currentdate, temperature, humidity, lat,long) values(?, ?, ?,?,?,?)''', (dataFromClientArray[0],dataFromClientArray[1],dataFromClientArray[2],dataFromClientArray[3],dataFromClientArray[4],dataFromClientArray[5]))

            #commit changes in the database
            db.commit()
            
            
            
            #Pause to allow for reconnection with client if connection is lost
            sleep(2)   