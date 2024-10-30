from pydantic import BaseModel
from typing import Optional

class Vector(BaseModel):
    """
    A 3D vector, that can be used for 3D transformations like moving, scaling, etc.

    Attributes:
        x: Optional[float] = None
        y: Optional[float] = None
        z: Optional[float] = None
    """

    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None
