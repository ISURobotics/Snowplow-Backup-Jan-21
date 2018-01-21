import numpy as np
import serial
import cv2
import glob
import yaml
from cv2 import aruco
import os
import sys
import time

from socket import *
import socket
from datetime import datetime

host = "192.168.1.4" # set to IP address of target computer
port = 13000
addr = (host, port)
##UDPSock = socket(AF_INET, SOCK_DGRAM)
##UDPSock.setsockopt(IPPROTO_TCP, TCP_NODELAY,1)

with open('calibration - mywebcam_720p.yaml') as f:
    loadeddict = yaml.load(f)
mtxloaded = loadeddict.get('camera_matrix')
distloaded = loadeddict.get('dist_coeff')

camera_matrix = np.array(mtxloaded)
dist_coeffs = np.array(distloaded)

rad2deg = 180/3.14159

image_size = (1280,720) #size of input image.  From webcam, this will be 1920, 1080
aruco_dict = aruco.Dictionary_get( aruco.DICT_6X6_1000 ) #Must be same as dictionary I made boards from
markerLength = 16*3/4*140/125 #Dimensions can be anything, but will match what is later returned in tvec
markerSeparation = .7 #only matters for boards
board = aruco.GridBoard_create(5, 7, markerLength, markerSeparation, aruco_dict)
arucoParams = aruco.DetectorParameters_create() #Just use this

i = 5
cap = cv2.VideoCapture(1)
cap.set(3,1280)
cap.set(4,720)
while True: #Can also be a while True loop
    ret, imgRemapped = cap.read()
    if i<1: #on the first iteration, find the obstacles and send their locations
        i+=1
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #c.connect(("192.168.1.4", 8089))
        c.connect(("192.168.1.4", 8089))
        data = "-.5 6 0 6"
        print(data)
        c.send(data)
        c.close()
        
        #time.sleep(5)
        #exit()
        continue
    imgRemapped_gray = cv2.cvtColor(imgRemapped, cv2.COLOR_BGR2GRAY)    # aruco.detectMarkers() requires gray image
    corners, ids, rejectedImgPoints = aruco.detectMarkers(imgRemapped_gray, aruco_dict, parameters=arucoParams) # Detect aruco marker.
    try: # if aruco marker detected
        tvec = aruco.estimatePoseSingleMarkers(corners, markerLength, camera_matrix, dist_coeffs)[1] # For a single marker
        rvec = aruco.estimatePoseSingleMarkers(corners, markerLength, camera_matrix, dist_coeffs)[0]
        #imgWithAruco = aruco.drawDetectedMarkers(imgRemapped, corners, ids, (0,255,0)) #Draws a box around the marker based on its corners, in green. Labels it with its id.
        #imgWithAruco = aruco.drawAxis(imgWithAruco, camera_matrix, dist_coeffs, rvec, tvec, 12)    # axis length is last parameter.  The unit of this matches input unit. Can be feet, inches, anything.
        print("Connecting")
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.connect(("192.168.1.4", 8089))
        print("Connected")
        x,y,z = tvec[0][0][0], tvec[0][0][1], tvec[0][0][2] #tvec stores position
        pitch,roll,yaw = rvec[0][0][0]*rad2deg, rvec[0][0][1]*rad2deg, rvec[0][0][2]*rad2deg
        print(x,y,z, ids[0][0])
        #print(rvec)
        #data = "x: "+str(x)+ " y: " + str(y)+" z: " + str(z)+" id: " + str(ids[0][0])+ "\n"
        data = str(x) + ' ' + str(y) + ' ' + str(z) + ' ' +str(ids[0][0])
        c.send(data)
        c.close()
        time.sleep(.2)
        #UDPSock.flush()
        #ser.write(' ')
        if(ids[0][0] == 1): #If I see the first marker, draw red
            color = 'r'
        if(ids[0][0] == 2): #If I see second marker, draw blue
            color = 'b'
        else:
            color = 'g'
        #print(rvec[0][0][1])
        ##ax.scatter(x, z, -y, c=color, marker='o') #Plots my points in a way that's easier to visualize.
       
    #else:   # if aruco marker is NOT detected
        #imgWithAruco = imgRemapped
        #time.sleep(.001)# assign imRemapped_color to imgWithAruco directly
        
    #cv2.imshow("aruco", imgRemapped)   # display
    except:
		continue
        #time.sleep(.2)
        #print("Marker not detected")
        # c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # c.connect(("192.168.1.4", 8089))
        # data = 's s s s'
        # c.send(data)
        # c.close()
    print(str(datetime.now()))
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):   # if 'q' is pressed, quit.
        break
UDPSock.sendto("exit", addr)
UDPSock.close()
os._exit(0)
##ax.set_xlabel('Left or Right')
##ax.set_ylabel('Depth')
##ax.set_zlabel('Height')

##plt.show()

##while True:
##    plt.pause(.05)


