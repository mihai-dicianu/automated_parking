#Local imports
from bt         import * 
from gpio_setup import *

import time
import numpy as np
import math
from math import sqrt
from math import pi


timeList = []
xList = []
xListPark = []
yList = []

carSpeed = 36.66 #cm
secondPress = False
time_initial = None
pushes = 0
arcLength = 0

Ri_min = 46
Re_min = 73
L_min  = 66.4
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

def positionMiddle():
    
    time_init = time.time()
    while True:
        time_current = time.time()
        distanceFront = read_sensor('front')
        distanceBack  = read_sensor('back')
        
        sendData(socketFront, time_current - time_init, distanceFront)
        sendData(socketBack, time_current - time_init, distanceBack)


        if(isAproxEqual(distanceFront, distanceBack)):
           moveNeutral()
           break
        elif (distanceFront > distanceBack):
           moveForward()
        else:
           moveBackward()

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
    
def parkCar (arcLength):
    steerRight()
    time.sleep(1)
    advanceCar(arcLength, False)
    moveBrake(False)
    
    #time.sleep(1)
    steerLeft()
    #time.sleep(1)
    advanceCar(arcLength, False)
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
    
def findParkingSpot():

    global ind_MAX, ind_MIN, parkingWidth, xList, yList, timeList, arcLength
    
    firstEdge  = False
    secondEdge = False
    parkOK     = False
    
    iteration = 0
    firstEdgeIndex = None
    secondEdgeIndex = None
    
    distanceThreshold = read_sensor('right') * 1.5
    print("Starting parking maneuver, distance threshold is ", distanceThreshold, "cm.")
    
    moveForward()
    #time.sleep(0.75)
    time_initial = time.time()
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
        
        if(socketRight != None):
            sendData(socketRight, time_current, distanceRight)
       
        xList.append(time_current*carSpeed)
        yList.append(distanceRight)
        timeList.append(time_current)
        
        #check if the car has passed the first parked car
        if( not (distanceRight < distanceThreshold) and areLastElementsEq() and not firstEdge):
            firstEdge = True
            parkingWidth = distanceRight
            firstEdgeIndex = iteration
                             
            print("First edge detected")            
            print("First edge iteration is ", iteration)
            print("First edge time is ", timeList[iteration])
            print("Currently at x:", xList[iteration])
            print("Parking width is ", parkingWidth)
        
        #check if the car has passed the parking spot
        if (firstEdge and distanceRight < distanceThreshold and areLastElementsEq() and not secondEdge):
            
            secondEdge = True
            moveBrake(True)
            secondEdgeIndex = iteration
            
            print("Second edge detected")
            print("Second edge time is ", timeList[iteration])
            print("Second edge iteration is ", iteration)
            
            print("Currently at x:", xList[iteration])
            
        #calculate coordinates if parking spot is passed    
        if (firstEdge and secondEdge and not parkOK):
            parkOK = True
            print ("Parking spot length is  ", carSpeed * (timeList[secondEdgeIndex] - timeList[firstEdgeIndex]))
            #calculate the numerical derivative of the lateral measurement
            derivative = np.diff(yList)/np.diff(xList)
            
            ind_MAX = np.argmax(derivative)
            ind_MIN = np.argmin(derivative)
            
            parkingLength = xList[ind_MIN] - xList[ind_MAX]
            print ("Derivative length is ", parkingLength)
                        
            if(parkingLength > L_min):
                print("Distance to parking spot", parkingWidth)
    
                #x_C1 = xList[ind_MAX] + p
                x_C1 = p
                y_C1 = Rmin_bar + w/2
                
                #y_s  = parkingWidth + w/2
                y_s  = parkingWidth + w/2
                y_C2 = y_s - Rmin_bar
                y_t  = (y_C1 + y_C2)/2
                x_t  = x_C1 + sqrt(Rmin_bar**2 - (y_t - y_C1)**2)
                x_s  = 2*x_t - x_C1
                x_C2 = x_s
                             
                diameter_C1 = math.hypot(x_t-x_C1, y_t-y_C1)
                diameter_C2 = math.hypot(x_C2 - x_t, y_C2 - y_t)
                
                angle_C1 = getAngle([x_C1,y_C1 - Rmin_bar],[x_C1,y_C1],[x_t,y_t])
                print ("C1 angle is ", angle_C1)
                angle_C2 = getAngle([x_s,y_s],[x_C2,y_C2],[x_t,y_t],)
                print ("C2 angle is ", angle_C2)
                
                arc_length_C1 = (pi*diameter_C1) * (angle_C1/360)
                arc_length_C2 = (pi*diameter_C2) * (angle_C2/360)
                
                print("C1 diameter:", diameter_C1)
                print("C2 diameter:", diameter_C2)
                print("x_C1:", x_C1, "; y_C1:", y_C1)
                print("x_C2:", x_C2, "; y_C2:", y_C2)
                print("x_s:", x_s, "; y_s:", y_s)
                print("x_t:", x_t, "; y_t:", y_t)
                
                print("Arc length C1:", arc_length_C1)
                print("Arc length C2:", arc_length_C2)
                
                arcLength = arc_length_C1
                
            else:
                
                print("Parking is too small")
                return
       
        if(parkOK):
           
            if (xList[-1] - xList[ind_MAX] > x_s):
                        print("arrived !")
                        print("In time:", time_current)
                        print ("last x is ", xList[-1])
                        
                        return

        iteration += 1
    
   
           
def buttonCallback(self):
    
    global pushes
    
    print("Button push detected")
    print("Mode selected:", pushes)
   
    time.sleep(2)
    
    if (pushes == 0):
        #positionMiddle()
        findParkingSpot()
    elif (pushes == 1):
        parkCar(arcLength)
        #advanceCar(20,True)
    #elif (pushes == 2):
        
    '''
    parkCar()
    '''
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
