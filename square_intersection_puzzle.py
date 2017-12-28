import math

class Coordinate:

    def __init__ (self, x, y):
        self.coord_x = self.convert_to_float(x)
        self.coord_y = self.convert_to_float(y)

    def convert_to_float (self, var):
        if not isinstance(var, float):
            try:
                return float(var)
            except Exception as ex:
                print ex
        else:
            return var

    @property
    def x (self):
        return self.coord_x

    @x.setter
    def x (self, val):
        self.coord_x = self.convert_to_float(val)

    @property
    def y(self):
        return self.coord_y

    @y.setter
    def y(self, val):
        self.coord_y = self.convert_to_float(val)

class Line:

    def __init__(self, coord_a, coord_b):
        self.gradient, self.y_intercept = self.calculate_line_equation(coord_a, coord_b)
        self.vertex_a = coord_a
        self.vertex_b = coord_b
        self.x_min = min(coord_a.x, coord_b.x)
        self.x_max = max(coord_a.x, coord_b.x)
        self.y_min = min(coord_a.y, coord_b.y)
        self.y_max = max(coord_a.y, coord_b.y)


    def calculate_line_equation(self, coord_a, coord_b):
        try:
            gradient = (coord_b.y - coord_a.y)/(coord_b.x - coord_a.x)
        except Exception as ex:
            print ex
            raise
        y_intercept = coord_a.y - (coord_a.x * gradient)
        return gradient, y_intercept


class Shape:

    def __init__(self, coordinate_string):
        coordinate_string = coordinate_string.replace('), (', ';')
        coordinate_string = coordinate_string .replace('),(', ';')
        coordinate_string = coordinate_string.replace('(', '')
        coordinate_string = coordinate_string.replace(')', '')
        self.vertices = []
        for coord in coordinate_string.split(';'):
            values = list(coord.split(','))
            while len(values)<2:
                values.append(0)

            self.vertices.append(Coordinate(values[0], values[1]))
        self.edges = []
        for i in xrange(len(self.vertices)):
            if i + 1 != len(self.vertices):
                self.edges.append(Line(self.vertices[i], self.vertices[i+1]))
            else:
                self.edges.append(Line(self.vertices[i], self.vertices[0]))

def calculate_line_intersection(line_1, line_2):
    if line_1.gradient == line_2.gradient:
        if line_2.y_intercept == line_1.y_intercept:
            intercept = Coordinate(0, 0)
            return True, intercept
        else:
            intercept = Coordinate(0, 0)
            return False, intercept
    x = (line_2.y_intercept - line_1.y_intercept)/(line_1.gradient - line_2.gradient)
    y = x * line_1.gradient + line_1.y_intercept
    # print "x", x
    # print "x lim", line_1.x_min, line_1.x_max, line_2.x_min , line_2.x_max
    # print "y", y
    # print "y lim", line_1.y_min, line_1.y_max, line_2.y_min, line_2.y_max
    # print (line_1.x_min <= x <= line_1.x_max), (line_2.x_min <= x <= line_2.x_max), (line_1.y_min <= y <= line_1.y_max), (line_2.y_min <= y <= line_2.y_max)
    if ((line_1.x_min <= x <= line_1.x_max) and
            (line_2.x_min <= x <= line_2.x_max) and
            (line_1.y_min <= y <= line_1.y_max) and
            (line_2.y_min <= y <= line_2.y_max)):
        intercept = Coordinate(x,y)
        print intercept.x, x
        return True, intercept
    else:
        intercept = Coordinate(0, 0)
        return False, intercept


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    # shape_1 = raw_input("Input coordinates of the vertices of shape 1 in format (0,0), (1,1)...")
    coord_string = "(0,1), (1,1), (2,2)"
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
            fl_intercept, coords =  calculate_line_intersection(shape_1_edge, shape_2_edge)
            print fl_intercept, coords.x, coords.y
            if fl_intercept:
                ax.annotate('({},{})'.format(round(coords.x,2), round(coords.y,2)),
                            xy=(coords.x, coords.y),
                            arrowprops=dict(facecolor='black', shrink=0.5))
    plt.show()