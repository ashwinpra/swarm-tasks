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

def threshold_method(frame):
    # we will do adaptive thresholding 
    # first we will convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # we will use the cv2.ADAPTIVE_THRESH_GAUSSIAN_C method, with C = 5 
    # we will use the cv2.THRESH_BINARY_INV as the thresholding method
    # we will use the block size of 11
    # we will use the constant C of 5
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 5)
    # we will use the cv2.bitwise_not function to invert the image
    thresh = cv2.bitwise_not(thresh)
    # we will return the thresholded image
    return thresh


def edge_based_segmentation(frame):
    # we will convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # noise reduction through different filters
    # edge detection
    edges = cv2.Canny(gray, 100, 200)
    # region of interest
    edges = cv2.erode(edges,(3,3))
    edges = cv2.dilate(edges,(3,3))
    # find the contours in the image
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # find those contours that are of sufficient area, in order to avoid small corners in background
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 1000]
    # make a mask with these contours
    mask = cv2.drawContours(edges, contours, -1, (255,255,255), 3)
    # apply the mask to the original image
    img = cv2.bitwise_and(frame, frame, mask=mask)
    # return the image
    return img

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
    print(frame.shape)
    thresh_frame = threshold_method(frame)
    edges = edge_based_segmentation(frame)
    # we will show the thresholded image
    cv2.imshow("Thresholded Image", thresh_frame)
    # we will show the edges
    cv2.imshow("Edges", edges)
    # this thresholded frame can further be segmented using other methods

    



    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.waitKey(1) & 0xFF == ord('0'): 
        break

vid.release()
cv2.destroyAllWindows()