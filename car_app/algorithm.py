#Local imports
from bt         import * 
from gpio_setup import *

import time
import numpy as np
import math

timeList = []
xList = []
yList = []

carSpeed = 58 #cm
calibratedDistance = 15
secondPress = False
time_initial = None
pushes = 0

Ri_min = 35
Re_min = 64.7
L_min  = 62.4
e = 26
p = 8
w = 20
'''
Rmin_bar = Ri_min + w/2

x_C1 = x_carLeft + p
y_C1 = Rmin_bar + w/2

x_t  = y_C1 + sqrt(Rmin_bar - (y_t - y_C1)**2)
y_t  = (y_C1 + y_C2)/2

x_C2 = x_s
y_C2 = y_i - Rmin_bar

x_s = 2*x_t - x_C1
y_s = y_i
'''
def advanceCar(distance):
    print("moving forward", distance)
    
    time_to_move = distance / carSpeed
    print("time to move: ", time_to_move)
    initial_time = time.time()
    
    moveForward()
    while ((time.time() - initial_time) < time_to_move):
        last_time = time.time()
    moveBrake(True)
    print ("Moved for time:", last_time-initial_time)
    

def isAproxEqual(distanceRef, distance):
    if(distance < distanceRef * 1.1 and distance > distanceRef * 0.9):
        return True
    else:
        return False

def areLastElementsEq():
    if (len (yList) > 3):
        if (isAproxEqual(yList[-1], yList[-2]) and isAproxEqual(yList[-1], yList[-3])):
            return True
        else:
            return False
    else:
        return False
def findParkingSpot(calibrationDistance):
    #time.sleep(0.050)
    
    firstEdge = False
    secondEdge = False
    emptyDistance = None

    time_initial = time.time()
    iteration = 0
    firstEdgeIndex = None
    secondEdgeIndex = None
    
    moveForward()
    
    while True:
        
        '''
        if isPressed() or distanceFront < 10:
            secondPress = not secondPress
            moveNeutral()
            break
        '''    
        #distanceFront = read_sensor('front')
        #distanceBack  = read_sensor('back')
        distanceRight = read_sensor('right')
        
        time_current = time.time() - time_initial
        
        xList.append(time_current*carSpeed)
        yList.append(distanceRight)
        timeList.append(time_current)
        
        #check if the car hasn't passed the first parked car
        if( not distanceRight < calibratedDistance and firstEdge == False and areLastElementsEq()):
            firstEdge = True
            print ("First edge detected")
            emptyDistance = distanceRight
            #print (yList)
            firstEdgeIndex = iteration
            print("Second edge iteration is ", iteration)
            print("First edge time is ", timeList[iteration])
            
        
        if ( firstEdge and distanceRight < calibratedDistance and areLastElementsEq()):
            secondEdge = True
            print ("Second edge detected")
            moveBackward()
            time.sleep(0.2)
            moveNeutral()
            print ("Second edge time is ", timeList[iteration])
            print("Second edge iteration is ", iteration)
            secondEdgeIndex = iteration
            print ("Parking spot length is  ", carSpeed * (timeList[secondEdgeIndex] - timeList[firstEdgeIndex]))
            
            #calculate the numerical derivative of the lateral measurement
            derivative = np.diff(yList)/np.diff(xList)
            
            ind_MAX = np.argmax(derivative)
            ind_MIN = np.argmin(derivative)
            
            print ("Derivative length is ", xList[ind_MIN] - xList[ind_MAX])
            
            return
       
        iteration += 1
       
def buttonCallback(self):
    
    global pushes
    
    print("Button push detected")
    print("Mode selected:", pushes)
    calibrationDistance = read_sensor('right')
    
    time.sleep(2)
    
    if (pushes == 0):
        findParkingSpot(calibrationDistance)
    elif (pushes == 1):
        advanceCar (40)
        
    print("Callback ended, exiting subroutine")
    pushes += 1
    pushes = pushes % 2
    moveNeutral()
    return 
     

    #close the Bluetooth socket
    

try:
    gpioInit(buttonCallback)
    #create Bluetooth sockets and establish connection
    #socketRight, socketFront, socketBack = connectBluetooth()
    
    #print (isAproxEqual(1,0.9))

    
    while True:
        time.sleep(10)

finally:
    print('Application is ending!')
    #disconnectBluetooth()
    GPIO.cleanup()
