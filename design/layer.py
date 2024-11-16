from pydantic import BaseModel, validator
from typing import List
from design.point import Point

class Layer(BaseModel):
    listOfPoints: List[Point]

    class Config:
        arbitrary_types_allowed = True

    @validator('listOfPoints')
    def validate_enclosed_shape(cls, v):
        """
        Validator to ensure that the first point is the same as the last point in the list.
        """
        if len(v) < 2:
            raise ValueError("The list must contain at least two points to form an enclosed shape.")

        # Check if the first and last points are the same
        if not (v[0].x == v[-1].x and v[0].y == v[-1].y and v[0].z == v[-1].z):
            raise ValueError("The first point must be the same as the last point to form an enclosed shape.")

        return v

    def getLastPoint(self):
        return self.listOfPoints[-1]

    def __str__(self):
        return f"{self.listOfPoints}"