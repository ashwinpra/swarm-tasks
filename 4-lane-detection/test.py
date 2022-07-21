import cv2 
import numpy as np 

level = int(input("Enter level: "))
vid = cv2.VideoCapture(f"./level{level}_raw.mp4")

"""
We will try the following methods: 
Threshold Method
Edge Based Segmentation
Region Based Segmentation
Clustering Based Segmentation
Watershed Based Method
Artificial Neural Network Based Segmentation
"""

def inROI(frame,x,y):
    return x > 0 and x < frame.shape[1] and y > frame.shape[0]*0.6 and y < frame.shape[0]

def threshold_method(frame):
    # we will do adaptive thresholding 
    # first we will convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # we will use the cv2.ADAPTIVE_THRESH_GAUSSIAN_C method, with C = 5 
    # we will use the cv2.THRESH_BINARY_INV as the thresholding method
    # we will use the block size of 11
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 5)
    # we will use the cv2.bitwise_not function to invert the image
    thresh = cv2.bitwise_not(thresh)

    return thresh



def edge_based_segmentation(frame):
     # Converting RGB Image to grayscale
    bw = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) 

    # Noise reduction through gaussian blur
    nr_img = cv2.GaussianBlur(bw,(5,5),0)

    # Edge Detection
    edges = cv2.Canny(nr_img, 100, 200)

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
    roi_x = [0, frame.shape[1]]
    roi_y = [frame.shape[0]*0.6, frame.shape[0]]
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # Check if this falls within the ROI 
            if inROI(frame,x1,y1) and inROI(frame,x2,y2):
                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    # Returning image with lines denoting path
    return frame

def region_based_segmentation(frame): 
    pass

def clustering_based_segmentation(frame):
    pass

def watershed_based_method(frame):
    pass

def ANN_based_segmentation(frame):
    pass

while 1:
    ret, frame = vid.read() 

    thresh_frame = threshold_method(frame)

    edge_frame = edge_based_segmentation(frame)

    # we will show the edges
    cv2.imshow("Edge based", edge_frame)



    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.waitKey(1) & 0xFF == ord('0'): 
        break

vid.release()
cv2.destroyAllWindows()