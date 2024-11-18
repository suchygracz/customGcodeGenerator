from typing import List, Union

from .vector import Vector
from ..point import Point
from design.geometricTools.polar import PolarPoint, pointToPolar, polarToPoint, rotatePolarPoint

def linespace(start: float, end: float, numberOfPoints: int) -> list:
    """
    Generate a list of evenly spaced points between start and end
    Args:
        start (float): starting value
        end (float): ending value
        numberOfPoints (int): number of points to be generated

    Returns: list of evenly spaced points between start and end

    """

    return [start + float(p) * (end - start) / (numberOfPoints - 1) for p in range(numberOfPoints)]

def flatten(listOfPoints: list) -> list:
    return [item for sublist in listOfPoints for item in sublist]

def flattenPoints(nested_points: List[Union[Point, List]]) -> List[Point]:
    """
    Recursively flattens a list of Point objects or nested lists of Point objects into a single list of Point objects.

    Args:
        nested_points (List[Union[Point, List]]): A list containing Point objects or nested lists of Point objects.

    Returns:
        List[Point]: A flattened list containing only Point objects.

    Raises:
        TypeError: If an item in the input list is neither a Point nor a list of Points.
    """
    flattened = []
    for item in nested_points:
        if isinstance(item, list):
            # If the item is a list, call the function recursively
            flattened.extend(flattenPoints(item))
        elif isinstance(item, Point):
            # If the item is a Point, append it to the flattened list
            flattened.append(item)
        else:
            raise TypeError(f"Unexpected item type: {type(item)}. Expected Point or list of Points.")
    return flattened

def move(points: Union[Point, List[Point], dict], vector: Vector, copy: bool = True) -> Union[Point, dict]:
    """
    Moves a point or list of points by a specified vector.

    Args:
        points (Union[Point, List[Point], dict]): The point(s) to move. Can be a single Point, a list of Points, or a dictionary with key 'shape'.
        vector (Vector): The vector by which to move the point(s).
        copy (bool, optional): Whether to create and return a copy of the points, or modify the original. Default is True.

    Returns:
        Union[Point, dict]: A Point or dictionary with key 'shape' containing a list of moved points.
                            If `copy=False`, modifies and returns the original points.

    Raises:
        TypeError: If the type of `points` is not supported.

    Example:
        ```python
        from design.point import Point
        from design.vector import Vector

        point = Point(1, 2, 3)
        vector = Vector(1, 0, -1)

        # Move a point
        moved_point = move(point, vector, copy=True)
        print(moved_point)  # Point(x=2, y=2, z=2)

        # Move a list of points
        points = [Point(1, 2, 3), Point(4, 5, 6)]
        moved_points = move(points, vector, copy=True)
        print(moved_points)  # {'shape': [Point(x=2, y=2, z=2), Point(x=5, y=5, z=5)]}
        ```
    """

    if isinstance(points, dict):
        points = points['shape']

    if isinstance(points, Point):
        if copy:
            return Point(
                x=points.x + vector.x,
                y=points.y + vector.y,
                z=points.z + vector.z
            )
        else:
            # Modify original point in place
            points.x += vector.x
            points.y += vector.y
            points.z += vector.z
            return points

    elif isinstance(points, list):
        if copy:
            # Create and return a copy with the points moved by the vector
            return {'shape': [
                Point(x=p.x + vector.x, y=p.y + vector.y, z=p.z + vector.z) for p in points
            ]}
        else:
            # Modify the original points in place
            for p in points:
                p.x += vector.x
                p.y += vector.y
                p.z += vector.z
            return {'shape': points}

    else:
        raise TypeError(f"Unexpected item type: {type(points)}. Expected Point, list of Points, or dict.")

def scale(points: Union[Point, List[Point], dict], scalar: float, axis: str = 'xyz', copy: bool = True) -> Union[Point, dict]:
    """
    Scales a point or list of points around the center of the shape by a given scalar.

    Args:
        points (Union[Point, List[Point], dict]): The point(s) to scale. Can be a single Point, a list of Points, or a dictionary with key 'shape'.
        scalar (float): The scale factor to apply.
        axis (str, optional): The axis or axes to apply scaling to. Default is 'xyz' (applies scaling in all axes).
        copy (bool, optional): Whether to create and return a copy of the points, or modify the original. Default is True.

    Returns:
        Union[Point, dict]: A Point or dictionary with key 'shape' containing a list of scaled points.
                            If `copy=False`, modifies and returns the original points.

    Raises:
        TypeError: If the type of `points` is not supported.
    """

    if isinstance(points, dict):
        points = points['shape']

    if isinstance(points, Point):
        # For a single point, scale and return the point itself
        if copy:
            return Point(
                x=points.x * scalar if 'x' in axis else points.x,
                y=points.y * scalar if 'y' in axis else points.y,
                z=points.z * scalar if 'z' in axis else points.z
            )
        else:
            points.x = points.x * scalar if 'x' in axis else points.x
            points.y = points.y * scalar if 'y' in axis else points.y
            points.z = points.z * scalar if 'z' in axis else points.z
            return points

    elif isinstance(points, list):
        # Determine if the shape is enclosed by checking if the first point equals the last point
        is_enclosed = points and points[0] == points[-1]

        # Make a copy of points if required
        if copy:
            points = points[:]

        # Exclude the last point if the shape is enclosed
        if is_enclosed:
            points = points[:-1]

        # Calculate the center point
        center_x = sum(p.x for p in points) / len(points)
        center_y = sum(p.y for p in points) / len(points)
        center_z = sum(p.z for p in points) / len(points)
        center = Point(x=center_x, y=center_y, z=center_z)

        # Scale points around the center
        if copy:
            scaled_points = [Point(
                x=center.x + (p.x - center.x) * scalar if 'x' in axis else p.x,
                y=center.y + (p.y - center.y) * scalar if 'y' in axis else p.y,
                z=center.z + (p.z - center.z) * scalar if 'z' in axis else p.z
            ) for p in points]
        else:
            # Modify points in place
            for p in points:
                if 'x' in axis:
                    p.x = center.x + (p.x - center.x) * scalar
                if 'y' in axis:
                    p.y = center.y + (p.y - center.y) * scalar
                if 'z' in axis:
                    p.z = center.z + (p.z - center.z) * scalar
            scaled_points = points

        # Add the closing point back if the shape was originally enclosed
        if is_enclosed:
            if copy:
                scaled_points.append(scaled_points[0].copy())
            else:
                points.append(points[0])

        return {'shape': scaled_points}

    else:
        raise TypeError(f"Unexpected item type: {type(points)}. Expected Point, list of Points, or dict.")


