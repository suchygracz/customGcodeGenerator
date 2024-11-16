import math

from numpy.ma.core import angle
from pydantic import BaseModel
from typing import Optional
from math import pi,cos,sin, atan2
from ..point import Point

class PolarPoint(BaseModel):
    """
    A point in polar coordinates

    Attributes
        radious (float): The distance of a point from the origin
        angle (float): The angle of the point from the x-axis
    """

    radious: Optional[float] = None
    angle: Optional[float] = None

def polarToPoint(center: Point, radious: float, angle: float) -> Point:
    """
    Convert polar coordinates to Cartesian coordinates
    Point XY coordinates of a point based on polar angle (radians) and radius from a centre point. The new Point has z = centre.z

    Args:
        center (Point): the center of polar coordinates
        radious (float): The distance of a point from the origin
        angle (float): The angle of the point from the x-axis

    Returns:
        Point: A new Point object with x, y, and z coordinates calculated based on the given polar coordinates
    """

    return Point(x = center.x + radious*cos(angle), y = center.y + radious*sin(angle), z = center.z)

def pointToPolar(origin: Point, point: Point) -> PolarPoint:
    """
    function converting a cartesian coordinate point to polar coordinates point
    Args:
        origin (Point): point representing origin point of polar coordinates
        point (Point): point to be converted to polar coordinates

    Returns:
        PolarPoint: converted polar coordinates point
    """

    return PolarPoint(radious= ((point.x - origin.x)**2 + (point.y - origin.y)**2)**0.5, angle = atan2(point.y - origin.y, point.x - origin.x))

def rotatePolarPoint(polarPoint: PolarPoint, angle: float) -> PolarPoint:
    """
    function rotating a polar point by a given angle
    Args:
        polarPoint (PolarPoint): point to be rotated
        angle (float): angle of rotation

    Returns:
        PolarPoint: rotated point
    """

    return PolarPoint(radious = polarPoint.radious, angle = polarPoint.angle + angle)