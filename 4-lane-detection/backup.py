import cv2 
import numpy as np 

level = int(input("Enter level: "))
vid = cv2.VideoCapture(f"./level{level}_raw.mp4")


def ROI(frame):
    # region of interest is taken as the rectangle drawn with vertices: 
    # (0,0.6*height), (width,0.6*height), (width,height), (0,height)    
    # must be passed in order: lower left, upper left, upper right, lower right
    vertices = np.array([[0,frame.shape[0]],[0,frame.shape[0]*0.6],[frame.shape[1],frame.shape[0]*0.6],[frame.shape[1],frame.shape[0]]],dtype=np.int32)
    mask = np.zeros_like(frame)
    cv2.fillPoly(mask, [vertices], 255)
    masked_image = cv2.bitwise_and(frame,mask)
    return masked_image

def hough(frame):
    # Converting RGB Image to HSV (for better color detection)
    #gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    # Defining the range of yellow color in HSV
    lower_yellow = np.array([20,100,100],dtype=np.uint8)
    upper_yellow = np.array([30,255,255],dtype=np.uint8)
    # Defining the range of white color in HSV
    lower_white = np.array([200,200,200],dtype=np.uint8)
    upper_white = np.array([255,255,255],dtype=np.uint8)
    # Thresholding the image
    mask_yellow = cv2.inRange(hsv,lower_yellow,upper_yellow)
    mask_white = cv2.inRange(hsv,lower_white,upper_white)
    # Bitwise-AND mask and original image
    mask_yw = cv2.bitwise_or(mask_white,mask_yellow)
    #mask_yw_image = cv2.bitwise_and(hsv,mask_yw)
    mask = cv2.bitwise_and(hsv,hsv,mask=mask_yellow)

    # Applying Gaussian Blur on the image
    blur = cv2.GaussianBlur(mask,(5,5),0)
    # Converting to grayscale
    gray = cv2.cvtColor(blur,cv2.COLOR_BGR2GRAY)

    # Edge Detection
    edges = cv2.Canny(gray, 100, 200)
    edges = ROI(edges)
    # Erode and dilute
    edges = cv2.erode(edges,(3,3))
    edges = cv2.dilate(edges,(3,3))

    # Hough Line Transform
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, np.array([]), 50, 10)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # Check if this falls within the ROI 
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 3,cv2.LINE_AA)

    # Returning image with lines denoting path
    return frame

def ANN_based_segmentation(frame):
    pass

while 1:
    ret, frame = vid.read() 

    if ret:
        hough_frame = hough(frame)
        cv2.imshow("Hough based",hough_frame)
    else:
        break


    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.waitKey(1) & 0xFF == ord('0'): 
        break

vid.release()
cv2.destroyAllWindows()