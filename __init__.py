# Import key classes and functions from submodules to the top level

from .design.directCommands.commands import *

from .design.geometricTools.baseTools import *

from .design.geometricTools.extraTools import *

from .design.geometricTools.polar import *

from .design.geometricTools.vector import Vector

from .design.geometries.curves import *

from .design.geometries.shapes import *

from .design.point import Point

from .transform.transformations import *

from .visualizator.main import SoftwareRender



# Defining what should be available at top level
# Create a list dynamically by filtering out built-in attributes and non-callables
#__all__ = [name for name in globals() if not name.startswith("_") and callable(globals()[name])]
# Defining what should be available at the top level

circle = circle(Point(x=0, y=0, z=0), 10)
