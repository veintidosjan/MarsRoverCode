from __future__ import print_function
from time import sleep
from dual_g2_hpmd_rpi import motors, MAX_SPEED
import random
import signal
import math
from berryIMU import compass
import random

#############################################################
# Define a custom exception to raise if a fault is detected.
class DriverFault(Exception):
    def __init__(self, driver_num):
        self.driver_num = driver_num

def keyboardInterruptHandler(signal, frame):
    motors.forceStop()
    sleep(2)
    
def runProgram(x1,y1,x2,y2):
    #starting point
    print('x1: ' + str(x1))
    print('y1: ' + str(y1))
    print('x2: ' + str(x2))
    print('y2: ' + str(y2))
    #jan Commented this out 
    boundary = 2
    #this will be the actual distance we use instead of random values
    distance = int(calculateDistance(x1, y1, x2, y2)) 
    print('rounded distance: ' + str(distance))
    
    #this distance is for testing purposes (random distance generator)
    #distance = randomValueX()
    
    if (distance < boundary):
        print('Rover is inside the boundary.')
        r = random.randrange(1,5)
        print('r: ' + str(r))
        if r == 1:
            unitforward()
            sleep(1)
            alignNorth()
            sleep(1)
            y2+=1
            return x1,y1,x2,y2
        if r == 2:
            rotateLeft()
            sleep(1)
            unitforward()
            sleep(1)
            alignNorth()
            sleep(1)
            x2-=1
            return x1,y1,x2,y2
        if r == 3:
            rotateRight()
            sleep(1)
            unitforward()
            sleep(1)
            alignNorth()
            sleep(1)
            x2+=1
            return x1,y1,x2,y2
        if r == 4:
            unitback()
            sleep(1)
            alignNorth()
            sleep(1)
            y2-=1
            return x1,y1,x2,y2
        sleep(2)
            
    if (distance >= boundary):
        print('Out of bounds. Turning until facing North.')
        alignNorth()
        sleep(2)
        print('Rover is facing North. Calculating path back to starting point.')
        calculateRotationAngle(x1, y1, x2, y2, distance)
        print('Rover is at starting point.')
        sleep(2)
        alignNorth()
        
    
def calculateDistance(x1, y1, x2, y2):
    #calculating distance of the rover from center location
    distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    print('distance: ' + str(distance))
    return int(distance)

def calculateRotationAngle(x1, y1, x2, y2, distance):
    #calculate theta from two co-ordinates
    thetaRad = (math.atan((y2-y1)/(x2-x1)))
    thetaDegree = 180 * thetaRad/math.pi
    print ('thetaDegree: ' + str(thetaDegree))
    
    #determine the quadrant with respect to
    #the starting point of the rover.
    deltaY = y2-y1
    deltaX = x2-x1
    print ('deltaY: ' + str(deltaY), 'deltaX: ' + str(deltaX))
    
    #First Quadrant
    if deltaX > 0 and deltaY > 0:
                theta = 90 + thetaDegree
                print('first quadrant: ' + str(theta))
                rotateLeftforCenter(theta)
                print('distance: ' + str(distance))
                forward(distance)
    #Second Quadrant
    if deltaX < 0 and deltaY > 0:
                theta = 90 - thetaDegree
                print('second quadrant: ' + str(theta))
                rotateRightforCenter(theta)
                forward(distance)
    #Third Quadrant
    if deltaX < 0 and deltaY < 0:
                theta = 90 - thetaDegree
                print('third quadrant: ' + str(theta))
                rotateRightforCenter(theta)
                forward(distance)

    #Fourth Quadrant
    if deltaX > 0 and deltaY < 0:
                theta = 90 + thetaDegree
                print('fourth quadrant: ' + str(theta))
                rotateLeftforCenter(theta)
                forward(distance)


#Functions for when inside the boundary:
###################################################################################################
#move forward one unit while inside boundary    
def unitforward():
    for i in range(1):
        motors.setSpeeds(280,280)
        raiseIfFault()
        sleep(.5)
        #once out of the loop kill the motor
        motorSleep()
        print('unitforward')
        
#move back one unit while inside boundary    
def unitback():
    for i in range(1):
        motors.setSpeeds(-200,-200)
        raiseIfFault()
        sleep(1)
        #once out of the loop kill the motor
        motorSleep()
        print('unitback')

def rotateLeft():
    while compass() not in range(265, 275):
        print('rotate left to 270 degrees')
        motors.setSpeeds(-330,330)
        raiseIfFault()
        sleep(.1)
        #jump out of the loop and shut down    
    motorSleep()
        
def rotateRight():
    while compass() not in range(85, 95):
        print('rotate right to 90 degrees')
        motors.setSpeeds(330,-330)
        raiseIfFault()
        sleep(.1)
        #jump out of the loop and shut down    
    motorSleep()
        
#make sure rover is facing north after each unit movement inside the boundary      
def alignNorth():
    compassAngle = compass()
    print('compassAngle: ' + str(compassAngle))
    if compassAngle >= 5 and compassAngle <= 180:
        rotateLeftforNorth()
    if compassAngle > 180 and compassAngle < 355:
        rotateRightforNorth()


#Functions for when outside of the boundary:
#########################################################################################################

def rotateLeftforNorth():
    while compass() not in range(350, 360):
        print('rotate left to north')
        motors.setSpeeds(-330,330)
        raiseIfFault()
        sleep(.1)
    #jump out of the loop and shut down    
    motorSleep()
 
def rotateRightforNorth():
    while compass() not in range(350,360):
        print('rotate right to north')
        motors.setSpeeds(330,-330)
        raiseIfFault()
        sleep(.1)
    #jump out of the loop and shut down
    motorSleep()

    
# function to turn left or to turn counter clockwise 
def rotateLeftforCenter(theta):
    while compass() not in range(round(theta) - 5, round(theta) + 5):
        print('rotate left to ' + str(theta) + ' degrees')
        motors.setSpeeds(-330,330)
        raiseIfFault()
        sleep(.1)
    #jump out the loop and kill the motors
    motorSleep()
        
# function to turn right or to turn clockwise
def rotateRightforCenter(theta):
    print('rotate right')
    while compass() not in range(round(theta) - 5, round(theta) + 5):
        print('rotate right to ' + str(theta) + ' degrees')
        motors.setSpeeds(330,-330)
        raiseIfFault()
        sleep(.1)
    #jump out of the loop and kill the motors
    motorSleep()

#function to move rover forward back to starting point
def forward(distance):
    for i in range(distance):
        motors.setSpeeds(280,280)
        raiseIfFault()
        sleep(.5)
    #once out of the loop kill the motor
        motorSleep()

####################################################################################################
 
 
 
#shuts down the motors 
def motorSleep():
    motors.setSpeeds(0,0)
    raiseIfFault()
    sleep(0.5)

def raiseIfFault():
    if motors.motor1.getFault():
        raise DriverFault(1)
    if motors.motor2.getFault():
        raise DriverFault(2)

        
#############################################################        
     
def runMotors():
    x1 = 5
    y1 = 5
    x2 = 5
    y2 = 5
    while True:
        x1, y1, x2, y2 = runProgram(x1,y1,x2,y2)
        print(x1, y1, x2, y2)
        sleep(10)

   
#runMotors()
                   