from typing import List, Union
from ..point import Point

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


