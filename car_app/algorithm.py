#Local imports
from bt         import * 
from gpio_setup import *

import time
import numpy as np
import math
from math import sqrt


timeList = []
xList = []
yList = []

carSpeed = 46 #cm
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

Rmin_bar = Ri_min + w/2

parkingWidth = None
ind_MAX = None
ind_MIN = None

def getAngle(a, b, c):
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang + 360 if ang < 0 else ang


def advanceCar(distance, forward):
    print("moving forward", distance)
    
    time_to_move = distance / carSpeed
    print("time to move: ", time_to_move)
    initial_time = time.time()
    if forward:
        moveForward()
    else:
        moveBackward()
    while ((time.time() - initial_time) < time_to_move):
        last_time = time.time()
    moveBrake(True)
    print ("Moved for time:", last_time-initial_time)
    
def parkCar ():
    
    print("Distance to parking spot", parkingWidth)
    
    x_C1 = xList[ind_MAX] + p
    y_C1 = Rmin_bar + w/2
    
    y_s = parkingWidth
    y_C2 = y_s - Rmin_bar
    y_t  = (y_C1 + y_C2)/2
    x_t  = y_C1 + sqrt(Rmin_bar**2 - (y_t - y_C1)**2)
    x_s = 2*x_t - x_C1
    x_C2 = x_s
    
    diameter_C1 = math.hypot(x_t-x_C1, y_t-y_C1)
    diameter_C2 = math.hypot(x_C2 - x_t, y_C2 - y_t)
    
    angle_C1 = getAngle([x_t,y_t],[x_C1,y_C1],[x_C1,y_C1 - Rmin_bar])
    angle_C2 = getAngle([x_t,y_t],[x_C2,y_C2],[x_s,y_s])
    
    arc_length_C1 = (pi*diameter_C1) * (angle_C1/360)
    arc_length_C2 = (pi*diameter_C2) * (angle_C2/360)
    
   #print("C1 diameter:", diameter_C1)
    
    print("x_C1:", x_C1, "; y_C1:", y_C1)
    print("x_C2:", x_C2, "; y_C2:", y_C2)
    print("x_s:", x_s, "; y_s:", y_s)
    print("x_t:", x_t, "; y_t:", y_t)
    
    print("Arc length C1:", arc_length_C1)
    print("Arc length C2:", arc_length_C2)
    
    steerRight()
    time.sleep(1)
    advanceCar(40, False)
    moveBrake(False)
    
    time.sleep(1)
    steerLeft()
    time.sleep(1)
    advanceCar(40, False)
    moveBrake(False)
    
    time.sleep(1)
    steerNeutral()    

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
    global ind_MAX, ind_MIN, parkingWidth, xList, yList, timeList
    
    firstEdge = False
    secondEdge = False
    

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
            parkingWidth = distanceRight
            firstEdgeIndex = iteration
            print("Second edge iteration is ", iteration)
            print("First edge time is ", timeList[iteration])
            
        
        if ( firstEdge and distanceRight < calibratedDistance and areLastElementsEq()):
            secondEdge = True
            print ("Second edge detected")
            moveBrake(True)
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
        parkCar()
    elif (pushes == 2):
        pass
    '''
    parkCar()
    '''
    print("Callback ended, exiting subroutine")
    pushes += 1
    pushes = pushes % 3
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
