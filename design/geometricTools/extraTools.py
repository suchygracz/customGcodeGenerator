from math import sqrt

from design.geometricTools.baseTools import linespace, copy
from design.point import Point
from typing import List, Union

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


