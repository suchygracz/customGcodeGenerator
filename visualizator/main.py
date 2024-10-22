from object3D import *
from camera import *
from projection import *
import pygame as pg


class SoftwareRender:
    def __init__(self):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 1600, 900
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.create_objects()

    def create_objects(self):
        self.camera = Camera(self, [-5, 6, -55])
        self.projection = Projection(self)
        #self.object = self.get_object_from_file('resources/t_34_obj.obj')
        print_path = [
            [0.0, 0.0, 0.0],
            [10.0, 0.0, 0.0],
            [10.0, 10.0, 0.0],
            [0.0, 10.0, 0.0],
            [0.0, 0.0, 10.0],
            [10.0, 0.0, 10.0],
            [10.0, 10.0, 10.0],
            [0.0, 10.0, 10.0]
        ]
        self.object = self.get_object_from_points(print_path)
        self.object.rotate_y(-math.pi / 4)

    def get_object_from_points(self, points):
        vertex = [point + [1] for point in points]  # Convert points to homogeneous coordinates by adding [1]
        lines = []

        # Create lines by connecting consecutive points
        for i in range(len(vertex) - 1):
            lines.append([i, i + 1])  # Line from point i to point i+1

        return Object3D(self, vertex, lines, is_line=True)
    def get_object_from_file(self, filename):
        vertex, faces = [], []
        with open(filename) as f:
            for line in f:
                if line.startswith('v '):
                    vertex.append([float(i) for i in line.split()[1:]] + [1])
                elif line.startswith('f'):
                    faces_ = line.split()[1:]
                    faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])
        return Object3D(self, vertex, faces)

    def draw(self):
        self.screen.fill(pg.Color('black'))
        self.object.draw()

    def run(self):
        while True:
            events = pg.event.get()
            self.draw()
            self.camera.control(events)
            self.object.movement(events)
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(self.FPS)


if __name__ == '__main__':
    app = SoftwareRender()
    app.run()