import cv2 
from functions import * 

lower_y = np.array([20,100,100],dtype=np.uint8)
upper_y = np.array([40,255,255],dtype=np.uint8)
lower_w = 220
upper_w = 255

vid = cv2.VideoCapture(f"./raw-videos/level2.mp4")

size = (int(vid.get(3)), int(vid.get(4)))
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
result_y = cv2.VideoWriter(f'./processed-videos/level2_yellow.avi',fourcc,10, size)
result_w = cv2.VideoWriter(f'./processed-videos/level2_white.avi',fourcc,10, size)

while 1: 
    ret, frame = vid.read() 

    if ret:
        y_processed, w_processed, all_lines = processYWLines(frame,lower_y,upper_y,lower_w,upper_w)
        result_y.write(y_processed)
        result_w.write(w_processed)
        cv2.imshow("Lane Detection",y_processed)
    else:
        break

    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.waitKey(1) & 0xFF == ord('0'): 
        break

vid.release()

cv2.destroyAllWindows()
