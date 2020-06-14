
import bluetooth
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import time
import csv
import threading

style.use('fivethirtyeight')

time_bytes = 7
distance_bytes = 7
delim_bytes = 1
total_bytes = time_bytes + delim_bytes + distance_bytes

 

def processData(data):
    
    pair = data.decode("utf-8")
    pair = pair.split(',')
    
    pair[0] = pair[0].lstrip('0')
    pair[1] = pair[1].lstrip('0')
    
    time = float(pair[0])
    distance = float(pair[1])
    
    return time, distance

def dataThread(name, port, file_path):
    print(name, "sensor thread started on Bluetooth port ", port)
    
    fieldnames = ["x_value", "distance"]
    with open(file_path, 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames, lineterminator='\n')
        csv_writer.writeheader()
    
    
    #create the RFCOMM Bluetooth socket and attach it to local adapter 
    server_sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    server_sock.bind(("",port))
    #start listening on the specified port 
    server_sock.listen(1)
    #accepted the incoming connection and print the address on the other device 
    client_sock,address = server_sock.accept()
    print ("Accepted connection from ",address," on thread ", name)
        
    while True:
        with open(file_path, 'a') as file:
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator='\n')
            data = client_sock.recv(total_bytes)

            time, distance = processData(data)
            row = [time, distance]
             
            print ("[BT_DATA_" + name.upper() + "] time = " + str(time).ljust(5,'0') + "s, distance = "+ str(distance).ljust(5,'0')+"cm")
            
            info = {
                "x_value": time,
                "distance": distance,
            }

            csv_writer.writerow(info)
        
    client_sock.close()
    server_sock.close()





    





