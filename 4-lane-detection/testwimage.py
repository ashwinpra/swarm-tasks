import cv2 
import numpy as np 

frame = cv2.imread("./test.png")


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

def draw_box(frame,lines):
    # identify the leftmost and the rightmost lines, extend them so that they have same y coordinates, and draw a box around them
    if lines is not None:
    # choose the lines with highest x1 and lowest
        left_line = lines[0]
        right_line = lines[0]
        for line in lines:
            if line[0][0] < left_line[0][0]:
                left_line = line
            if line[0][0] > right_line[0][0]:
                right_line = line
        # extend the lines so that they have same y coordinates

        # draw the polygon
        x1, y1, x2, y2 = left_line[0]
        x3, y3, x4, y4 = right_line[0]
        # use equation of straight line to extend both lines such that higher y value is close to 0.6* height
        # similarly make lower y value close to 0.9 * height
        if(y1>y2):
            y1 = int(y1 - (y1-y2)*0.4)
            x1 = int(x1 - (x1-x2)*0.4)
        else:
            y1 = int(y1 + (y2-y1)*0.4)
            x1 = int(x1 + (x2-x1)*0.4)
        if(y3>y4):
            y3 = int(y3 - (y3-y4)*0.4)
            x3 = int(x3 - (x3-x4)*0.4)
        else:
            y3 = int(y3 + (y4-y3)*0.4)
            x3 = int(x3 + (x4-x3)*0.4)
        cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 3,cv2.LINE_AA)
        cv2.line(frame, (x3, y3), (x4, y4), (0, 255, 0), 3,cv2.LINE_AA)
        # must be passed in order: lower left, upper left, upper right, lower right
        vertices = np.array([[x1,y1],[x1,y2],[x3,y3],[x3,y4]],dtype=np.int32)
        # printcv2.fillPoly(frame, [vertices], (0,255,0))

        
    return frame

    print("left lines: ",left_line)
    print("----------------------------------------------------------------")
    print("right lines: ",right_line)
    return frame


lower_yellow = np.array([20,100,100],dtype=np.uint8)
upper_yellow = np.array([40,255,255],dtype=np.uint8)
lower_white = 220
upper_white = 255
#lower_white = np.array([0, 100, 100], dtype=np.uint8)
#upper_white = np.array([10, 255, 255], dtype=np.uint8)


y_lines = hough_with_mask(frame,lower_yellow,upper_yellow)
w_lines = hough_with_mask(frame,lower_white,upper_white)
# print("Yellow lines: ",y_lines)
# print("--------------------------------")
# print("White lines: ",w_lines)
# print("--------------------------------")
all_lines = np.concatenate((y_lines,w_lines),axis=0)
print("All lines: ",all_lines)

frame = draw_box(frame,all_lines)

cv2.imshow("frame",frame)

cv2.waitKey(0)
cv2.destroyAllWindows()