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

def hough_with_mask(frame,lower,upper):
    if(type(lower)==np.ndarray):
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv,lower,upper) 
        masked_image = cv2.bitwise_and(hsv,hsv,mask=mask)
        blur = cv2.GaussianBlur(masked_image,(5,5),0)
        final = cv2.cvtColor(blur,cv2.COLOR_BGR2GRAY)
    else:
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        mask = cv2.inRange(gray,lower,upper)
        masked_image = cv2.bitwise_and(gray,gray,mask=mask)
        final = cv2.GaussianBlur(masked_image,(5,5),0)

    edges = cv2.Canny(final, 50, 150)
    edges = ROI(edges)
    # Erode and dilute
    edges = cv2.erode(edges,(3,3))
    edges = cv2.dilate(edges,(3,3))

    # Hough Line Transform
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, np.array([]), 50, 10)

    return lines

# Work with dem lines 
def draw(frame,lines):
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 3,cv2.LINE_AA)
    return frame

def combine_lines(l1,l2):
    # return a set of lines combining both l1 and l2, while neglecting duplicates
    if l1 is not None and l2 is not None:
        for line in l1:
            if line not in l2:
                np.append(l2,line)
        return l2

lower_yellow = np.array([20,100,100],dtype=np.uint8)
upper_yellow = np.array([40,255,255],dtype=np.uint8)
lower_white = 220
upper_white = 255
#lower_white = np.array([0, 100, 100], dtype=np.uint8)
#upper_white = np.array([10, 255, 255], dtype=np.uint8)

while 1:
    ret, frame = vid.read() 

    if ret:
        """Code goes here"""
        y_lines = hough_with_mask(frame,lower_yellow,upper_yellow)
        w_lines = hough_with_mask(frame,lower_white,upper_white)
        all_lines = combine_lines(y_lines,w_lines)
        frame = draw(frame,all_lines)
        #frame = draw(frame,y_lines)
        #frame = draw(frame,w_lines)
        cv2.imshow("frame",frame)

    else:
        break


    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.waitKey(1) & 0xFF == ord('0'): 
        break

vid.release()
cv2.destroyAllWindows()