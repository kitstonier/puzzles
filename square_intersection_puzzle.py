class Coordinate:
    def __init__ (self, x, y):
        """
        2D cartesian coordinates class
        :param x: horizontal coordinate
        :type x: str, float or int
        :param y: vertical coordinate
        :type y: str, float or int
        """
        self.coord_x = self.convert_to_float(x)
        self.coord_y = self.convert_to_float(y)

    @staticmethod
    def convert_to_float (var):
        """
        :param var: value to convert
        :type var: str, int, float, boolean
        :return: float of input
        :rtype: float
        """
        if not isinstance(var, float):
            try:
                return float(var)
            except Exception as ex:
                print ex
        else:
            return var

    @property
    def x(self):
        """
        :return: x part of coordinate
        :rtype: float
        """
        return self.coord_x

    @x.setter
    def x(self, val):
        """
        :param val: x part of coordinate
        :type val: float
        """
        self.coord_x = self.convert_to_float(val)

    @property
    def y(self):
        """
        :return: x part of coordinate
        :rtype: float
        """
        return self.coord_y

    @y.setter
    def y(self, val):
        """
        :param val: y part of coordinate
        :type val: float
        """
        self.coord_y = self.convert_to_float(val)


class Line:

    def __init__(self, coord_a, coord_b):
        """
        A class to define a line or edge of a shape. Line is initially defined from the two end points.
        :param coord_a: end point of the line
        :type coord_a: Coordinate
        :param coord_b: end point of the line
        :type coord_b: Coordinate
        """

        # Get the factors for the line equation
        self.gradient, self.y_intercept = self.calculate_line_equation(coord_a, coord_b)
        # Store end point coordinates to class
        self.vertex_a = coord_a
        self.vertex_b = coord_b
        # Find maximum and minimums x and y position
        self.x_min = min(coord_a.x, coord_b.x)
        self.x_max = max(coord_a.x, coord_b.x)
        self.y_min = min(coord_a.y, coord_b.y)
        self.y_max = max(coord_a.y, coord_b.y)

    @staticmethod
    def calculate_line_equation(coord_a, coord_b):
        """
        :param coord_a: end point of the line
        :type coord_a: Coordinate
        :param coord_b: end point of the line
        :type coord_b: Coordinate
        :return: gradient and y intercept of the line
        :rtype: float
        """
        try:
            gradient = (coord_b.y - coord_a.y)/(coord_b.x - coord_a.x)
        except Exception as ex:
            print ex
            raise
        y_intercept = coord_a.y - (coord_a.x * gradient)
        return gradient, y_intercept


class Shape:

    def __init__(self, coordinate_string):
        """
        :param coordinate_string: A string of coordinates, coordinates in brackets seperated by a comma
        :type coordinate_string: str
        """
        # Edit string to seperate coordinates by semicolons and remove excess brackets
        coordinate_string = coordinate_string.replace('), (', ';')
        coordinate_string = coordinate_string .replace('),(', ';')
        coordinate_string = coordinate_string.replace('(', '')
        coordinate_string = coordinate_string.replace(')', '')

        # Split string by semi-colons to create and array of coordinate strings
        self.vertices = []
        for coord in coordinate_string.split(';'):
            # split coordinates by commas to give an array of cartesian coordinates
            # for the vertices of the shape.
            values = list(coord.split(','))
            # If only x value defined add y value of 0
            while len(values) < 2:
                values.append(0)
            # Create a coordinate class from values and append to an array
            # of vertices coordinates.
            self.vertices.append(Coordinate(values[0], values[1]))

        # Create line classes from the vertices with the assumption that
        # the vertices before and after each other in the array are connected.
        # Connect the last and first vertices together. Append the lines to an array
        # of edges of the shape.
        self.edges = []
        for i in xrange(len(self.vertices)):
            if i + 1 != len(self.vertices):
                self.edges.append(Line(self.vertices[i], self.vertices[i+1]))
            else:
                self.edges.append(Line(self.vertices[i], self.vertices[0]))


def calculate_line_intersection(line_1, line_2):
    """
    Function to calculate whether two lines intercept and where the interseption.
    :param line_1: One of the two lines
    :type line_1: Line
    :param line_2: One of the two lines
    :type line_2: Line
    :return: Flag as to whether the lines intersect each other, the coordinates where the intersect
    :rtype: boolean, Coordinate
    """
    # If two lines have the same gradient, check if parrallel or on the same line.
    if line_1.gradient == line_2.gradient:
        if line_2.y_intercept == line_1.y_intercept:
            # TODO: if on the same line check either of the endpoints are within the end points of the other line
            intercept = Coordinate(0, 0)
            return True, intercept
        else:
            intercept = Coordinate(0, 0)
            return False, intercept
    # Calculate the coordinates of where the two line intercept.
    x = (line_2.y_intercept - line_1.y_intercept)/(line_1.gradient - line_2.gradient)
    y = x * line_1.gradient + line_1.y_intercept
    # Calculate whether the two line intercept within the endpoints of each line.
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
            fl_intercept, coords =  calculate_line_intersection(shape_1_edge, shape_2_edge)
            print fl_intercept, coords.x, coords.y
            if fl_intercept:
                ax.annotate('({},{})'.format(round(coords.x,2), round(coords.y,2)),
                            xy=(coords.x, coords.y),
                            arrowprops=dict(facecolor='black', shrink=0.5))
    plt.show()

