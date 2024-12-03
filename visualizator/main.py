from visualizator.object3D import *
from visualizator.camera import *
from visualizator.projection import *
from design.point import Point
import pygame as pg
import numpy as np



class SoftwareRender:
    def __init__(self,listOfSteps):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 1600, 900
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.listOfSteps = listOfSteps
        self.objects = []
        self.create_objects(listOfSteps)


    def create_objects(self, listOfSteps):
        self.camera = Camera(self, [-5, 6, -55])
        self.projection = Projection(self)
        #self.grid = Grid(self)
        last_point = [0,0,0]

        for step in listOfSteps:
            command_type, data = next(iter(step.items()))
            match command_type:
                case 'shape':
                    self.objects.append(getObjectFromPoints(self, command_type, data))
                    last_point = pointsIndiciesToStrRepresentation(data)[-1]
                case 'moveWithNoExtrusion':
                    toGoPoint = pointsIndiciesToStrRepresentation(data)
                    data = [last_point]
                    data += toGoPoint
                    self.objects.append(getObjectFromPoints(self, command_type, data))
                    last_point = data[-1]
                case 'stationaryExtrusion':
                    ammount = data['amount']
                    data2 = []
                    data2.append(ammount)
                    data2.append(last_point)

                    self.objects.append(getObjectFromPoints(self, command_type, data2))

                case 'retraction':
                    ammount = data
                    data2 = []
                    data2.append(ammount)
                    data2.append(last_point)
                    self.objects.append(getObjectFromPoints(self, command_type, data2))

        #self.grid = getGrid(self,256,5)
        #self.object.rotate_y(-math.pi / 4)


    def draw(self):
        self.screen.fill(pg.Color('white'))
        #self.grid.draw()
        for obj in self.objects:
            obj.draw()


    def run(self):
        while True:
            events = pg.event.get()
            self.draw()
            self.camera.control(events)
            for object in self.objects:
                object.movement(events)
            #self.object.movement(events)
            #self.grid.movement(events)
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(self.FPS)

"""
if __name__ == '__main__':
    app = SoftwareRender()
    app.run()"""

def visualize(listOfSteps):
    app = SoftwareRender(listOfSteps)
    app.run()