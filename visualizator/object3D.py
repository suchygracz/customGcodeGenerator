import pygame as pg
from visualizator.matrixFunctions import *
import numpy as np
from transform.transformations import pointsIndiciesToStrRepresentation
#from numba import njit


"""@njit(fastmath=True)
def any_func(arr, a, b):
    return np.any((arr == a) | (arr == b))
"""

class Object3D:
    def __init__(self, render, vertices='', lines=None, command_type='shape', data=None):
        self.render = render
        self.vertices = np.array(vertices, dtype=np.float64) if vertices is not None else np.array([], dtype=np.float64)
        #self.faces = lines
        self.lines = np.array(lines) if lines else None
        self.data = data
        self.command_type = command_type
        self.translate([0.0001, 0.0001, 0.0001])

        self.font = pg.font.SysFont('Arial', 30, bold=True)
        #self.color_faces = [(pg.Color('orange'), face) for face in self.faces]
        self.movement_flag, self.draw_vertices = False, False
        self.label = ''

        # Mouse control variables
        self.mouse_rotating = False  # Track whether mouse is rotating
        self.last_mouse_pos = None  # Track the last mouse position



    def draw(self):
        self.screen_projection()
        

    def movement(self, events):
        key = pg.key.get_pressed()
        if key[pg.K_LEFT]:
            self.rotate_y(-(pg.time.get_ticks() % 0.01))
        if key[pg.K_RIGHT]:
            self.rotate_y((pg.time.get_ticks() % 0.01))
        if key[pg.K_UP]:
            self.rotate_x(-(pg.time.get_ticks() % 0.01))
        if key[pg.K_DOWN]:
            self.rotate_x((pg.time.get_ticks() % 0.01))
        '''
        if self.movement_flag:
            self.rotate_y(-(pg.time.get_ticks() % 0.005))
'''

        for event in events:
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button pressed
                    self.mouse_rotating = True
                    self.last_mouse_pos = pg.mouse.get_pos()  # Capture initial mouse position

            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    # Left mouse button released stop rotating
                    self.mouse_rotating = False

            if event.type == pg.MOUSEMOTION:
                if self.mouse_rotating:
                    # rotate acording to mouse movement
                    self.rotate_around_target(event)

    def rotate_around_target(self, event):
        # Get the current mouse position
        mouse_x, mouse_y = pg.mouse.get_pos()

        if self.last_mouse_pos:
            last_x, last_y = self.last_mouse_pos

            # Calculate the change in mouse position (delta)
            delta_x = mouse_x - last_x
            delta_y = mouse_y - last_y

            # Adjust camera yaw (horizontal rotation) and pitch (vertical rotation) based on mouse movement
            self.rotate_y(-(delta_x * (pg.time.get_ticks() % 0.005)))
            self.rotate_x(-(delta_y * (pg.time.get_ticks() % 0.005)))

            # Limit pitch to avoid flipping the camera (clamp pitch angle)
            #self.anglePitch = np.clip(self.anglePitch, -np.pi / 2 + 0.1, np.pi / 2 - 0.1)

            # Update camera position based on yaw and pitch (spherical coordinates)
            #self.update_camera_position()

        # Update the last mouse position
        self.last_mouse_pos = (mouse_x, mouse_y)

    def screen_projection(self):
        vertices = self.vertices @ self.render.camera.camera_matrix()
        vertices = vertices @ self.render.projection.projection_matrix
        vertices /= vertices[:, -1].reshape(-1, 1)
        vertices[(vertices > 2) | (vertices < -2)] = 0
        vertices = vertices @ self.render.projection.to_screen_matrix
        vertices = vertices[:, :2]

        if self.command_type == 'shape':
            # Draw the usual shape lines
            for line in self.lines:
                pg.draw.line(self.render.screen, pg.Color('#4848ed'), vertices[line[0]], vertices[line[1]], 1)

        elif self.command_type == 'moveWithNoExtrusion':
            # Draw moves with no extrusion as a lighter/thinner line
            for line in self.lines:
                pg.draw.line(self.render.screen, pg.Color('lightgray'), vertices[line[0]], vertices[line[1]], 1)

        elif self.command_type == 'stationaryExtrusion':
            # Draw stationary extrusion as small violet circles to represent extruded blobs
            # Use the extrusion amount to determine the size of the circle
            extrusion_amount = self.data[0]
            for vertex in vertices:
                pg.draw.circle(self.render.screen, pg.Color('violet'), vertex, int(extrusion_amount))

        elif self.command_type == 'retraction':
            # Draw retractions as a red marker to visually show where retraction occurs
            retraction_amount = self.data[0]
            for vertex in vertices:
                pg.draw.circle(self.render.screen, pg.Color('red'), vertex, int(retraction_amount))
    """        
        else:
            for index, color_face in enumerate(self.color_faces):
                color, face = color_face
                polygon = vertices[face]
                if not any_func(polygon, self.render.H_WIDTH, self.render.H_HEIGHT):
                    pg.draw.polygon(self.render.screen, color, polygon, 1)
                    if self.label:
                        text = self.font.render(self.label[index], True, pg.Color('white'))
                        self.render.screen.blit(text, polygon[-1])

        if self.draw_vertices:
            for vertex in vertices:
                if not any_func(vertex, self.render.H_WIDTH, self.render.H_HEIGHT):
                    pg.draw.circle(self.render.screen, pg.Color('blue'), vertex, 20)
    """

    def translate(self, pos):
        self.vertices = self.vertices @ translate(pos)

    def scale(self, scale_to):
        self.vertices = self.vertices @ scale(scale_to)

    def rotate_x(self, angle):
        self.vertices = self.vertices @ rotate_x(angle)

    def rotate_y(self, angle):
        self.vertices = self.vertices @ rotate_y(angle)

    def rotate_z(self, angle):
        self.vertices = self.vertices @ rotate_z(angle)

