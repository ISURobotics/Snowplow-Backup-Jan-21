import cv2
import numpy as np
from stopsignDetectionGRIP import GripPipeline

def detectStopSign(scene):
        try:
                pipeline = GripPipeline()
                pipeline.process(scene)
                redoct = cv2.imread("red octagon.png")
                redoctHSV = cv2.cvtColor(redoct,cv2.COLOR_BGR2HSV)
                #sceneHSV = cv2.cvtColor(scene,cv2.COLOR_BGR2HSV)
                #cv2.imshow('img', sceneHSV)
                #key = cv2.waitKey(0) & 0xFF
                lower1 = (0,23, 0)
                upper1 = (56, 255, 255)
                #lower2 = (0,109,20)
                #upper2 = (33,255,255)
                #lower2b = (160, 60, 30)
                #upper2b = (180, 255, 166)

                octMask = cv2.inRange(redoctHSV,lower1,upper1)

##                sceneMask = cv2.inRange(sceneHSV,lower2,upper2)
##                sceneMaskb = cv2.inRange(sceneHSV, lower2b, upper2b)
##                sceneMask = cv2.bitwise_or(sceneMask, sceneMaskb)
##                sceneMask = cv2.erode(sceneMask,None, iterations = 1)
##                sceneMask = cv2.dilate(sceneMask,None, iterations = 5)

                contours = cv2.findContours(octMask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)[-2]
                cnt1 = contours[0]
                #rectDrawn = cv2.drawContours(redoct,[cnt1],0, (0,255,0),3)
                #contours = cv2.findContours(sceneMask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)[-2]
                contours = pipeline.filter_contours_output
                #hull = cv2.convexHull(contours[0])
                c = max(contours, key = cv2.contourArea)
                hull = cv2.convexHull(c)
                #sceneDrawn = cv2.drawContours(scene, [hull], 0, (0,255,0), 3)
                ret = cv2.matchShapes(cnt1,hull,1,0.0)
                return ret
        except:
                print("Error when detecting stop sign")
                return 1


