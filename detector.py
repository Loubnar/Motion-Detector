# motion.py
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time
import numpy as np

# Computing the difference
def diffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1,t0)
    return cv2.bitwise_and(d1,d2)


filename = "card.jpeg"
cam = PiCamera()
cam.resolution = (1440,1080)
cam.color_effects = (128,128)
cam.framerate = 24
raw = PiRGBArray(cam, size=(1440,1080))
minchange = 250*250*2/100

print "Camera warm up..."
time.sleep(1)

print "Initializing..."
cam.capture(raw, 'bgr', True)
t_minus = raw.array
raw.truncate(0)
time.sleep(0.05)
cam.capture(raw, 'bgr', True)
t = raw.array

print "Started."

while True:
    raw.truncate(0)
    
    # Creating selections for motion tests

    #t-1
    zone1m = t_minus[400:650,595:845] # Center
    zone2m = t_minus[0:250,0:250] # Top left
    zone3m = t_minus[850:1080,0:250] # Bottom left
    zone4m = t_minus[0:250,1190:1440] # Top right
    zone5m = t_minus[830:1080,1190:1440] # Bottom right

    # t
    zone1 = t[400:650,595:845] # Center
    zone2 = t[0:250,0:250] # Top left
    zone3 = t[850:1080,0:250] # Bottom left
    zone4 = t[0:250,1190:1440] # Top right
    zone5 = t[830:1080,1190:1440] # Bottom right

    # Computing difference
    result = cv2.absdiff(zone1,zone1m)
    change = np.count_nonzero(result>20)
    
    if change > minchange:
        print "Motion detected : zone 1."	
    else:
	result = cv2.absdiff(zone2,zone2m)
	change = np.count_nonzero(result>20)
	if change > minchange:
        	print "Motion detected : zone 2."
	else:
		result = cv2.absdiff(zone3,zone3m)
		change = np.count_nonzero(result>20)
		if change > minchange:
        		print "Motion detected : zone 3."
		else:
			result = cv2.absdiff(zone4,zone4m)
			change = np.count_nonzero(result>20)
			if change > minchange:
        			print "Motion detected : zone 4."
			else:	
				result = cv2.absdiff(zone5,zone5m)
				change = np.count_nonzero(result>20)
				if change > minchange:
        				print "Motion detected : zone 5."
				else:
					print "No motion."
					cv2.imwrite(filename,t)
	  
    t_minus = t
    cam.capture(raw, 'bgr', True)
    t = raw.array

print "Done."

