import unittest
from design.geometricTools.baseTools import move, scale, rotate
from design.geometries.shapes import varyingArc, spiral, helix, polygon, circle, rectangle, square
from design.geometries.curves import sinusoidalWave, squareWave, tringleWave, cubic_bezier_curve, bezier_curve_de_casteljau
from design.geometries.shapes import generatePolarShape, polar_function_1, polar_function_2
from math import pi
from design.geometricTools.vector import Vector
from transform.transformations import pointsIndiciesToStrRepresentation
from design.point import Point
from visualizator import main

class TestTransformations(unittest.TestCase):
    def setUp(self):
        self.shapes = [
            varyingArc(Point(x=0, y=0, z=0), 30, 90, 0, 3, 100),
            spiral(Point(x=0, y=0, z=0), 30, 90, 0, 13, 100),
            helix(Point(x=0, y=0, z=0), 30, 30, 0, 33, 0, 100, 100),
            polygon(Point(x=0, y=0, z=0), 30, 5),
            circle(Point(x=0, y=0, z=0), 30),
            rectangle(Point(x=0, y=0, z=0), 30, 30),
            square(Point(x=0, y=0, z=0), 30),
            sinusoidalWave(Point(x=0, y=0, z=0), 0, 5, 10, 15),
            squareWave(Point(x=0, y=0, z=0), 0, 5, 10, 15),
            tringleWave(Point(x=0, y=0, z=0), 0, 5, 10, 15),
            cubic_bezier_curve(Point(x=0, y=0), Point(x=10, y=20), Point(x=15, y=5), Point(x=20, y=30), 200),
            bezier_curve_de_casteljau([Point(x=0, y=0), Point(x=10, y=20), Point(x=15, y=5), Point(x=20, y=30), Point(x=25, y=10), Point(x=30, y=50), Point(x=40, y=3)], 200),
            generatePolarShape(Point(x=0, y=0, z=0), polar_function_1, start_angle=0, end_angle=2 * pi, segments=100),
            generatePolarShape(Point(x=0, y=0, z=0), polar_function_2, start_angle=0, end_angle=10 * pi, segments=1000)
        ]

    def test_transformations(self):
        for shape in self.shapes:
            with self.subTest(shape=shape):
                moved_shape = move(shape, Vector(x=10, y=10, z=10))
                #scaled_shape = scale(shape, 2, 'xy')
                #rotated_shape = rotate(shape, pi/4, 'z')
                #self.assertIsNotNone(moved_shape)
                #self.assertIsNotNone(scaled_shape)
                #self.assertIsNotNone(rotated_shape)

    def test_visualizator(self):
        for shape in self.shapes:
            with self.subTest(shape=shape):
                #extracredPoints = shape['shape']
                listOfPoints = pointsIndiciesToStrRepresentation(shape)
                softwareRender = main.SoftwareRender(listOfPoints)
                self.assertIsNotNone(softwareRender)
                softwareRender.run()

if __name__ == '__main__':
    unittest.main()