import bluetooth
import time

target_name = "MIHAIPC"
bd_addr     = "5C:F3:70:91:CC:D6"

portFront   = 10
portRight   = 9
portBack    = 11

socketFront      = None
socketRight      = None
socketBack       = None

time_bytes = 7
distance_bytes = 7


def connectBluetooth():
    start_time = time.time()    
    print ("Starting Bluetooth connections.")
    
    discover_time = time.time() - start_time
        
    global socketFront
    global socketRight
    global socketBack

    socketFront = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    socketFront.connect((bd_addr, portFront))
    print ("FRONT socket is connected.")    
    
    socketRight = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    socketRight.connect((bd_addr, portRight))
    print ("RIGHT socket is connected.")
    
    socketBack = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    socketBack.connect((bd_addr, portBack))
    print ("BACK socket is connected.")
    
    time_to_connect = time.time() - start_time
    print ("Connection time for all Bluetooth sockets is %.2f s." % time_to_connect )

    return socketRight, socketFront, socketBack

def sendData (socket, time, distance):

    if distance > 100:
        distance = 100
    if distance < 1:
        distance = 1    
    
    time_formatted = "{:.3f}".format(time)
    time_formatted  = time_formatted.zfill(time_bytes)
    print(time_formatted)

    distance_formatted = "{:.3f}".format(distance)
    distance_formatted  = distance_formatted.zfill(distance_bytes)
    print(distance_formatted)

    packetBT = str(time_formatted) + ","  + str(distance_formatted)
    
    ## add len check
    print (packetBT)
    socket.send(packetBT)
    
    return 0

def disconnectBluetooth():
    socket.close()