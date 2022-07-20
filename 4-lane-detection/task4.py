import cv2 
import numpy as np

# Capturing and decoding video file
vid = cv2.VideoCapture('./level3_raw.mp4')

# Function to find path from video
def findPath(img, nr):
    # Converting RGB Image to grayscale
    bw = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 

    # Noise reduction through different filters
    if nr == 'gaussian':
        nr_img = cv2.GaussianBlur(bw,(5,5),0)
    elif nr == 'bilateral':
        nr_img = cv2.bilateralFilter(bw,9,75,75)
    elif nr == 'median':
        nr_img = cv2.medianBlur(bw,5)
    elif nr == 'box':
        nr_img = cv2.boxFilter(bw,0,(5,5))
    elif nr == 'fast':
        nr_img = cv2.fastNlMeansDenoising(bw,None,10,7,21)

    # Edge Detection
    edges = cv2.Canny(nr_img, 100, 200)

    #! Region of Interest (Not sure if procedure is right)
    # Erode and dilute
    edges = cv2.erode(edges,(3,3))
    edges = cv2.dilate(edges,(3,3))
    # Find the contours in the image
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Find those contours that are of sufficient area, in order to avoid small corners in background
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 1000]
    # Make a mask with these contours 
    mask = cv2.drawContours(edges, contours, -1, (255,255,255), 3)
    # Perform bitwise-and
    edges = cv2.bitwise_and(edges, edges, mask=mask)

    # Hough Line Transform
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # Drawing lines to denote path
            cv2.line(img, (x1, y1), (x2, y2), (0,0,255), 10)

    # Returning image with lines denoting path
    return img



while 1:
    ret, frame = vid.read() 

    #Testing different noise reduction methods
    p1 = findPath(frame,'gaussian')
    #p2 = findPath(frame,'bilateral')
    #p3 = findPath(frame,'median')
    #p4 = findPath(frame,'box')
    #p5 = findPath(frame,'fast')
    
    cv2.imshow('p1',p1)
    #cv2.imshow('p3',p3)
    #cv2.imshow('p2',p2)
    #cv2.imshow('p4',p4)
    #cv2.imshow('p5',p5)


    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.waitKey(1) & 0xFF == ord('0'): 
        break


vid.release()
cv2.destroyAllWindows()