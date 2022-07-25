import numpy as np
import cv2

green = np.uint8([[[255, 255, 255]]]) #here insert the bgr values which you want to convert to hsv
hsvGreen = cv2.cvtColor(green, cv2.COLOR_BGR2HSV)
print(hsvGreen)

lowerLimit = hsvGreen[0][0][0] - 10, 100, 100
upperLimit = hsvGreen[0][0][0] + 10, 255, 255

print(upperLimit)
print(lowerLimit)

lower_yellow = np.array([20,100,100],dtype=np.uint8)
upper_yellow = np.array([40,255,255],dtype=np.uint8)
lower_white = 200
upper_white = 255

print(type(lower_yellow)==np.ndarray)