class Grid(Object3D):
    def __init__(self,render,vertices='', lines='', is_line=False, size: int = 100, spacing: int = 10):
        super().__init__(render, vertices, lines, is_line)

        self.size = size
        self.spacing = spacing
        self.lines = self.generate_grid_lines()

    def generate_grid_lines(self):
        # Generate lines on the XY plane spaced by `self.spacing`
        # This function should return a list of line segments
        lines = []
        half_size = self.size / 2
        current = -half_size
        while current <= half_size:
            # Horizontal line from -half_size to +half_size at y=current
            lines.append(((current, -half_size, 0), (current, half_size, 0)))  # Line coordinates (x, y, z)
            # Vertical line from -half_size to +half_size at x=current
            lines.append(((-half_size, current, 0), (half_size, current, 0)))
            current += self.spacing
        return lines

    def draw(self):
        """
        # Assuming you have some way to draw lines in your visualizer
        for line in self.lines:
            # draw_line(start_point, end_point) would be part of your visualizer
            start, end = line
            print(f"Drawing line from {start} to {end}")  # Replace with actual drawing logic
"""
        self.screen_projection()
"""
class Grid(Object3D):
    def __init__(self, render, size=10, step=1):
        super().__init__(render)
        self.size = size
        self.step = step
        self.color = pg.Color('grey')
        self.vertices = self.generate_grid_vertices()

    def generate_grid_vertices(self):
        vertices = []
        for x in range(-self.size, self.size + 1, self.step):
            vertices.append([x, -self.size, 0, 1])
            vertices.append([x, self.size, 0, 1])
        for y in range(-self.size, self.size + 1, self.step):
            vertices.append([-self.size, y, 0, 1])
            vertices.append([self.size, y, 0, 1])
        return np.array(vertices)

    def draw(self):
        self.screen_projection()
        for i in range(0, len(self.vertices), 2):
            start_pos = self.vertices[i][:2]
            end_pos = self.vertices[i + 1][:2]
            pg.draw.line(self.render.screen, self.color, start_pos, end_pos, 1)
"""
'''
class Grid:
    def __init__(self, render, size=10, step=1):
        self.render = render
        self.size = size
        self.step = step
        self.color = pg.Color('grey')
        self.vertices = self.generate_grid_vertices()

    def generate_grid_vertices(self):
        vertices = []
        for x in range(-self.size, self.size + 1, self.step):
            vertices.append([x, -self.size, 0, 1])
            vertices.append([x, self.size, 0, 1])
        for y in range(-self.size, self.size + 1, self.step):
            vertices.append([-self.size, y, 0, 1])
            vertices.append([self.size, y, 0, 1])
        return np.array(vertices)

    def draw(self):
        vertices = self.vertices @ self.render.camera.camera_matrix()
        vertices = vertices @ self.render.projection.projection_matrix
        vertices /= vertices[:, -1].reshape(-1, 1)
        vertices[(vertices > 2) | (vertices < -2)] = 0
        vertices = vertices @ self.render.projection.to_screen_matrix
        vertices = vertices[:, :2]

        for i in range(0, len(vertices), 2):
            start_pos = vertices[i]
            end_pos = vertices[i + 1]
            pg.draw.line(self.render.screen, self.color, start_pos, end_pos, 1)
'''

