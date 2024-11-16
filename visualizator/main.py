from visualizator.object3D import *
from visualizator.camera import *
from visualizator.projection import *
import pygame as pg
import numpy as np


class SoftwareRender:
    def __init__(self,listOfPoints):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 1600, 900
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.listOfPoints = listOfPoints
        self.create_objects(listOfPoints)


    def create_objects(self, listOfPoints):
        self.camera = Camera(self, [-5, 6, -55])
        self.projection = Projection(self)
        self.listOfPoints = listOfPoints
        #self.grid = Grid(self)
        #self.object = self.get_object_from_file('resources/t_34_obj.obj')
        print_path = [
            [1.0, 1.0, 1.0],
            [50.0, 1.0, 1.0],
            [50.0, 70.0, 1.0],
            [1.0, 70.0, 1.0],
            [1.0, 1.0, 1.0]
        ]
        self.object = getObjectFromPoints(self,listOfPoints)
        #self.grid = getGrid(self,256,5)
        #self.object.rotate_y(-math.pi / 4)


    def draw(self):
        self.screen.fill(pg.Color('black'))
        #self.grid.draw()
        self.object.draw()

    def run(self):
        while True:
            events = pg.event.get()
            self.draw()
            self.camera.control(events)
            self.object.movement(events)
            #self.grid.movement(events)
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(self.FPS)

"""
if __name__ == '__main__':
    app = SoftwareRender()
    app.run()"""