# To visualise the grid better using OpenCV 
import cv2
import numpy as np

# 9x14 grid, we will multiply by 100 so that each cell is 100x100

grid = np.full((900,1400,3),255, dtype=np.uint8)

# Draw gridlines

for i in range(0,1500,100):
    cv2.line(grid, (i,0), (i,900), (0,0,0), 1)
for j in range(0,1000,100):
    cv2.line(grid, (0,j), (1400,j), (0,0,0), 1)

# Draw start and goal
for i in range (600,700):
    for j in range (100,200):
        grid[i,j] = (255,0,0)

for i in range (800,900):
    for j in range (1100,1200):
        grid[i,j] = (0,255,0)

# Draw obstacles and wind




cv2.imshow("Grid", grid)


cv2.waitKey(0)
cv2.destroyAllWindows()