def rotate(points: Union[Point, List[Point], dict], angle: float, axis: str = 'z', copy: bool = True) -> Union[
    Point, dict]:
    """
    Rotates a point or list of points around the center of the shape.

    Args:
        points (Union[Point, List[Point], dict]): The point(s) to rotate. Can be a single Point, a list of Points, or a dictionary with key 'shape'.
        angle (float): The angle in radians to rotate the points.
        axis (str, optional): The axis around which to perform the rotation. Default is 'z'.
        copy (bool, optional): Whether to create and return a copy of the points, or modify the original. Default is True.

    Returns:
        Union[Point, dict]: A Point or dictionary with key 'shape' containing a list of rotated points.
                            If `copy=False`, modifies and returns the original points.

    Raises:
        TypeError: If the type of `points` is not supported.
    """

    if isinstance(points, dict):
        points = points['shape']

    if isinstance(points, Point):
        # For a single point, we just return it without rotating since there's no center defined for a single point
        return points

    elif isinstance(points, list):

        # Determine if the shape is enclosed by checking if the first point equals the last point
        is_enclosed = points and points[0] == points[-1]

        # Make a copy of the points if required
        if copy:
            points = points[:]

        # Exclude the last point if it is a copy of the first
        if is_enclosed:
            points = points[:-1]

        # Calculate the center point
        center_x = sum(p.x for p in points) / len(points)
        center_y = sum(p.y for p in points) / len(points)
        center_z = sum(p.z for p in points) / len(points)
        center = Point(x=center_x, y=center_y, z=center_z)

        # Rotate points around the center using polar coordinates
        rotated_points = []
        for p in points:
            polar_point = pointToPolar(center, p)
            rotated_polar_point = rotatePolarPoint(polar_point, angle)
            rotated_point = polarToPoint(center, rotated_polar_point.radious, rotated_polar_point.angle)

            if copy:
                rotated_points.append(rotated_point)
            else:
                # Modify the original point in place
                p.x = rotated_point.x
                p.y = rotated_point.y
                p.z = rotated_point.z

        if is_enclosed:
            if copy:
                rotated_points.append(rotated_points[0].copy())
            else:
                # If modifying in place, add the closing point again by modifying the reference to match the first point
                points.append(points[0])

        return {'shape': rotated_points} if copy else {'shape': points}

    else:
        raise TypeError(f"Unexpected item type: {type(points)}. Expected Point, list of Points, or dict.")

"""
def rotate(points: Union[Point, List[Point], dict], angle: float, axis: str = 'z') -> Union[Point, dict]:

    if isinstance(points, dict):
        points = points['shape']

    if isinstance(points, Point):
        return points

    elif isinstance(points, list):

        # Determine if the shape is enclosed by checking if the first point equals the last point
        is_enclosed = points and points[0] == points[-1]

        # Exclude the last point if it is a copy of the first
        if is_enclosed:
            points = points[:-1]

        # Calculate the center point
        center_x = sum(p.x for p in points) / len(points)
        center_y = sum(p.y for p in points) / len(points)
        center_z = sum(p.z for p in points) / len(points)
        center = Point(x=center_x, y=center_y, z=center_z)

        # Rotate points around the center using polar coordinates
        rotated_points = []
        for p in points:
            polar_point = pointToPolar(center, p)
            rotated_polar_point = rotatePolarPoint(polar_point, angle)
            rotated_points.append(polarToPoint(center, rotated_polar_point.radious, rotated_polar_point.angle))

        if is_enclosed:
            rotated_points.append(rotated_points[0].copy())

        return {'shape': rotated_points}
"""

def copy(points: Union[Point, List[Point], dict]) -> Union[Point, dict]:
    """
    Creates a copy of a point or list of points.

    Args:
        points (Union[Point, List[Point], dict]): The point(s) to copy. Can be a single Point, a list of Points, or a dictionary with key 'shape'.

    Returns:
        Union[Point, dict]: A Point or dictionary with key 'shape' containing a list of copied points.

    Raises:
        TypeError: If the type of `points` is not supported.
    """

    if isinstance(points, dict):
        points = points['shape']

    if isinstance(points, Point):
        return points.copy()

    elif isinstance(points, list):
        return [p.copy() for p in points]

    else:
        raise TypeError(f"Unexpected item type: {type(points)}. Expected Point, list of Points, or dict.")