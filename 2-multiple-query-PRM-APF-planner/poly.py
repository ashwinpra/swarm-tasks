import zipapp
from matplotlib.path import Path
import matplotlib.pyplot as plt
import numpy as np

tupVerts = [(5,11),(14,5),(11,20)]


point=[(6,12)]

fig,ax = plt.subplots()

p = Path(tupVerts) # make a polygon
p.contains_points(point)



fig.show()