class Axes(Object3D):
    def __init__(self, render):
        super().__init__(render)
        self.vertices = np.array([(0, 0, 0, 1), (1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)])
        self.faces = np.array([(0, 1), (0, 2), (0, 3)])
        self.colors = [pg.Color('red'), pg.Color('green'), pg.Color('blue')]
        self.color_faces = [(color, face) for color, face in zip(self.colors, self.faces)]
        self.draw_vertices = False
        self.label = 'XYZ'

def getObjectFromPoints(render, command_type, data=None):
    """
    Create an Object3D instance from given points, command type, and additional data.

    Args:
        render: Reference to the SoftwareRender instance.
        points (list): List of points to create the object.
        command_type (str): The type of command, e.g., 'shape', 'moveWithNoExtrusion', 'stationaryExtrusion', 'retraction'.
        data (dict or Point, optional): Additional data for drawing, such as extrusion amount.

    Returns:
        Object3D: An Object3D instance representing the given points and command type.
    """
    if command_type == 'shape':
        points = pointsIndiciesToStrRepresentation(data)
        print(points)
        vertex = [point + [1] for point in points]  # Convert points to homogeneous coordinates by adding [1]
    elif command_type == 'moveWithNoExtrusion':
        print(data)
        points = data
        vertex = [point + [1] for point in points]
    elif command_type == 'stationaryExtrusion':
        print(data)
        vertex = [data[1] + [1]]
    elif command_type == 'retraction':
        print(data)
        vertex = [data[1] + [1]]

    lines = []

    # Create lines by connecting consecutive points if this is a shape or a move command
    if command_type in ['shape', 'moveWithNoExtrusion']:
        for i in range(len(vertex) - 1):
            lines.append([i, i + 1])

    # Return an Object3D with the appropriate command type and data
    return Object3D(render, vertex, lines, command_type, data)


"""
def getGrid(self, size: int = 10, spacing: int = 1):

    return Grid(self, vertices=[], lines=[], is_line=True, size=size, spacing=spacing)
    """

def getGrid(self, size: int = 10, spacing: int = 5):
    vertices = []
    lines = []
    half_size = size / 2
    nOfLines = int(size / spacing)

    # Generate grid vertices and lines
    for i in range(nOfLines + 1):
        position = -half_size + i * spacing
        # Horizontal lines
        vertices.append([position, -half_size, 0, 1])
        vertices.append([position, half_size, 0, 1])
        lines.append([len(vertices) - 2, len(vertices) - 1])

        # Vertical lines
        vertices.append([-half_size, position, 0, 1])
        vertices.append([half_size, position, 0, 1])
        lines.append([len(vertices) - 2, len(vertices) - 1])

    return Object3D(self, vertices, lines, is_line=False)