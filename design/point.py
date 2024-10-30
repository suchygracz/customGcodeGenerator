from pydantic import BaseModel
from typing import Optional

class Point(BaseModel):
    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None
    e: Optional[float] = None