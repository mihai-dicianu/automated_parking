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

def aproxEqual (distanceRef, distance):
    if(distance < distanceRef * 1.1 and distance > distanceRef * 0.9)
        return True
    else:
        return False

def findParkingSpot(calibrationDistance):

    firstEdge = False
    secondEdge = False
    emptyDistance = None

    time_initial = time.time()
    
    while True:
        if isPressed() or distanceFront < 10:
            secondPress = not secondPress
            moveNeutral()
            break
            
        #distanceFront = read_sensor('front')
        #distanceBack  = read_sensor('back')
        distanceRight = read_sensor('right')
        
        time_current = time.time() - time_initial
        
        xList.append(time_current*carSpeed)
        yList.append(distanceRight)
        timeList.append(time_current)
        
        #check if the car hasn't passed the first parked car
        if( not aproxEqual(calibrationDistance, distanceRight) and firstEdge == False):
            firstEdge = True
            emptyDistance = distanceRight        
        
        if ( emptyDistance != None and firstEdge == True and not aproxEqual(emptyDistance, distanceRight) )
            secondEdge = True 

        if (firstEdge and secondEdge)
        
            #calculate the numerical derivative of the lateral measurement
            derivative = np.diff(yList)/np.diff(xList)
            
            ind_MAX = np.argmax(derivative)
            ind_MIN = np.argmin(derivative)
        
       
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
    socketRight, socketFront, socketBack = connectBluetooth()
    


    a = None
    while True:
        time.sleep(10)

finally:
    print('Application is ending!')
    disconnectBluetooth()
    GPIO.cleanup()
