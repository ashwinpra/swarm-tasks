import numpy as np
import cv2

def inRange(img,point):
    #checks if point is within the range of the image's dimensions
    return (point[0]>=0 and point[0]<img.shape[0] and point[1]>=0 and point[1]<img.shape[1])

def aStar(self, img):
        n, m = img.shape[:2]    # Height and Width of the maze
        parent = np.zeros((n,m,2))  # Keeping track of the parent pixels
        visited = []    # Keepinig a list of visited pixels so that we dont visit the same pixel again
        current = self.start
        visited.append(current)
        distance = np.full((n,m), np.inf)   # initialising the distance of every pixel to infinity
        pixel_distance = np.full((n,m), np.inf)
        distance[self.start] = 0
        pixel_distance[self.start] = 0
         # Loop runs until we reach the target 
        while True:
            if current != self.end:
                for (i, j) in [(-1,0), (1,0), (0,-1), (0,1)]:   # Visiting all 4 neighboring pixels

                    # Code for visualisation
                    if img.shape[0] < 100:
                        showImg = cv2.resize(img, (500,500), interpolation=cv2.INTER_AREA)
                        cv2.imshow("A*", showImg)
                        cv2.waitKey(1)
                    else:
                        cv2.imshow("A*", img)

                    newpoint = (current[0]+i, current[1]+j)
                    # Checking if the pixel lies in the valid path or not
                    if inRange(img, newpoint) and not (img[newpoint] == BLACK).all():
                        pixel_distance[newpoint] = pixel_distance[current] + find_dist(newpoint, current)
                        if distance[newpoint] > pixel_distance[newpoint]+ find_dist(newpoint, current) + find_dist(newpoint, self.end):
                            distance[newpoint] = pixel_distance[newpoint] + find_dist(newpoint, current)+ find_dist(newpoint, self.end)
                            img[newpoint] = COLOR2
                            parent[newpoint] =  current
                            visited.append(newpoint)
                # Choosing the pixel with the least current distance for analysis in the next cycle
                    min = np.inf
                for point in visited:
                    if distance[point] < min:
                        min = distance[point]
                        current = point
                if not len(visited):
                    return None, None
                else:
                    visited.remove(current)
            else:
                img[self.end] = BLUE
                distance[self.end] = distance[current] +find_dist(self.end, current)
                return distance[self.end], parent

    def trackaStar(self):
        img = np.copy(self.inimg)       # Making a copy of the maze for the algorithm to work on
        dist, parent = self.aStar(img)   # Running the algorithm
        # Tracking the final path
        current = tuple(list(map(int, parent[self.end])))
        dist = 1
        while current != self.start:
            dist += 1
            img[current] = GREEN
            current = tuple(list(map(int, parent[current])))
            # Scaling the right maze
            if img.shape[0] < 100:
                showImg = cv2.resize(img, (500,500), interpolation=cv2.INTER_AREA)
                cv2.imshow("A*", showImg)
                cv2.waitKey(1)
            else:
                cv2.imshow("A*", img)
        # Printing the final
        print("Distance: " + str(dist) + " pixels")