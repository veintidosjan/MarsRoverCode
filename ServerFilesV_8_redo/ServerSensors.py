import RPi.GPIO as GPIO
import dht11
import datetime
import serial               #import serial pacakge
from time import sleep
import webbrowser           #import package for opening link in browser
import sys                  #import system package
import signal
import sqlite3

#initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

#read data using pin 6 / bcm17
instance = dht11.DHT11(pin=27)

#signal.signal(signal.SIGINT, keyboardInterruptHandler)

#def keyboardInterruptHandler():
    #motors.forceStop()

def GPS_Info():
    global NMEA_buff
    global lat_in_degrees
    global long_in_degrees
    nmea_time = []
    nmea_latitude = [] 
    nmea_longitude = []
    nmea_time = NMEA_buff[0]                    #extract time from GPGGA string
    nmea_latitude = NMEA_buff[1]                #extract latitude from GPGGA string
    nmea_longitude = NMEA_buff[3]               #extract longitude from GPGGA string
    
    lat = float(nmea_latitude)                  #convert string into float for calculation
    longi = float(nmea_longitude)               #convertr string into float for calculation

    lat_in_degrees = convert_to_degrees(lat)    #get latitude in degree decimal format
    long_in_degrees = convert_to_degrees(longi) #get longitude in degree decimal format

#convert raw NMEA string into degree decimal format   
def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = "%.7f" %(position)
    return position
    
gpgga_info = "$GPGGA,"
ser = serial.Serial ("/dev/ttyAMA0")              #Open port with baud rate
GPGGA_buffer = 0
NMEA_buff = 0
lat_in_degrees = 0
long_in_degrees = 0



def GPS_Temp_Hum_Run():
    print('GPS_run has been accessed')
    count = 0
    gpsFlag = 0 #false when 0 True when 1

    try:
        
        #create the connection....if DB doesn't exist, it will create the DB
        db = sqlite3.connect('ServerData.db')

        #prepare a cursor obj using cursor() method
        c = db.cursor()

        #create the table
        c.execute('''CREATE TABLE IF NOT EXISTS dhtreadings(id INTEGER PRIMARY KEY, currentdate TEXT, temperature REAL, humidity REAL, lat REAL, long REAl)''')
        db.commit()

        while True:
            #for reading GPS data
            global GPGGA_buffer
            global NMEA_buff
            global gpgga_info
            global lat_in_degrees
            global long_in_degrees
            
            received_data = (str)(ser.readline())                   #read NMEA string received
            GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string 
                                                
            if (GPGGA_data_available>=0):
                
                GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string 
                NMEA_buff = (GPGGA_buffer.split(','))               #store comma separated data in buffer
                GPS_Info()                                          #get time, latitude, longitude

                #Convert to negative if longitude is W & latitude is S
                if(NMEA_buff[4] == "W"):
                    long_in_degrees = -1 * float(long_in_degrees)
                else:
                    long_in_degrees = float(long_in_degrees)
                if (NMEA_buff[2] == "S"):
                    lat_in_degrees = -1 * float(lat_in_degrees)
                else:
                    lat_in_degrees = float(lat_in_degrees)
                
                lastLat = lat_in_degrees
                lastLong = long_in_degrees
                
                
                #print("Latitude", lastLat, "Longitude", lastLong)
                
                #for reading tem/hum
                result = instance.read()
                if result.is_valid():
                    lastRecordedDate = str(datetime.datetime.now())
                    lastRecordedTemp = "%-3.1f C" % result.temperature
                    lastRecordedHum = "%-3.1f %%" % result.humidity
                    gpsFlag = 1
          
            
            if gpsFlag == 1:
                #execute the SQL statement
                c.execute('''INSERT INTO dhtreadings(currentDate, temperature, humidity, lat,long) values(?, ?, ?,?,?)''', (lastRecordedDate,lastRecordedTemp,lastRecordedHum,lastLat,lastLong))

                #commit changes in the database
                db.commit()
                
                gpsFlag = 0
                sleep(1)
                
    except ValueError as e:
        while e == e:
            print("no signal")
            sleep(1.00)
            continue

    
#GPS_Temp_Hum_Run()