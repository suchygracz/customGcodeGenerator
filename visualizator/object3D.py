import pygame as pg
from matrixFunctions import *
import numpy as np
from numba import njit


@njit(fastmath=True)
def any_func(arr, a, b):
    return np.any((arr == a) | (arr == b))


class Object3D:
    def __init__(self, render, vertices='', faces='', lines = '', is_line=False):
        self.render = render
        self.vertices = np.array(vertices)
        self.faces = faces
        self.lines = lines
        self.is_line = is_line
        self.translate([0.0001, 0.0001, 0.0001])

        self.font = pg.font.SysFont('Arial', 30, bold=True)
        self.color_faces = [(pg.Color('orange'), face) for face in self.faces]
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

        if self.is_line:  # Check if this object should be drawn as lines
            for line in self.faces:  # Faces store line indices in this case
                pg.draw.line(self.render.screen, pg.Color('white'), vertices[line[0]], vertices[line[1]], 1)
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
                    pg.draw.circle(self.render.screen, pg.Color('white'), vertex, 2)

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


class Axes(Object3D):
    def __init__(self, render):
        super().__init__(render)
        self.vertices = np.array([(0, 0, 0, 1), (1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)])
        self.faces = np.array([(0, 1), (0, 2), (0, 3)])
        self.colors = [pg.Color('red'), pg.Color('green'), pg.Color('blue')]
        self.color_faces = [(color, face) for color, face in zip(self.colors, self.faces)]
        self.draw_vertices = False
        self.label = 'XYZ'