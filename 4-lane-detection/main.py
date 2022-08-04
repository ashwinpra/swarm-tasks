import lanedetection

level = int(input("Enter level: "))
vid = cv2.VideoCapture(f"./raw-videos/level{level}.mp4")
#out = cv2.VideoWriter('output.avi', -1, 20.0, (640,480))