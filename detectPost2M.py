import cv2
import grip
import numpy as np
from time import sleep
from math import pow
from math import sin
from math import cos
from math import tan
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
pi = 3.14159
thetaT = -158*pi/180

##camera = PiCamera()
##camera.resolution = (640,480)
##camera.framerate = 32
##rawCapture = PiRGBArray(camera, size=(640,480))
##time.sleep(2)

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)
	
def roundToHalf(num):
	return round(num*2)/2
	
def scaleWidth(w, c):
	dfc = abs(640-c)
	ratio = 8*pow(10,-7)*dfc*dfc+8*pow(10,-5)*dfc+.9958
	newWidth = w/ratio
	return newWidth
	
def transX(x, y):
	newX = x*cos(thetaT)-y*sin(thetaT)-7
	return -newX

def transY(x,y):
	newY = x*sin(thetaT)+y*cos(thetaT)+0
	return -newY

Postpipeline = grip.GripPipeline()
wlist = []
centerList = []
counter = 0
numSamples = 100

def detectPost(scene):
    #time.sleep(.1)
    global Postpipeline
    Postpipeline.process(scene)
    #print("Frame processed")
    cnts = Postpipeline.convex_hulls_output
    try:
            firstCnt = max(cnts, key = cv2.contourArea)
            rect = cv2.minAreaRect(firstCnt)
            try:
                    x = int(rect[0][0])
                    y = int(rect[0][1])
                    w = int(rect[1][0])
                    h = int(rect[1][1])
                    center = x+w/2
                    if(w>h):
                            temp = w
                            w = h
                            h = temp
                    if(5*w<h and w>=28 and (center>280 or center<360)):
                        print("Post Detected less than 2 meters away")
                        return True
                    else:
                        print("Post not detected")
                        print(str(w))
                        return False
            
            except:
                    print("Post not detected - Exception 1")
                    return False
            
    except:
            print("Post not detected - Exception 2")
            return False
