import design
from typing import List, Dict, Union
from math import sqrt, pi
from design.geometricTools.baseTools import flatten, flattenPoints
from typing import List, Dict
from design.point import Point


def pointsIndiciesToStrRepresentation(points: List[Union[Point, List[Point], dict]]) -> list:
    """
    Converts a list of points to a list of string representations of the points.
    mostly for visualization purposes

    Args:
        points (List[Union[Point, List[Point], dict]]):
            A list of points to be converted. Each item in the list can be:
                - A single Point object,
                - A list of Point objects,
                - A dictionary containing the key 'shape', with a list of Point objects.

    Returns:
        list: A list of strings, where each string is the representation of a Point object.

    Example:
        ```python
        from design.point import Point

        point1 = Point(x=1.0, y=2.0, z=3.0)
        point2 = Point(x=4.0, y=5.0, z=6.0)
        points = [point1, point2]

        str_rep = pointsIndiciesToStrRepresentation(points)
        print(str_rep)
        # Output: ['[1.0, 2.0, 3.0]', '[4.0, 5.0, 6.0]']
        ```
    """
    if isinstance(points, dict):
        points = points['shape']

    if isinstance(points, Point):
        return [points.listRepresentation()]
    elif isinstance(points, list):
        flatList = flattenPoints(points)
        counter = 0
        listOfPoints = []
        for point in flatList:
            counter += 1
            if counter < len(flatList):
                listOfPoints.append(point.listRepresentation())
                #print(f"{point},")
            else:
                #print(point)
                listOfPoints.append(point.listRepresentation())
        return listOfPoints


def parseStepsToGcode(steps: List[Dict], filename: str, extrusion_params: List[float]):
    """
    Parses a list of steps representing G-code commands and writes them to a G-code file.
    Adds extrusion calculation for G-code moves if extrusion is not explicitly defined.

    Args:
        steps (List[Dict]): A list of steps, each represented as a dictionary containing a command type and associated data.
            The dictionary has the following structure:
                - 'moveWithNoExtrusion': A Point object representing a move without extrusion.
                - 'stationaryExtrusion': A dictionary containing 'amount' (float) and 'speed' (int) representing the extrusion amount and speed.
                - 'shape': A list of Point objects representing a shape defined by its points.
                - 'retraction': A float representing the amount of filament to retract.
        filename (str): The name of the output file to write the G-code commands to.
        extrusion_params (List[float]): A list containing two values:
            - extrusionWidth (float): The default width of the extrusion.
            - extrusionHeight (float): The default height of the extrusion.

    Example:
        ```
        from design.point import Point

        listOfSteps = [
            {'moveWithNoExtrusion': Point(x=0, y=0, z=0)},
            {'stationaryExtrusion': {'amount': 5, 'speed': 600}},
            {'shape': [
                Point(x=0, y=0, z=0, e=None),
                Point(x=10, y=0, z=0, e=None),
                Point(x=10, y=10, z=0, e=2),
                Point(x=0, y=10, z=0, e=4),
                Point(x=0, y=0, z=0, e=None)
            ]}
        ]

        parseSteps(listOfSteps, 'output.gcode', extrusion_params=[0.4, 0.2])
        ```

    Raises:
        ValueError: If an unsupported command type is encountered in the steps.

    """
    extrusionWidth, extrusionHeight = extrusion_params
    last_point = None
    retraction_amount = 2.0  # The amount to retract before non-extrusion moves (in mm)
    prime_amount = retraction_amount * 0.9  # Extrude back slightly less than retracted amount (e.g., 90%)

    with open(filename, 'w') as gcode_file:
        for step in steps:
            command_type, data = next(iter(step.items()))  # Extract the single key-value pair in each step

            match command_type:
                case 'moveWithNoExtrusion':
                    # Add retraction before the move with no extrusion
                    gcode_file.write(f"G1 E-{retraction_amount} F1800 ; Retraction before moving\n")

                    # Perform the move with no extrusion
                    point = data
                    gcode_file.write(f"G0 X{point.x} Y{point.y} Z{point.z}\n")
                    last_point = point  # Update the last point

                    # Prime extrusion after moving
                    gcode_file.write(f"G1 E{prime_amount} F1800 ; Priming after move\n")

                case 'stationaryExtrusion':
                    extrude_amount = data['amount']
                    speed = data['speed']
                    gcode_file.write(f"G1 E{extrude_amount} F{speed}\n")

                case 'shape':
                    gcode_file.write(f"; Generating shape\n")
                    for point in data:
                        if point.e is None and last_point:
                            # Calculate distance from last point
                            distance = sqrt(
                                (point.x - last_point.x) ** 2
                                + (point.y - last_point.y) ** 2
                                + (point.z - last_point.z) ** 2
                            )
                            # Calculate extrusion value based on distance, extrusionWidth, and extrusionHeight
                            e_value = (extrusionWidth * extrusionHeight * distance) / (pi * (1.75 / 2) ** 2)
                        else:
                            e_value = point.e

                        e_command = f"E{e_value}" if e_value is not None else ""
                        gcode_file.write(f"G1 X{point.x} Y{point.y} Z{point.z} {e_command}\n")

                        last_point = point  # Update the last point after each move

                case 'retraction':
                    retraction = data
                    gcode_file.write(f"G1 E{retraction} F{speed}\n")

                case _:
                    gcode_file.write(f"; Unknown command type: {command_type}\n")


