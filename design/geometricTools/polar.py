import math

from pydantic import BaseModel
from typing import Optional
from math import pi,cos,sin
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

def polarToPoint(polar_point: PolarPoint) -> Point:
    """
    Convert polar coordinates to Cartesian coordinates
    Point XY coordinates of a point based on polar angle (radians) and radius from a centre point. The new Point has z = centre.z

    Args:
        polar_point (PolarPoint): A point in polar coordinates

    Returns:
        Point: A new Point object with x, y, and z coordinates calculated based on the given polar coordinates
    """

    return Point(polar_point.radious * math.cos(polar_point.angle), polar_point.radious * math.sin(polar_point.angle), )

