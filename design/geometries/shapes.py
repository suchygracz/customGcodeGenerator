from design.geometries import Point
import typing


def rectangle(startPoint: Point, width: float, height: float) -> list:
    """

    generate a 2d XY rectangle starting at a given point 
    Args:
        startPoint (Point):
        width (float):
        height (float):

    Returns:
        list:

    """
    point1 = Point(startPoint.x, startPoint.y)
    point2 = Point(startPoint.x + width, startPoint.y)
    point3 = Point(startPoint.x + width, startPoint.y + height)
    point4 = Point(startPoint.x, startPoint.y + height)
    return [startPoint.copy(), point2, point3, point4, startPoint.copy()]
