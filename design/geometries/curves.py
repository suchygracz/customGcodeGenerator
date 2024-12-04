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
def cosineWave(
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
    Generate a cosine wave in Cartesian coordinates using polar coordinates for rotation.

    Parameters:
    - startPoint (Point): The starting point of the cosine wave.
    - direction_polar (float): The polar angle in radians that determines the direction of the wave.
    - amplitude (float): The amplitude of the wave.
    - periodLength (float): The length of each period of the wave.
    - periods (int): The number of periods in the wave.
    - segmentsPerPeriod (int): The number of line segments per period. Defaults to 50.
    - extraHalfPeriod (bool): Whether to add an extra half period. Defaults to False.
    - phaseShift (float): The phase shift of the wave. Defaults to 0.

    Returns:
    - List[Point]: Points representing the cosine wave.
    """
    # Calculate total number of steps
    totalSegments = periods * segmentsPerPeriod
    if extraHalfPeriod:
        totalSegments += int(segmentsPerPeriod / 2)

    # Generate cosine wave points
    points = []
    # Starting with a phase shift of tau / 4 (which equals pi/2) to start at the peak
    phaseShift += tau / 2

    for step in range(totalSegments + 1):  # +1 to include the last point
        # Compute axis distance and cosine amplitude
        axis_distance = step * periodLength / segmentsPerPeriod
        cosine_amplitude = (-1) * amplitude * cos((step / segmentsPerPeriod) * tau + phaseShift)

        # Use polar coordinates to compute the point
        polar_point = PolarPoint(radious=axis_distance, angle=direction_polar)
        cartesian_point = polarToPoint(startPoint, polar_point.radious, polar_point.angle)

        # Adjust the y-coordinate for the cosine wave amplitude
        cartesian_point.y += cosine_amplitude

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

@geometryDecorator
def cardinal_spline(points: List[Point], tension: float = 0.0, resolution: int = 10) -> List[Point]:
    """
    Generates a Cardinal Spline based on given control points.

    Args:
        points (List[Point]): List of control points through which the spline will pass.
        tension (float): The tension parameter. Range -1 to 1, where -1 is very tight, and 1 is very loose.
        resolution (int): The number of interpolated points between each pair of control points.

    Returns:
        List[Point]: The list of points representing the interpolated Cardinal Spline.
    """
    if len(points) < 2:
        raise ValueError("At least two points are required to generate a cardinal spline.")

    spline_points = []

    # Iterate through each pair of control points
    for i in range(len(points) - 1):
        p0 = points[i - 1] if i > 0 else points[i]
        p1 = points[i]
        p2 = points[i + 1]
        p3 = points[i + 2] if i + 2 < len(points) else points[i + 1]

        # Compute interpolated points between p1 and p2
        tValuese = linespace(0, 1, resolution)
        for t in tValuese:
            # Hermite basis functions (modified by tension)
            t2 = t * t
            t3 = t2 * t

            h1 = 2 * t3 - 3 * t2 + 1
            h2 = -2 * t3 + 3 * t2
            h3 = t3 - 2 * t2 + t
            h4 = t3 - t2

            # Tension adjustment
            m1_x = (1 - tension) * (p2.x - p0.x) / 2
            m1_y = (1 - tension) * (p2.y - p0.y) / 2
            m2_x = (1 - tension) * (p3.x - p1.x) / 2
            m2_y = (1 - tension) * (p3.y - p1.y) / 2

            # Interpolated point
            x = h1 * p1.x + h2 * p2.x + h3 * m1_x + h4 * m2_x
            y = h1 * p1.y + h2 * p2.y + h3 * m1_y + h4 * m2_y
            z = p1.z  # Retain the z-coordinate from the control point p1 for simplicity

            spline_points.append(Point(x=x, y=y, z=z))

    return spline_points

def catmull_rom_spline(points: List[Point], resolution: int = 10) -> List[Point]:
    """
    Generates a Catmull-Rom Spline based on given control points.

    Args:
        points (List[Point]): List of control points through which the spline will pass.
        resolution (int): The number of interpolated points between each pair of control points.

    Returns:
        List[Point]: The list of points representing the interpolated Catmull-Rom Spline.
    """
    return cardinal_spline(points, tension=0.0, resolution=resolution)


def basis_function(i: int, k: int, t: float, knot_vector: List[float]) -> float:
    """
    Calculate the basis function value for a given i, k, t, and knot vector.
    """
    if k == 1:
        if knot_vector[i] <= t < knot_vector[i + 1]:
            return 1.0
        return 0.0
    else:
        denom1 = knot_vector[i + k - 1] - knot_vector[i]
        denom2 = knot_vector[i + k] - knot_vector[i + 1]

        term1 = ((t - knot_vector[i]) / denom1) * basis_function(i, k - 1, t, knot_vector) if denom1 != 0 else 0
        term2 = ((knot_vector[i + k] - t) / denom2) * basis_function(i + 1, k - 1, t, knot_vector) if denom2 != 0 else 0

        return term1 + term2


def generate_open_uniform_knot_vector(num_control_points: int, degree: int) -> List[float]:
    """
    Generate an open uniform knot vector.

    Args:
        num_control_points (int): Number of control points.
        degree (int): Degree of the curve.

    Returns:
        List[float]: Generated knot vector.
    """
    num_knots = num_control_points + degree + 1
    knot_vector = [0] * (degree + 1)  # Start with repeated knots
    knot_vector += list(range(1, num_knots - 2 * (degree + 1) + 1))  # Uniform spacing
    knot_vector += [num_knots - 2 * (degree + 1)] * (degree + 1)  # End with repeated knots
    return knot_vector


@geometryDecorator
def nurbs_curve(control_points: List[Point], weights: List[float], degree: int, num_points: int = 100) -> List[Point]:
    """
    Generate a NURBS curve from control points, weights, and degree.

    Args:
        control_points (List[Point]): List of control points.
        weights (List[float]): Weights for each control point.
        degree (int): Degree of the NURBS curve.
        num_points (int): Number of points to generate for the curve.

    Returns:
        List[Point]: List of points representing the NURBS curve.
    """
    # Automatically generate the knot vector based on control points and degree
    num_control_points = len(control_points)
    knot_vector = generate_open_uniform_knot_vector(num_control_points, degree)

    # Number of knots should match `num_control_points + degree + 1`
    assert len(knot_vector) == num_control_points + degree + 1, "Incorrect knot vector length."

    # Generate NURBS points
    curve_points = []
    t_values = linespace(knot_vector[degree], knot_vector[-degree - 1], num_points)

    for t in t_values:
        numerator = Point(x=0, y=0, z=0, e=0)
        denominator = 0.0
        for i in range(num_control_points):
            basis = basis_function(i, degree + 1, t, knot_vector)
            weighted_basis = basis * weights[i]
            numerator = add_points(numerator, multiply_point_scalar(control_points[i], weighted_basis))
            denominator += weighted_basis

        if denominator != 0:
            curve_points.append(multiply_point_scalar(numerator, 1 / denominator))

    return curve_points