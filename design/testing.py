from design.geometries.shapes import varyingArc, spiral, helix, polar_function_1, polar_function_2, generatePolarShape
from transform.geometryToPlot import pointsIndiciesToStrRepresentation
from design.point import Point
import math
from visualizator import main


#varc = varyingArc(Point(x = 0, y = 0, z = 0), 30, 90, 0, 3, 100)
#varc = spiral(Point(x = 0, y = 0, z = 0), 30, 90, 0, 13, 100)
varc = helix(Point(x = 0, y = 0, z = 0), 30, 30, 0, 33, 0, 100, 100)
# Generate points for the first polar equation
#varc = generatePolarShape(Point(x = 0, y = 0, z = 0), polar_function_1, start_angle=0, end_angle=2 * math.pi, segments=500)
#varc = helix(Point(x = 0, y = 0, z = 0), 30, 30, 0, 13, 0, 100, 100)
listOfPoints = pointsIndiciesToStrRepresentation(varc)
print(listOfPoints)
softwareRender = main.SoftwareRender(listOfPoints)
softwareRender.run()