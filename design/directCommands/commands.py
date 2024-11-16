from typing import Dict
from design.point import Point

def moveWithNoExtrusion(point: Point) -> Dict[str, Point]:
    """
    Creates a dictionary representing a 'moveWithNoExtrusion' command.

    Args:
        point (Point): The target point to move to without extruding.

    Returns:
        Dict[str, Point]: A dictionary representing the command with type 'moveWithNoExtrusion' and the target point.
    """
    return {'moveWithNoExtrusion': point}

def stationaryExtrusion(amount: float, speed: int) -> Dict[str, Dict[str, float]]:
    """
    Creates a dictionary representing a 'stationaryExtrusion' command.

    Args:
        amount (float): The amount of material to extrude in millimeters.
        speed (int): The speed of extrusion in mm/min.

    Returns:
        Dict[str, Dict[str, float]]: A dictionary representing the command with type 'stationaryExtrusion'
                                     and the amount and speed of extrusion.
    """
    return {'stationaryExtrusion': {'amount': amount,'speed': speed}}

def retraction(amount: float) -> Dict[str, float]:
    """
    Creates a dictionary representing a 'retraction' command.

    Args:
        amount (float): The amount of material to retract in millimeters.

    Returns:
        Dict[str, float]: A dictionary representing the command with type 'retraction' and the amount to retract.
    """
    return {
        'retraction': amount
    }


