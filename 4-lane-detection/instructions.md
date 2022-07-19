# 4 Lane Detection 

## 4.1 Introduction 

Lane detection is of utmost importance in autonomous robots. The vehicle must know where it is supposed to drive. Lane can be detected using basic Image Processing tricks on the visual feed of the robot. For suggested reading, refer to Reading Task resources on Image Segmentation. Lane detection isn’t an easy task as the color of the lane and the lighting conditions may vary. Lane markers aren’t always straight. So one must use Line detection algorithms with caution. 

## 4.2 The Task (20 + 30 + 50%) 

For this task, there are three levels, each having a video file. The objective is to process the video, detect lane and annotate the driving area, as shown in Figure 3. 

- Level 1 has a straight lane with white color. 20% 

- Level 2 has a straight lane with colors other than the white present. 30% 

- Level 3 has curved lanes with variable lighting conditions. 50% 

  

## 4.3 Submission 

Your submissions will be judged based on how accurately and reliably your code can detect lanes and driving area. Download the videos mentioned in the task section, and process and annotate them. Export the annotated videos using Open CV. 

1. You are expected to write python or C++ code and use Open-CV for this task. Code must be documented and readable. 
2. You must export the videos after processing them using Open-CV, keep them in a drive folder and send link for the same. Output videos must be named Level1, Level2 and Level3 respectively. 
3. You are expected to document your approach as we will ask you to explain your approach during personal interview.