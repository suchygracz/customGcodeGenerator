import pytest

from design.geometricTools.extraTools import nonPlanarVase, vaseMode, solidLayerInfill
from design.geometricTools.vector import Vector
from design.geometries.curves import sinusoidalWave, squareWave, tringleWave, cubic_bezier_curve, bezier_curve_de_casteljau, cardinal_spline, nurbs_curve
from design.geometries.shapes import varyingArc, spiral, helix, polar_function_1, polar_function_2, generatePolarShape, polygon, circle, rectangle, square
from design.layer import Layer
from transform.transformations import pointsIndiciesToStrRepresentation, parseStepsToGcode
from design.geometricTools.baseTools import move, scale, rotate
from design.point import Point
from design.layer import Layer
import math
from math import pi, sin, cos
from visualizator import main
from design.directCommands.commands import moveWithNoExtrusion, stationaryExtrusion, retraction


# File: tests/test_point_and_polar.py


from design.geometricTools.polar import  PolarPoint, polarToPoint, pointToPolar, rotatePolarPoint
from math import pi, sqrt, atan2

# Tests for Point class
def test_point_initialization():
    point = Point(x=1.0, y=2.0, z=3.0)
    assert point.x == 1.0
    assert point.y == 2.0
    assert point.z == 3.0
    assert point.e is None

def test_point_str():
    point = Point(x=1.0, y=2.0, z=3.0)
    assert str(point) == "[1.0, 2.0, 3.0]"

def test_point_list_representation():
    point = Point(x=1.0, y=2.0, z=3.0)
    assert point.listRepresentation() == [1.0, 2.0, 3.0]

# Tests for PolarPoint class
def test_polar_point_initialization():
    polar_point = PolarPoint(radious=5.0, angle=pi/4)
    assert polar_point.radious == 5.0
    assert polar_point.angle == pi / 4

# Tests for conversion functions
def test_polar_to_point():
    center = Point(x=0, y=0, z=0)
    radious = 5.0
    angle = pi / 4

    cartesian_point = polarToPoint(center, radious, angle)

    assert pytest.approx(cartesian_point.x, 0.01) == 5.0 * 2 ** 0.5 / 2
    assert pytest.approx(cartesian_point.y, 0.01) == 5.0 * 2 ** 0.5 / 2
    assert cartesian_point.z == center.z

def test_point_to_polar():
    origin = Point(x=0, y=0, z=0)
    point = Point(x=3.0, y=4.0, z=0)

    polar_point = pointToPolar(origin, point)

    # Expected radius is sqrt(3^2 + 4^2) = 5
    assert pytest.approx(polar_point.radious, 0.01) == 5.0
    # Expected angle is atan2(4, 3)
    assert pytest.approx(polar_point.angle, 0.01) == atan2(4, 3)

def test_rotate_polar_point():
    polar_point = PolarPoint(radious=5.0, angle=pi / 4)
    angle = pi / 4

    rotated_polar_point = rotatePolarPoint(polar_point, angle)

    # The radius should not change
    assert rotated_polar_point.radious == polar_point.radious
    # The angle should be increased by pi / 4
    assert pytest.approx(rotated_polar_point.angle, 0.01) == pi / 2

def test_rectangle_creation():
    """ Test the creation of a simple rectangle. """
    start_point = Point(x=0, y=0, z=0)
    width = 5.0
    height = 3.0

    rect = rectangle(start_point, width, height)['shape']

    # Verify that the rectangle has five points (to form a closed shape)
    assert len(rect) == 5

    # Verify each point's coordinates
    assert rect[0] == Point(x=0, y=0, z=0)  # Start point
    assert rect[1] == Point(x=5, y=0, z=0)  # Width along x-axis
    assert rect[2] == Point(x=5, y=3, z=0)  # Height along y-axis
    assert rect[3] == Point(x=0, y=3, z=0)  # Back to original x position
    assert rect[4] == Point(x=0, y=0, z=0)  # Closed shape, back to start

def test_rectangle_move():
    """ Test moving the rectangle by a given vector. """
    start_point = Point(x=0, y=0, z=0)
    width = 5.0
    height = 3.0
    rect = rectangle(start_point, width, height)

    # Move the rectangle by a vector (2, 3, 1)
    move_vector = Vector(x=2, y=3, z=1)
    moved_rect = move(rect, move_vector)['shape']

    # Verify that all points are moved correctly
    expected_points = [
        Point(x=2, y=3, z=1),
        Point(x=7, y=3, z=1),
        Point(x=7, y=6, z=1),
        Point(x=2, y=6, z=1),
        Point(x=2, y=3, z=1)
    ]
    for i in range(len(moved_rect)):
        assert moved_rect[i] == expected_points[i]

def test_rectangle_scale():
    """ Test scaling the rectangle around its center. """
    start_point = Point(x=0, y=0, z=0)
    width = 4.0
    height = 2.0
    rect = rectangle(start_point, width, height)

    # Scale the rectangle by a factor of 2
    scaled_rect = scale(rect, scalar=2.0, axis='xy')['shape']

    # Verify that the points have been scaled properly
    expected_points = [
        Point(x=-2, y=-1, z=0),
        Point(x=6, y=-1, z=0),
        Point(x=6, y=3, z=0),
        Point(x=-2, y=3, z=0),
        Point(x=-2, y=-1, z=0)
    ]

    for i in range(len(scaled_rect)):
        assert scaled_rect[i] == expected_points[i]

def test_rectangle_rotate():
    """ Test rotating the rectangle around its center. """
    start_point = Point(x=0, y=0, z=0)
    width = 4.0
    height = 2.0
    rect = rectangle(start_point, width, height)

    # Rotate the rectangle by 90 degrees (pi/2 radians) around the z-axis
    rotated_rect = rotate(rect, angle=math.pi/2, axis='z')['shape']

    # Verify that the points have been rotated correctly
    # Due to precision issues in floating-point calculations, we'll use a tolerance
    expected_points = [
        Point(x=3, y=-1, z=0),
        Point(x=3, y=3, z=0),
        Point(x=1, y=3, z=0),
        Point(x=1, y=-1, z=0),
        Point(x=3, y=-1, z=0)
    ]
    print(rotated_rect)
    tolerance = 1e-6
    for i in range(len(rotated_rect)):
        assert abs(rotated_rect[i].x - expected_points[i].x) < tolerance
        assert abs(rotated_rect[i].y - expected_points[i].y) < tolerance
        assert abs(rotated_rect[i].z - expected_points[i].z) < tolerance

if __name__ == "__main__":
    pytest.main()

