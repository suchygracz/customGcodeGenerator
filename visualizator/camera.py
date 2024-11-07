import pygame as pg
from visualizator.matrixFunctions import *

class Camera:
    def __init__(self, render, position):
        self.render = render
        self.position = np.array([*position, 1.0])
        self.target = np.array([0, 0, 0, 1.0])  # Position of the object to orbit around
        self.distance_to_target = np.linalg.norm(self.position - self.target)  # Distance from the camera to the object

        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])
        self.h_fov = math.pi / 3
        self.v_fov = self.h_fov * (render.HEIGHT / render.WIDTH)
        self.near_plane = 0.1
        self.far_plane = 100
        self.moving_speed = 0.3
        self.rotation_speed = 0.015

        self.anglePitch = 0
        self.angleYaw = 0
        self.angleRoll = 0

        # Mouse control variables
        self.mouse_rotating = False  # Track whether mouse is rotating
        self.last_mouse_pos = None  # Track the last mouse position

    def control(self, events):
        key = pg.key.get_pressed()
        if key[pg.K_a]:
            self.position -= self.right * self.moving_speed
        if key[pg.K_d]:
            self.position += self.right * self.moving_speed
        if key[pg.K_w]:
            self.position += self.up * self.moving_speed
        if key[pg.K_s]:
            self.position -= self.up * self.moving_speed
        for event in events:
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up (zoom in)
                    self.position += self.forward * self.moving_speed * 10
                if event.button == 5:  # Scroll down (zoom out)
                    self.position -= self.forward * self.moving_speed * 10

            '''              
                if event.button == 1:  # Left mouse button pressed
                    self.mouse_rotating = True
                    self.last_mouse_pos = pg.mouse.get_pos()  # Capture initial mouse position

            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button released stop rotating
                    self.mouse_rotating = False

            if event.type == pg.MOUSEMOTION:
                if self.mouse_rotating:    # rotate acording to mouse movement
                    self.rotate_around_target(event)'''
    '''
    def rotate_around_target(self, event):
        # Get the current mouse position
        mouse_x, mouse_y = pg.mouse.get_pos()

        if self.last_mouse_pos:
            last_x, last_y = self.last_mouse_pos

            # Calculate the change in mouse position (delta)
            delta_x = mouse_x - last_x
            delta_y = mouse_y - last_y

            # Adjust camera yaw (horizontal rotation) and pitch (vertical rotation) based on mouse movement
            self.angleYaw += delta_x * self.rotation_speed
            self.anglePitch += delta_y * self.rotation_speed

            # Limit pitch to avoid flipping the camera (clamp pitch angle)
            self.anglePitch = np.clip(self.anglePitch, -np.pi / 2 + 0.1, np.pi / 2 - 0.1)

            # Update camera position based on yaw and pitch (spherical coordinates)
            self.update_camera_position()

        # Update the last mouse position
        self.last_mouse_pos = (mouse_x, mouse_y)

    def update_camera_position(self):
        # Use spherical coordinates to calculate the new position of the camera
        x = self.target[0] + self.distance_to_target * math.cos(self.anglePitch) * math.sin(self.angleYaw)
        y = self.target[1] + self.distance_to_target * math.sin(self.anglePitch)
        z = self.target[2] + self.distance_to_target * math.cos(self.anglePitch) * math.cos(self.angleYaw)

        # Update the camera position
        self.position = np.array([x, y, z, 1.0])

        # Keep the camera looking at the target
        self.forward = self.target - self.position
        self.forward /= np.linalg.norm(self.forward)  # Normalize the forward vector
'''
    def camera_yaw(self, angle):
        self.angleYaw += angle

    def camera_pitch(self, angle):
        self.anglePitch += angle

    def axiiIdentity(self):
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])

    def camera_update_axii(self):
        # rotate = rotate_y(self.angleYaw) @ rotate_x(self.anglePitch)
        rotate = rotate_x(self.anglePitch) @ rotate_y(self.angleYaw)  # this concatenation gives right visual
        self.axiiIdentity()
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def camera_matrix(self):
        self.camera_update_axii()
        return self.translate_matrix() @ self.rotate_matrix()

    def translate_matrix(self):
        x, y, z, w = self.position
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-x, -y, -z, 1]
        ])

    def rotate_matrix(self):
        rx, ry, rz, w = self.right
        fx, fy, fz, w = self.forward
        ux, uy, uz, w = self.up
        return np.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1]
        ])