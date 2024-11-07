import math
from typing import Callable, List

from design.geometries import Point, linespace, polarToPoint
from visualizator import main

def rectangle(startPoint: Point, width: float, height: float) -> list:
    """

    generate a 2d XY rectangle starting at a given point 
    Args:
        startPoint (Point): point where the rectangle starts
        width (float): width of the rectangle
        height (float): height of the rectangle

    Returns:
        list:   list of points that define the rectangle (5 points as we have to draw 4 lines from p1 to p2, p2 to p3, p3 to p4, p4 to p1)

    """

    point2 = Point(x = startPoint.x + width, y = startPoint.y, z = startPoint.z)
    point3 = Point(x = startPoint.x + width, y = startPoint.y + height, z = startPoint.z)
    point4 = Point(x = startPoint.x, y = startPoint.y + height, z = startPoint.z)
    return [startPoint.copy(), point2, point3, point4, startPoint.copy()]

def arcXY(center: Point, radious: float, startAngle: float, endAngle: float, segments: int = 100) -> list:
    """

    generate a 2d XY arc starting at a given point
    Args:
        center (Point): point where the arc center is
        radious (float): radious of the arc
        startAngle (float): start angle of the arc
        endAngle (float): end angle of the arc
        segments (int): number of segments arc should be devided to
    Returns:
        list:   list of points that define the arc

    """

    angles = linespace(startAngle, endAngle, segments)
    return [polarToPoint(center, radious, angle) for angle in angles]

def varyingArc(center: Point, startRadious: float, endRadious: float, startAngle: float, endAngle: float, segments: int = 100) -> list:
    """

    generate a 2d XY arc starting at a given point
    Args:
        center (Point): point where the arc center is
        startRadious (float): start radious of the arc
        endRadious (float): end radious of the arc
        startAngle (float): start angle of the arc
        endAngle (float): end angle of the arc
        segments (int): number of segments arc should be devided to
    Returns:
        list:   list of points that define the arc

    """
    radious = linespace(startRadious, endRadious, segments)
    angles = linespace(startAngle, endAngle, segments)
    return [polarToPoint(center, radious, angle) for radious, angle in zip(radious, angles)]

def circle(center: Point, radious: float, segments: int = 100) -> list:
    """

    generate a 2d XY circle starting at a given point
    Args:
        center (Point): point where the circle center is
        radious (float): radious of the circle
        segments (int): number of segments circle should be devided to
    Returns:
        list:   list of points that define the circle

    """

    return arcXY(center, radious, 0, 2*3.14159265359, segments)

def spiral(center: Point, startRadious: float, endRadious: float, startAngle: float, endAngle: float, segments: int = 100) -> list:
    """

    generate a 2d XY spiral starting at a given point
    Args:
        center (Point): point where the spiral center is
        startRadious (float): start radious of the spiral
        endRadious (float): end radious of the spiral
        startAngle (float): start angle of the spiral
        endAngle (float): end angle of the spiral
        segments (int): number of segments spiral should be devided to
    Returns:
        list:   list of points that define the spiral

    """

    radious = linespace(startRadious, endRadious, segments)
    angles = linespace(startAngle, endAngle, segments)
    return [polarToPoint(center, radious, angle) for radious, angle in zip(radious, angles)]

def helix(center: Point, startRadious: float, endRadious: float, startAngle: float, endAngle: float, startZ: float, endZ: float, segments: int = 100) -> list:
    """

    generate a 3d XYZ helix starting at a given point
    Args:
        center (Point): point where the helix center is
        startRadious (float): start radious of the helix
        endRadious (float): end radious of the helix
        startAngle (float): start angle of the helix
        endAngle (float): end angle of the helix
        startZ (float): start z of the helix
        endZ (float): end z of the helix
        segments (int): number of segments helix should be devided to
    Returns:
        list:   list of points that define the helix

    """

    radious = linespace(startRadious, endRadious, segments)
    angles = linespace(startAngle, endAngle, segments)
    z = linespace(startZ, endZ, segments)
    return [Point(x = polarToPoint(center, radious, angle).x, y = polarToPoint(center, radious, angle).y, z = z) for radious, angle, z in zip(radious, angles, z)]

def generatePolarShape(center: Point, polar_function: Callable[[float], float], start_angle: float = 0, end_angle: float = 2 * math.pi, segments: int = 100) -> List[Point]:
    """
    Generates points that approximate a shape defined by a polar equation.

    Args:
        center (Point): The center of the shape.
        polar_function (Callable[[float], float]): A function that takes an angle (in radians) and returns the radius.
        start_angle (float): The start angle in radians.
        end_angle (float): The end angle in radians.
        segments (int): The number of segments to divide the shape.

    Returns:
        List[Point]: A list of Point objects that define the shape.
    """
    angles = linespace(start_angle, end_angle, segments)
    points = []

    for angle in angles:
        radius = polar_function(angle)
        point = polarToPoint(center, radius, angle)
        points.append(point)

    return points



def polar_function_1(angle: float) -> float:
    # First equation from the screenshot: r_eq(t) = r1 + r2 * cos(r3 * (t * 2π))
    r1 = 4
    r2 = 1
    r3 = 12
    return 10*(r1 + r2 * math.cos(r3 * angle))


def polar_function_2(angle: float) -> float:
    # Second equation: r = sin(a/b * θ) + 2
    a = 9
    b = -5
    return math.sin(a / b * angle) + 2


