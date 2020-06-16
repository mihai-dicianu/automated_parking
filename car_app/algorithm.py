#Local imports
from bt         import * 
from gpio_setup import *
import time
import numpy as np

timeList = []
xList = []
yList = []

carSpeed = 26.66

secondPress = False
time_initial = None   

def isAproxEqual(distanceRef, distance):
    if(distance < distanceRef * 1.1 and distance > distanceRef * 0.9):
        return True
    else:
        return False

def areLastElementsEq():
    if (isAproxEqual(yList[-1], yList[-2]) and isAproxEqual(yList[-1], yList[-3])):
        return True
    else:
        return False

def findParkingSpot(calibrationDistance):
    #time.sleep(0.050)
    moveForward()
    firstEdge = False
    secondEdge = False
    emptyDistance = None

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
        
        xList.append(time_current*carSpeed)
        yList.append(distanceRight)
        timeList.append(time_current)
        
        #check if the car hasn't passed the first parked car
        if( not distanceRight < 10 and firstEdge == False and areLastElementsEq()):
            firstEdge = True
            print ("First edge detected")
            emptyDistance = distanceRight
            print (yList)
            
        
        if ( firstEdge and distanceRight < 10 and areLastElementsEq()):
            secondEdge = True
            print ("Second edge detected")
            moveNeutral()
            return
        '''
        if (firstEdge and secondEdge):
        
            #calculate the numerical derivative of the lateral measurement
            derivative = np.diff(yList)/np.diff(xList)
            
            ind_MAX = np.argmax(derivative)
            ind_MIN = np.argmin(derivative)
        '''
       
def buttonCallback(self):
    print("Raspi button pushed: Initiate")
    
    calibrationDistance = read_sensor('right')
    
    time.sleep(2)
    
    findParkingSpot(calibrationDistance)
  
    print("Callback ended, exiting subroutine")
    moveNeutral()
     

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
