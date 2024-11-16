from design.geometricTools.polar import pointToPolar, rotatePolarPoint
from design.geometries import Point, linespace, polarToPoint, PolarPoint
from math import sin, cos, pi, tau
from typing import List

from design.geometricTools.decorators import geometryDecorator
from math import sin, cos, pi, tau

@geometryDecorator
def sinusoidalWave(
        startPoint: Point,
        direction_polar: float,
        amplitude: float,
        periodLength: float,
        periods: int,
        segmentsPerPeriod: int = 50,
        extraHalfPeriod: bool = False,
        phaseShift: float = 0,
) -> List[Point]:
    """
    Generate a sine wave in Cartesian coordinates using polar coordinates for rotation.

    Parameters:
    - startPoint (Point): The starting point of the sine wave.
    - direction_polar (float): The polar angle in radians that determines the direction of the wave.
    - amplitude (float): The amplitude of the wave.
    - periodLength (float): The length of each period of the wave.
    - periods (int): The number of periods in the wave.
    - segmentsPerPeriod (int): The number of line segments per period. Defaults to 16.
    - extraHalfPeriod (bool): Whether to add an extra half period. Defaults to False.
    - phaseShift (float): The phase shift of the wave. Defaults to 0.

    Returns:
    - List[Point]: Points representing the sine wave.
    """
    # Calculate total number of steps
    totalSegments = periods * segmentsPerPeriod
    if extraHalfPeriod:
        totalSegments += int(segmentsPerPeriod / 2)

    # Generate sine wave points
    points = []
    for step in range(totalSegments + 1):  # +1 to include the last point
        # Compute axis distance and sine amplitude
        axis_distance = step * periodLength / segmentsPerPeriod
        sine_amplitude = amplitude * sin((step / segmentsPerPeriod) * tau + phaseShift)

        # Use polar coordinates to compute the point
        polar_point = PolarPoint(radious=axis_distance, angle=direction_polar)
        cartesian_point = polarToPoint(startPoint, polar_point.radious, polar_point.angle)

        # Adjust the y-coordinate for the sine wave amplitude
        cartesian_point.y += sine_amplitude

        # Append the point
        points.append(cartesian_point)

    return points

@geometryDecorator
def squareWave(
        startPoint: Point,
        direction_polar: float,
        amplitude: float,
        periodLength: float,
        periods: int,
        segmentsPerPeriod: int = 16,
        extraHalfPeriod: bool = False,
) -> List[Point]:
    """
    Generate a true square wave in Cartesian coordinates using polar coordinates for rotation.

    Parameters:
    - startPoint (Point): The starting point of the square wave.
    - direction_polar (float): The polar angle in radians that determines the direction of the wave.
    - amplitude (float): The amplitude of the wave.
    - periodLength (float): The length of each period of the wave.
    - periods (int): The number of periods in the wave.
    - segmentsPerPeriod (int): The number of line segments per period. Defaults to 16.
    - extraHalfPeriod (bool): Whether to add an extra half period. Defaults to False.

    Returns:
    - List[Point]: Points representing the square wave.
    """
    # Generate square wave points
    points = []
    points.append(Point(x=startPoint.x, y=startPoint.y, z=startPoint.z))
    halfAmplitude = amplitude / 2
    for period in range(periods):
        # Generate square wave points for each period
        points.append(Point(x=startPoint.x + period * periodLength, y=startPoint.y +  amplitude , z=startPoint.z))

        points.append(Point(x=startPoint.x + (period + 0.5) * periodLength, y=startPoint.y +  amplitude , z=startPoint.z)) 

        points.append(Point(x=startPoint.x + (period + 0.5) * periodLength, y=startPoint.y, z=startPoint.z))

        points.append(Point(x=startPoint.x + (period + 1) * periodLength, y=startPoint.y, z=startPoint.z))

    print(points)
    
    rotatedPoints = []
    centerPoint = startPoint
    for point in points:
        polarPoint = pointToPolar(centerPoint, point)
        rotatedPolarPoint = rotatePolarPoint(polarPoint, direction_polar)
        rotatedPoints.append(polarToPoint(centerPoint, rotatedPolarPoint.radious, rotatedPolarPoint.angle))

    return rotatedPoints

