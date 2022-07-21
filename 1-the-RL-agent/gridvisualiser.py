# To visualise the grid better using OpenCV 
import cv2
import numpy as np
import gridworld


class GridVisualiser:
    def __init__(self):
        # 9x14 grid, we will multiply by 100 so that each cell is 100x100
        self.colors = {'blue': (255,0,0), 'red': (0,0,255), 'green': (0,255,0),'white': (255,255,255), 'black': (0,0,0), 'gray': (127,127,127), 'light_blue': (235,206,135)}
        self.gwTemplate = gridworld.GridWorld()


    def fill_cell(self,grid,y,x,color):
        grid[y*100:y*100+100,x*100:x*100+100] = color

    def fill_row(self,grid,y,color):
        grid[y*100:y*100+100,:] = color

    def draw_grid(self):
        grid = np.full((self.gwTemplate.WORLD_HEIGHT*100,self.gwTemplate.WORLD_WIDTH*100,3),255, dtype=np.uint8)

        # Fill obstacles
        for obstacle in self.gwTemplate.obstacles:
            pass
            self.fill_cell(grid, obstacle[0], obstacle[1], self.colors['gray'])

        # Wind in entire 4th 5th and 6th rows
        for i,strength in enumerate(self.gwTemplate.WIND):
            if(strength!=0):
                self.fill_row(grid,i,self.colors['light_blue'])

        # Draw start and goal
        self.fill_cell(grid,self.gwTemplate.START[0],self.gwTemplate.START[1],self.colors['blue'])
        self.fill_cell(grid,self.gwTemplate.GOAL[0],self.gwTemplate.GOAL[1],self.colors['green'])

        # Draw gridlines
        for i in range(0,self.gwTemplate.WORLD_WIDTH*100,100):
            cv2.line(grid, (i,0), (i,self.gwTemplate.WORLD_HEIGHT*100),self.colors['black'], 1)
        for j in range(0,self.gwTemplate.WORLD_HEIGHT*100,100):
            cv2.line(grid, (0,j), (self.gwTemplate.WORLD_WIDTH*100,j),self.colors['black'], 1)

        # Draw lines to represent wind
        for i,strength in enumerate(self.gwTemplate.WIND):
            if(strength==1):
                cv2.line(grid, (self.gwTemplate.WORLD_WIDTH*100-70,i*100+50), (self.gwTemplate.WORLD_WIDTH*100-30,i*100+50),self.colors['black'], 5)
            elif(strength==2):
                cv2.line(grid, (self.gwTemplate.WORLD_WIDTH*100-70,i*100+50), (self.gwTemplate.WORLD_WIDTH*100-30,i*100+50),self.colors['black'], 5)
                cv2.line(grid, (self.gwTemplate.WORLD_WIDTH*100-170,i*100+50), (self.gwTemplate.WORLD_WIDTH*100-130,i*100+50),self.colors['black'], 5)

        return grid 
    
    def show_path(self,grid,path):
        for i in range(len(path)):
            self.fill_cell(grid,path[i][0],path[i][1],self.colors['yellow'])
        cv2.imshow('Path',grid)


gridvisualiser = GridVisualiser()
grid = gridvisualiser.draw_grid()

cv2.imshow("Grid", grid)
cv2.waitKey(0)
cv2.destroyAllWindows()