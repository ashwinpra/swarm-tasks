import cv2 
import numpy as np 

level = int(input("Enter level: "))
vid = cv2.VideoCapture(f"./4-lane-detection/raw-videos/level{level}.mp4")

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

def extend_line(x1,y1,x2,y2):
    '''
        use equation of straight line to extend the line such that:
        higher y value is close to 0.65* height
        similarly make lower y value close to 0.95 * height
        (higher and lower in the visual sense)
    '''
    m = (y2-y1)/(x2-x1)
    c = y1 - m*x1
    if(y1>y2):
        y1_new = int(0.65*frame.shape[0])
        x1_new = int((y1_new-c)/m)

        y2_new = int(0.95*frame.shape[0])
        x2_new = int((y2_new-c)/m)
    else:
        y2_new = int(0.65*frame.shape[0])
        x2_new = int((y2_new-c)/m)

        y1_new = int(0.95*frame.shape[0])
        x1_new = int((y1_new-c)/m)
    return x1_new,y1_new,x2_new,y2_new

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

        #print(f"left line: {left_line}")
        #print(f"right line: {right_line}")
        # draw the polygon
        x1, y1, x2, y2 = left_line[0]
        x3, y3, x4, y4 = right_line[0]
       
        x1,y1,x2,y2 = extend_line(x1,y1,x2,y2)
        x3,y3,x4,y4 = extend_line(x3,y3,x4,y4)


        cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255),5,cv2.LINE_AA)
        cv2.line(frame, (x3, y3), (x4, y4), (0, 0, 255),5,cv2.LINE_AA)
        # must be passed in order: lower left, upper left, upper right, lower right
        vertices = np.array([[x1,y1],[x2,y2],[x3,y3],[x4,y4]],dtype=np.int32)
        cv2.fillPoly(frame, [vertices], (144,238,144))

        
    return frame

lower_yellow = np.array([20,100,100],dtype=np.uint8)
upper_yellow = np.array([40,255,255],dtype=np.uint8)
lower_white = 220
upper_white = 255

last_y_lines = None
last_w_lines = None

while 1:
    ret, frame = vid.read() 

    if ret:
        y_lines = hough_with_mask(frame,lower_yellow,upper_yellow)
        w_lines = hough_with_mask(frame,lower_white,upper_white)
        print(type(y_lines))
        if(y_lines is not None):
            last_y_lines = y_lines
        if(w_lines is not None):
            last_w_lines = w_lines
        if(y_lines is None and last_y_lines is not None):
            y_lines = last_y_lines
        if(w_lines is None and last_w_lines is not None):
            w_lines = last_w_lines
        if(y_lines is not None and w_lines is not None):
            all_lines = np.concatenate((y_lines,w_lines),axis=0)
        elif(y_lines is None):
            all_lines = w_lines
        elif(w_lines is None):
            all_lines = y_lines

        frame = draw_box(frame,all_lines)
        #frame = draw(frame,y_lines)
        #frame = draw(frame,w_lines)
        cv2.imshow("frame",frame)

    else:
        break


    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.waitKey(1) & 0xFF == ord('0'): 
        break

vid.release()
cv2.destroyAllWindows()