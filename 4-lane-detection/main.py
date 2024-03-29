import cv2 
import numpy as np
from functions import * 

level = int(input("Enter level: "))

vid = cv2.VideoCapture(f"./raw-videos/level{level}.mp4")

lower_y = np.array([20,100,100],dtype=np.uint8)
upper_y = np.array([40,255,255],dtype=np.uint8)
lower_w = 220
upper_w = 255

last_left_line = None
last_right_line = None

last_y_lines = None
last_w_lines = None

while 1:
    ret, frame = vid.read() 

    if ret:
        all_lines = processYWLines(frame,lower_y,upper_y,lower_w,upper_w)
        try:
            left_line,right_line = getLR(all_lines)
        except:
            continue

        try:
            frame = drawBox(frame,left_line,right_line)
        except:
            continue

        cv2.imshow("Lane Detection",frame)

    else:
        break

    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.waitKey(1) & 0xFF == ord('0'): 
        break

vid.release()
result.release()
cv2.destroyAllWindows()