@geometryDecorator
def tringleWave(
        startPoint: Point,
        direction_polar: float,
        amplitude: float,
        periodLength: float,
        periods: int,
        segmentsPerPeriod: int = 16,
        extraHalfPeriod: bool = False,
) -> List[Point]:
    """
    Generate a true tringle wave in Cartesian coordinates using polar coordinates for rotation.

    Parameters:
    - startPoint (Point): The starting point of the tringle wave.
    - direction_polar (float): The polar angle in radians that determines the direction of the wave.
    - amplitude (float): The amplitude of the wave.
    - periodLength (float): The length of each period of the wave.
    - periods (int): The number of periods in the wave.
    - segmentsPerPeriod (int): The number of line segments per period. Defaults to 16.
    - extraHalfPeriod (bool): Whether to add an extra half period. Defaults to False.

    Returns:
    - List[Point]: Points representing the tringle wave.
    """
    # Generate tringle wave points
    points = []
    points.append(Point(x=startPoint.x, y=startPoint.y, z=startPoint.z))

    for period in range(periods):
        # Generate tringle wave points for each period

        points.append(Point(x=startPoint.x + (period + 0.5) * periodLength, y=startPoint.y +  amplitude , z=startPoint.z))

        points.append(Point(x=startPoint.x + (period + 1) * periodLength, y=startPoint.y, z=startPoint.z))

    print(points)

    rotatedPoints = []
    centerPoint = startPoint
    for point in points:
        polarPoint = pointToPolar(centerPoint, point)
        rotatedPolarPoint = rotatePolarPoint(polarPoint, direction_polar)
        rotatedPoints.append(polarToPoint(centerPoint, rotatedPolarPoint.radious, rotatedPolarPoint.angle))

    return rotatedPoints


def add_points(P1: Point, P2: Point) -> Point:
    return Point(
        x=(P1.x or 0) + (P2.x or 0),
        y=(P1.y or 0) + (P2.y or 0),
        z=(P1.z or 0) + (P2.z or 0),
        e=(P1.e or 0) + (P2.e or 0)
    )

def multiply_point_scalar(P: Point, scalar: float) -> Point:
    return Point(
        x=(P.x or 0) * scalar,
        y=(P.y or 0) * scalar,
        z=(P.z or 0) * scalar,
        e=(P.e or 0) * scalar
    )

def cubic_bezier_point(P0: Point, P1: Point, P2: Point, P3: Point, t: float) -> Point:
    """
    Compute a point on a cubic Bézier curve for a given parameter t.
    """
    # Compute the Bernstein polynomials
    b0 = (1 - t) ** 3
    b1 = 3 * (1 - t) ** 2 * t
    b2 = 3 * (1 - t) * t ** 2
    b3 = t ** 3

    # Compute the point
    point = add_points(
        add_points(
            multiply_point_scalar(P0, b0),
            multiply_point_scalar(P1, b1)
        ),
        add_points(
            multiply_point_scalar(P2, b2),
            multiply_point_scalar(P3, b3)
        )
    )
    return point

@geometryDecorator
def cubic_bezier_curve(
    P0: Point, P1: Point, P2: Point, P3: Point, num_points: int = 100
) -> List[Point]:
    """
    Generate a list of points approximating a cubic Bézier curve.

    Args:
        P0, P1, P2, P3 (Point): Control points of the cubic Bézier curve.
        num_points (int): Number of points to generate along the curve.

    Returns:
        List[Point]: List of points approximating the Bézier curve.
    """
    t_values = linespace(0.0, 1.0, num_points)
    curve_points = [cubic_bezier_point(P0, P1, P2, P3, t) for t in t_values]
    return curve_points


def de_casteljau(control_points: List[Point], t: float) -> Point:
    """
    Compute a point on a Bézier curve using De Casteljau's algorithm.

    Args:
        control_points (List[Point]): List of control points.
        t (float): Parameter between 0 and 1.

    Returns:
        Point: Point on the Bézier curve at parameter t.
    """
    points = control_points.copy()
    n = len(points)
    for r in range(1, n):
        for i in range(n - r):
            points[i] = add_points(
                multiply_point_scalar(points[i], 1 - t),
                multiply_point_scalar(points[i + 1], t)
            )
    return points[0]

@geometryDecorator
def bezier_curve_de_casteljau(control_points: List[Point], num_points: int = 1000) -> List[Point]:
    t_values = linespace(0.0, 1.0, num_points)
    curve_points = [de_casteljau(control_points, t) for t in t_values]
    return curve_points

