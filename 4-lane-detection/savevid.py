import cv2 
from functions import * 

for i in range(1,4):
    vid = cv2.VideoCapture(f"./raw-videos/level{i}.mp4")

    size = (int(vid.get(3)), int(vid.get(4)))
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    result_y = cv2.VideoWriter(f'./processed-videos/level{i}_yellow.avi',fourcc,10, size)
    result_w = cv2.VideoWriter(f'./processed-videos/level{i}_white.avi',fourcc,10, size)

    while 1: 
        ret, frame = vid.read() 

    if ret:
        y_processed, w_processed, all_lines = processYWLines(frame)
        result_y.write(y_processed)
        result_w.write(w_processed)

    else:
        break

    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.waitKey(1) & 0xFF == ord('0'): 
        break

    vid.release()

cv2.destroyAllWindows()
