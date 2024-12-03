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

# Define a function for the starting G-code
def generateStartingGcode(hotend_temp: float, bed_temp: float) -> List[str]:
    """
    Generates starting G-code commands to set up the 3D printer.

    Args:
        hotend_temp (float): Temperature to set for the hotend in degrees Celsius.
        bed_temp (float): Temperature to set for the print bed in degrees Celsius.

    Returns:
        List[str]: List of G-code commands to set up the 3D printer.
    """
    startingGcode = [
        "G21 ; Set units to millimeters",
        "G90 ; Use absolute positioning",
        "M82 ; Use absolute distances for extrusion",
        f"M104 S{hotend_temp} ; Set hotend temperature",
        f"M140 S{bed_temp} ; Set bed temperature",
        "G28 ; Home all axes",
        "M107 S255; set fan to 100%"
        f"M190 S{bed_temp} ; Wait for bed temperature to reach {bed_temp}°C",
        f"M109 S{hotend_temp} ; Wait for hotend temperature to reach {hotend_temp}°C",
        "G1 Z0.3 F5000 ; Move nozzle to start height",
        "G92 E0 ; Zero the extruder",
        "G1 X0 Y0 F3000 ; Move to start position",
    ]
    return startingGcode

# Define a function for the ending G-code
def generateEndingGcode() -> List[str]:
    """
    Generates ending G-code commands to shut down the 3D printer.

    Returns:
        List[str]: List of G-code commands to safely end the print.
    """
    endingGcode = [
        "G91 ; Relative positioning",
        "G1 E-3 F300 ; Retract filament a little to reduce ooze",
        "G1 Z10 F3000 ; Lift the nozzle",
        "G90 ; Absolute positioning",
        "G1 X0 Y200 F3000 ; Move the print head away from the print",
        "M104 S0 ; Turn off hotend",
        "M140 S0 ; Turn off bed",
        "M84 ; Disable motors",
        "M107 ; Turn off fan",
    ]
    return endingGcode



def parseStepsToGcode(steps: List[Dict], filename: str, extrusion_params: List[float], hotendTemp: float, bedTemp: float) -> None:
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
        startingGcode = generateStartingGcode(hotendTemp, bedTemp)
        for line in startingGcode:
            gcode_file.write(line + "\n")

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

        endingGcode = generateEndingGcode()
        for line in endingGcode:
            gcode_file.write(line + "\n")