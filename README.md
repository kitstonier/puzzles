# Puzzles
Sample code of solutions to puzzles

```
import square_intersection_puzzle
from square_intersection_puzzle import Shape
import matplotlib.pyplot as plt
import matplotlib
import seaborn
matplotlib.rcParams['figure.figsize'] = (15, 10)
```

# Shape Intersection Puzzle

The puzzle is determine whether two shapes cross. To do this the software looks to see whether any of the edges of the shape intercept with any edge of the other shape. This is then shown on a graph, marking all points of intersection.

```
coord_string = "(0,1), (1,10), (1.2,1.2), (5,3), (2,-4)"
shape_1 = Shape(coord_string)
coord_string = "(0,0), (1,3), (2,1)"
shape_2 = Shape(coord_string)
ax = plt.gca()
for shape_1_edge in shape_1.edges:
    plt.plot([shape_1_edge.vertex_a.x, shape_1_edge.vertex_b.x],
             [shape_1_edge.vertex_a.y, shape_1_edge.vertex_b.y],
             'b')
    for shape_2_edge in shape_2.edges:
        plt.plot([shape_2_edge.vertex_a.x, shape_2_edge.vertex_b.x],
                 [shape_2_edge.vertex_a.y, shape_2_edge.vertex_b.y],
                 'r')
        fl_intercept, coords =  square_intersection_puzzle.calculate_line_intersection(shape_1_edge, shape_2_edge)
        if fl_intercept:
            ax.annotate('({},{})'.format(round(coords.x,2), round(coords.y,2)),
                        xy=(coords.x, coords.y),)
plt.show()
```
