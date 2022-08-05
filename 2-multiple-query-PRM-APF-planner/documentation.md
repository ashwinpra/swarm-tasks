- An algorithm for making the grid 
- An algorithm for local path planning 
- An algorithm for handling queries 
- A pathfinding algorithm for queries 
- Collision-check algorithm 
- Postprocessing (Shortening and Smoothening)

- Define attractive and repulsive potentials and gradients 
- total U = Uattr + Urep 

- Use local planner to join the nodes, while checking collision also 
- Learn about Brushfire/ Wavefront planner

- Modify it such that we deal with only the green nodes, rather than using check function everywhere

## References Used
- https://github.com/abdurj/Local-Planner-Visualization-Project/blob/master/planners/planners.py
- https://github.com/KaleabTessera/PRM-Path-Planning/blob/master/main.py
- https://cs.gmu.edu/~kosecka/cs685/cs685-motion-planning.pdf
- https://d-nb.info/1123478015/34
- https://web.ics.purdue.edu/~rvoyles/Classes/ROSprogramming/Lectures/PathPlanning.pdf
- http://lavalle.pl/planning/bookbig.pdf
- https://github.com/nicholasRenninger/cSpaceViz_Gradient_Wavefront_planners
- https://www.researchgate.net/figure/Example-of-Artificial-Potential-Field-method_fig3_347823605
- https://thesai.org/Downloads/Volume10No8/Paper_76-Artificial_Potential_Field_Algorithm_Implementation.pdf
- https://medium.com/@rymshasiddiqui/path-planning-using-potential-field-algorithm-a30ad12bdb08
