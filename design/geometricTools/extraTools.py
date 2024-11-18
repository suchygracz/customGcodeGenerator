from math import sqrt

from design.geometricTools.baseTools import linespace, copy
from design.point import Point
from typing import List, Union
from design.directCommands.commands import moveWithNoExtrusion

def euclideanDistance(p1: Point, p2: Point) -> float:
    """
    Calculate the Euclidean distance between two points in 3D space.

    Args:
        p1 (Point): The first point.
        p2 (Point): The second point.

    Returns:
        float: The Euclidean distance between the two points.
    """
    return sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)

def nonPlanarVase(baseShape: dict[str, Union[Point, List[Point]]],variation: float, height: int, extrusionW: float, extrusionH: float ) -> dict[str, List[Point]]:
    """
        Generates a non-planar vase-like 3D shape by extruding a given base shape with variation over a specified height.

        Args:
            baseShape (dict[str, Union[Point, List[Point]]]): A dictionary containing the base shape, represented as a list of Points.
            variation (float): A factor that adds variation to the extrusion height, resulting in a non-planar effect.
            height (int): The number of layers to extrude the base shape vertically.
            extrusionW (float): The width factor for extrusion calculations.
            extrusionH (float): The height factor for extrusion calculations.

        Returns:
            dict[str, List[Point]]: A dictionary containing the extruded non-planar shape as a list of Points.
    `"""
    shapePoints = baseShape['shape']
    print(shapePoints)
    pointsLength = len(shapePoints)
    change1  = linespace(0, 1, pointsLength//2)
    change2 = linespace(1, 0, pointsLength//2)
    change = change1 + change2

    previousPoint = shapePoints[0]

    vasePoints = [previousPoint]
    for point in range(1, pointsLength):
        if point < pointsLength / 2:
            distance = euclideanDistance(previousPoint, shapePoints[point])
            extrusion = (distance * extrusionW * extrusionH) * (1 + variation * change[point])
            shapePoints[point].z = (shapePoints[point].z + extrusionH) * (1 + variation * change[point])
            shapePoints[point].e = extrusion
        else:
            distance = euclideanDistance(previousPoint, shapePoints[point])
            extrusion = (distance * extrusionW * extrusionH) * (1 + variation * change[point])
            shapePoints[point].z = (shapePoints[point].z + extrusionH) * (1 + variation * change[point])
            shapePoints[point].e = extrusion
        previousPoint = shapePoints[point]
        vasePoints.append(shapePoints[point])


    for layer in range(1, height):
        currentLayer = copy(shapePoints)
        print(currentLayer)
        for point in range(0, pointsLength):
            currentLayer[point].z = shapePoints[point].z * layer
            vasePoints.append(currentLayer[point])

    return {'shape': vasePoints}

def vaseMode(baseShape: dict[str, Union[Point, List[Point]]],height: int, extrusionW: float, extrusionH: float ) -> dict[str, List[Point]]:
    """
        Generates a vase-like 3D shape by extruding a given base shape over a specified height.

        Args:
            baseShape (dict[str, Union[Point, List[Point]]]): A dictionary containing the base shape, represented as a list of Points.
            height (int): The number of layers to extrude the base shape vertically.
            extrusionW (float): The width factor for extrusion calculations.
            extrusionH (float): The height factor for extrusion calculations.

        Returns:
            dict[str, List[Point]]: A dictionary containing the extruded shape as a list of Points.
    """

    shapePoints = baseShape['shape']

    pointsLength = len(shapePoints)

    change = linespace(0, 1, pointsLength)

    previousPoint = shapePoints[0]

    vasePoints = [previousPoint]

    for point in range(1, pointsLength):
        distance = euclideanDistance(previousPoint, shapePoints[point])
        extrusion = (distance * extrusionW * extrusionH) * change[point]
        shapePoints[point].z = (shapePoints[point].z + extrusionH) * change[point]
        shapePoints[point].e = extrusion
        previousPoint = shapePoints[point]
        vasePoints.append(shapePoints[point])


    for layer in range(1, height - 1):
        currentLayer = copy(shapePoints)
        print(currentLayer)
        for point in range(0, pointsLength):
            extrusion = (distance * extrusionW * extrusionH)
            currentLayer[point].z = shapePoints[point].z + extrusionH * layer
            currentLayer[point].e = shapePoints[point].e * layer
            vasePoints.append(currentLayer[point])

    for point in range(1, pointsLength):
        currentLayer = copy(shapePoints)
        distance = euclideanDistance(previousPoint, shapePoints[point])
        extrusion = (distance * extrusionW * extrusionH) * change[-point]
        shapePoints[point].z = shapePoints[point].z * height
        shapePoints[point].e = extrusion
        previousPoint = shapePoints[point]
        vasePoints.append(shapePoints[point])

    return {'shape': vasePoints}

'''
def solid_layer_infill(baseShape: dict[str, List[Point]], extrusion_width: float) -> dict[str, List[Point]]:
    """
    Generate a solid layer inside the enclosed base shape using a linear infill pattern that fits inside a complex shape.

    Args:
        baseShape (dict[str, List[Point]]): The closed base shape represented as a dictionary with the key 'shape' and a list of Point objects.
        extrusion_width (float): The width of the extrusion in millimeters, used as the spacing between infill lines.

    Returns:
        dict[str, List[Point]]: A dictionary with a 'shape' key containing a list of Point objects representing the infill pattern.
    """
    # Extract points from baseShape
    shape_points = baseShape['shape']

    # Calculate the bounding box of the shape, expanding by half the extrusion width to ensure complete fill
    min_x = min(point.x for point in shape_points) - (extrusion_width / 2)
    max_x = max(point.x for point in shape_points) + (extrusion_width / 2)
    min_y = min(point.y for point in shape_points) - (extrusion_width / 2)
    max_y = max(point.y for point in shape_points) + (extrusion_width / 2)

    # Generate y values for the infill lines using linespace
    num_lines = int((max_y - min_y) / extrusion_width)
    y_values = linespace(min_y, max_y, num_lines)

    # Initialize list to hold the infill points
    infill_points = []

    # Create parallel lines within the bounding box, spaced according to 'extrusion_width'
    for current_y in y_values:
        # Create line endpoints from min_x to max_x at the current y level
        start_point = Point(x=min_x, y=current_y, z=0)
        end_point = Point(x=max_x, y=current_y, z=0)

        # Find intersections between the line and the boundary of the shape
        intersections = find_intersections_with_shape(shape_points, start_point, end_point)

        # Sort intersections by x to determine segments within the shape
        intersections.sort(key=lambda p: p.x)

        # Use the even-odd rule to add segments inside the shape
        for i in range(0, len(intersections) - 1, 2):
            p1 = intersections[i]
            p2 = intersections[i + 1]
            infill_points.extend([p1, p2])

    return {'shape': infill_points}

def find_intersections_with_shape(shape_points: List[Point], start: Point, end: Point) -> List[Point]:
    """
    Finds the intersections of a line segment with the boundary of a complex shape.

    Args:
        shape_points (List[Point]): List of points representing the boundary of the shape.
        start (Point): Start point of the line segment.
        end (Point): End point of the line segment.

    Returns:
        List[Point]: A list of intersection points between the line segment and the shape boundary.
    """
    intersections = []

    # Iterate through each edge of the shape
    for i in range(len(shape_points) - 1):
        shape_start = shape_points[i]
        shape_end = shape_points[i + 1]

        intersection = find_line_intersection(start, end, shape_start, shape_end)
        if intersection:
            intersections.append(intersection)

    return intersections
'''
'''
def solid_layer_infill(baseShape: dict[str, List[Point]], extrusion_width: float) -> List[dict[str, Union[List[Point], Point]]]:
    """
    Generate a solid layer inside the enclosed base shape using a linear infill pattern that fits inside a complex shape.

    Args:
        baseShape (dict[str, List[Point]]): The closed base shape represented as a dictionary with the key 'shape' and a list of Point objects.
        extrusion_width (float): The width of the extrusion in millimeters, used as the spacing between infill lines.

    Returns:
        List[Dict[str, Union[List[Point], Point]]]: A list containing dictionaries with either a 'shape' key or 'moveWithNoExtrusion' key. Each 'shape' key contains a list of Point objects representing the infill pattern. Each 'moveWithNoExtrusion' key contains a Point object for a non-extruding move.
    """
    # Extract points from baseShape
    shape_points = baseShape['shape']

    # Calculate the bounding box of the shape, expanding by half the extrusion width to ensure complete fill
    min_x = min(point.x for point in shape_points) - (extrusion_width / 2)
    max_x = max(point.x for point in shape_points) + (extrusion_width / 2)
    min_y = min(point.y for point in shape_points) - (extrusion_width / 2)
    max_y = max(point.y for point in shape_points) + (extrusion_width / 2)

    # Generate y values for the infill lines using linespace
    num_lines = int((max_y - min_y) / extrusion_width)
    y_values = linespace(min_y, max_y, num_lines)

    # Initialize list to hold the infill points and the move commands
    infill_commands = []

    # Create parallel lines within the bounding box, spaced according to 'extrusion_width'
    for i, current_y in enumerate(y_values):
        # Create line endpoints from min_x to max_x at the current y level
        start_point = Point(x=min_x, y=current_y, z=0)
        end_point = Point(x=max_x, y=current_y, z=0)

        # Find intersections between the line and the boundary of the shape
        intersections = find_intersections_with_shape(shape_points, start_point, end_point)

        # Sort intersections by x to determine segments within the shape
        intersections.sort(key=lambda p: p.x)

        # Use the even-odd rule to add segments inside the shape
        line_points = []
        for j in range(0, len(intersections) - 1, 2):
            p1 = intersections[j]
            p2 = intersections[j + 1]
            line_points.extend([p1, p2])

        # If line_points are found (indicating a valid infill segment), add it to infill_commands
        if line_points:
            infill_commands.append({'shape': line_points})

            # If not the last line, add a moveWithNoExtrusion to the start of the next line
            if i < len(y_values) - 1:
                move_to_next_start = moveWithNoExtrusion(Point(x=min_x, y=y_values[i + 1], z=0))
                infill_commands.append(move_to_next_start)

    return infill_commands

# Required supporting function for intersection calculations
def find_intersections_with_shape(shape_points: List[Point], start: Point, end: Point) -> List[Point]:
    """
    Finds the intersections of a line segment with the boundary of a complex shape.

    Args:
        shape_points (List[Point]): List of points representing the boundary of the shape.
        start (Point): Start point of the line segment.
        end (Point): End point of the line segment.

    Returns:
        List[Point]: A list of intersection points between the line segment and the shape boundary.
    """
    intersections = []

    # Iterate through each edge of the shape
    for i in range(len(shape_points) - 1):
        shape_start = shape_points[i]
        shape_end = shape_points[i + 1]

        intersection = find_line_intersection(start, end, shape_start, shape_end)
        if intersection:
            intersections.append(intersection)

    return intersections


def find_line_intersection(start1: Point, end1: Point, start2: Point, end2: Point) -> Union[None, Point]:
    """
    Finds the intersection point between two line segments, if it exists.

    Args:
        start1 (Point): Start point of the first line segment.
        end1 (Point): End point of the first line segment.
        start2 (Point): Start point of the second line segment.
        end2 (Point): End point of the second line segment.

    Returns:
        Union[None, Point]: The intersection point if one exists, otherwise None.
    """
    # Calculate the direction of the lines
    dx1, dy1 = end1.x - start1.x, end1.y - start1.y
    dx2, dy2 = end2.x - start2.x, end2.y - start2.y

    # Calculate determinants
    determinant = (-dx2 * dy1 + dx1 * dy2)
    if determinant == 0:
        # Lines are parallel, no intersection
        return None

    s = (-dy1 * (start1.x - start2.x) + dx1 * (start1.y - start2.y)) / determinant
    t = (dx2 * (start1.y - start2.y) - dy2 * (start1.x - start2.x)) / determinant

    # Check if the intersection point lies on both line segments
    if 0 <= s <= 1 and 0 <= t <= 1:
        intersection_x = start1.x + (t * dx1)
        intersection_y = start1.y + (t * dy1)
        intersection_z = start1.z + (t * (end1.z - start1.z))  # Assume linear interpolation for z-axis
        return Point(x=intersection_x, y=intersection_y, z=intersection_z)

    # No intersection found
    return None
'''

def solid_layer_infill(baseShape: dict[str, List[Point]], extrusion_width: float) -> List[dict[str, Union[List[Point], Point]]]:
    """
    Generate a solid layer inside the enclosed base shape using a linear infill pattern that fits inside a complex shape.

    Args:
        baseShape (dict[str, List[Point]]): The closed base shape represented as a dictionary with the key 'shape' and a list of Point objects.
        extrusion_width (float): The width of the extrusion in millimeters, used as the spacing between infill lines.

    Returns:
        List[Dict[str, Union[List[Point], Point]]]: A list containing dictionaries with either a 'shape' key or 'moveWithNoExtrusion' key.
                                                     Each 'shape' key contains a list of Point objects representing the infill pattern.
                                                     Each 'moveWithNoExtrusion' key contains a Point object for a non-extruding move.
    """
    # Extract points from baseShape
    shape_points = baseShape['shape']

    # Calculate the bounding box of the shape, expanding by half the extrusion width to ensure complete fill
    min_x = min(point.x for point in shape_points) - (extrusion_width / 2)
    max_x = max(point.x for point in shape_points) + (extrusion_width / 2)
    min_y = min(point.y for point in shape_points) - (extrusion_width / 2)
    max_y = max(point.y for point in shape_points) + (extrusion_width / 2)

    # Generate y values for the infill lines using a for loop with an extrusion width step
    y_values = [min_y + i * extrusion_width for i in range(int((max_y - min_y) / extrusion_width) + 1)]

    # Initialize list to hold the infill points and the move commands
    infill_commands = []

    # Create parallel lines within the bounding box, spaced according to 'extrusion_width'
    for i, current_y in enumerate(y_values):
        # Create line endpoints from min_x to max_x at the current y level
        start_point = Point(x=min_x, y=current_y, z=0)
        end_point = Point(x=max_x, y=current_y, z=0)

        # Find intersections between the line and the boundary of the shape
        intersections = find_intersections_with_shape(shape_points, start_point, end_point)

        # Sort intersections by x to determine segments within the shape
        intersections.sort(key=lambda p: p.x)

        # Use the even-odd rule to add segments inside the shape
        for j in range(0, len(intersections) - 1, 2):
            p1 = intersections[j]
            p2 = intersections[j + 1]

            # Create a segment between each pair of intersections
            infill_commands.append({'shape': [p1, p2]})

            # Add a moveWithNoExtrusion command to move to the start of the next segment without extruding
            if j + 2 < len(intersections):
                move_to_next_start = moveWithNoExtrusion(intersections[j + 2])
                infill_commands.append(move_to_next_start)

        # If not the last line, add a moveWithNoExtrusion to the start of the next line
        if i < len(y_values) - 1:
            move_to_next_start = moveWithNoExtrusion(Point(x=min_x, y=y_values[i + 1], z=0))
            infill_commands.append(move_to_next_start)

    return infill_commands

# Required supporting function for intersection calculations
def find_intersections_with_shape(shape_points: List[Point], start: Point, end: Point) -> List[Point]:
    """
    Finds the intersections of a line segment with the boundary of a complex shape.

    Args:
        shape_points (List[Point]): List of points representing the boundary of the shape.
        start (Point): Start point of the line segment.
        end (Point): End point of the line segment.

    Returns:
        List[Point]: A list of intersection points between the line segment and the shape boundary.
    """
    intersections = []

    # Iterate through each edge of the shape
    for i in range(len(shape_points) - 1):
        shape_start = shape_points[i]
        shape_end = shape_points[i + 1]

        intersection = find_line_intersection(start, end, shape_start, shape_end)
        if intersection:
            intersections.append(intersection)

    return intersections


def find_line_intersection(start1: Point, end1: Point, start2: Point, end2: Point) -> Union[None, Point]:
    """
    Finds the intersection point between two line segments, if it exists.

    Args:
        start1 (Point): Start point of the first line segment.
        end1 (Point): End point of the first line segment.
        start2 (Point): Start point of the second line segment.
        end2 (Point): End point of the second line segment.

    Returns:
        Union[None, Point]: The intersection point if one exists, otherwise None.
    """
    # Calculate the direction of the lines
    dx1, dy1 = end1.x - start1.x, end1.y - start1.y
    dx2, dy2 = end2.x - start2.x, end2.y - start2.y

    # Calculate determinants
    determinant = (-dx2 * dy1 + dx1 * dy2)
    if determinant == 0:
        # Lines are parallel, no intersection
        return None

    s = (-dy1 * (start1.x - start2.x) + dx1 * (start1.y - start2.y)) / determinant
    t = (dx2 * (start1.y - start2.y) - dy2 * (start1.x - start2.x)) / determinant

    # Check if the intersection point lies on both line segments
    if 0 <= s <= 1 and 0 <= t <= 1:
        intersection_x = start1.x + (t * dx1)
        intersection_y = start1.y + (t * dy1)
        intersection_z = start1.z + (t * (end1.z - start1.z))  # Assume linear interpolation for z-axis
        return Point(x=intersection_x, y=intersection_y, z=intersection_z)

    # No intersection found
    return None


