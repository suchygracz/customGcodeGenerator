from pydantic import BaseModel
from typing import Optional

class Point(BaseModel):
    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None
    e: Optional[float] = None

    def __str__(self):
        return f"[{self.x}, {self.y}, {self.z}]"

    def listRepresentation(self):
        return [self.x, self.y, self.z]