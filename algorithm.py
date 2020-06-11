#Local imports
from bt         import * 
from gpio_setup import *

import time

secondPress = False       

def buttonCallback(self):
    print("Raspi button pushed: Initiate")
    
    global secondPress
    if secondPress:
        return
    
    time.sleep(2)
    
    moveForward()
    
    time_initial = time.time()
    
    while True:
        if isPressed():
            secondPress = not secondPress
            break
        
        #distanceFront = read_sensor('front')
        #distanceBack  = read_sensor('back')
        distanceRight = read_sensor('right')
        
        '''
        if distanceBack < 10 or distanceFront < 10:
            #moveForward()
            #time.sleep(0.5)
            print ("OooO")
            break
        '''
        time_delta_current = time.time() - time_initial

        #time.sleep(0.01)
        #sendData(socketRight, time_delta_current, distanceRight)
        #sendData(socketFront, 0, 1)
        #sendData(socketBack, 10, 10)
    
    
  
  
    print("DIED")
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
