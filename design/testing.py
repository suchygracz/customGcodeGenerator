from numpy.ma.core import shape

from design.geometricTools.extraTools import nonPlanarVase, vaseMode, solidLayerInfill
from design.geometricTools.vector import Vector
from design.geometries.curves import sinusoidalWave, squareWave, tringleWave, cubic_bezier_curve, bezier_curve_de_casteljau, cardinal_spline, nurbs_curve
from design.geometries.shapes import varyingArc, spiral, helix, polar_function_1, polar_function_2, generatePolarShape, polygon, circle, rectangle, square
from design.layer import Layer
from transform.transformations import pointsIndiciesToStrRepresentation, parseStepsToGcode
from design.geometricTools.baseTools import move, scale, rotate
from design.point import Point
from design.layer import Layer
from math import pi, sin, cos
from visualizator import main
from design.directCommands.commands import moveWithNoExtrusion, stationaryExtrusion, retraction



#varc = varyingArc(Point(x = 0, y = 0, z = 0), 30, 90, 0, 3, 100)
"""
varc = spiral(Point(x = 0, y = 0, z = 0), 30, 90, 0, 13, 100)
moovedSpiral = move(varc, Vector(x = 0, y = 0, z = 100))
"""
#varc = helix(Point(x = 0, y = 0, z = 0), 30, 30, 0, 33, 0, 100, 100)
#varc = polygon(Point(x = 0, y = 0, z = 0), 30, 5)
#varc = sinusoidalWave(Point(x = 0, y = 0, z = 0), 0, 5, 10, 15)
#varc = squareWave(Point(x = 0, y = 0, z = 0), 0, 5, 10, 15)
#varc = tringleWave(Point(x = 0, y = 0, z = 0), 0, 5, 10, 15)
# Generate points for the first polar equation
#varc = generatePolarShape(Point(x = 0, y = 0, z = 0), polar_function_1, start_angle=0, end_angle=2 * pi, segments=100)
#varc = helix(Point(x = 0, y = 0, z = 0), 30, 30, 0, 13, 0, 100, 100)

# Define control points
P0 = Point(x=0, y=0)
P1 = Point(x=10, y=20)
P2 = Point(x=15, y=5)
P3 = Point(x=20, y=30)
P4 = Point(x=25, y=10)
P5 = Point(x=30, y=50)
P6 = Point(x=40, y=3)

#varc = rectangle(Point(x = 0, y = 0, z = 0), 30, 30)

#varc = polygon(Point(x = 0, y = 0, z = 0), 30, 5)
#print(varc)
#layer = Layer(listOfPoints = varc)

# Generate the Bézier curve points
#varc = cubic_bezier_curve(P0, P1, P2, P3, 200)
#varc = bezier_curve_de_casteljau([P0, P1, P2, P3, P4, P5, P6], 200)

#combining shapes
"""
listOfPoints = pointsIndiciesToStrRepresentation(varc)
listOfPoints2 = pointsIndiciesToStrRepresentation(moovedSpiral)
combined = listOfPoints + listOfPoints2
"""
#print(listOfPoints)
#print(combined)
#print(pointsIndiciesToStrRepresentation(varc))
#print (layer)
"""
varc = polygon(Point(x = 0, y = 0, z = 0), 30, 5)
#scaledCircle = scale(varc, 2, 'xy')
movedCircle = rotate(varc, 1, 'z')
print(varc)
listOfPointsAcr = varc['shape']

listOfPointsAcr += movedCircle['shape']
"""
"""
sq = square(Point(x = 0, y = 0, z = 0), 30)
#scaledCircle = scale(varc, 2, 'xy')
rotatedCircle = rotate(sq, 1, 'z', False)
print(sq)
#listOfPointsAcr = sq['shape']

listOfPointsAcr = rotatedCircle['shape']
"""


polarShape2 = generatePolarShape(Point(x = 150, y = 0, z = 0), polar_function_1, start_angle=0, end_angle=2 * pi, segments=300)
#rotated = rotate(polarShape, 1, 'z', True)

cardinalS = cardinal_spline([Point(x = 0, y = 0, z = 0), Point(x = 10, y = 10, z = 0), Point(x = 20, y = 0, z = 0), Point(x = 30, y = 10, z = 0), Point(x = 40, y = 0, z = 0)], 0, 1000)
'''
#simple low res circle
circle = circle(Point(x = 0, y = 0, z = 0), 30, 8)
listOfPoints = [circle]
'''

circle = circle(Point(x = 0, y = 0, z = 0), 20, 100)
circinfill = solidLayerInfill(circle, 0.6)
vase = vaseMode(circle, 120, 0.6, 0.2)
listOfPoints = [circle]
listOfPoints.extend(circinfill)
listOfPoints.append(vase)

#creation of non polar vase with infill

'''
polarShape = generatePolarShape(Point(x = 0, y = 0, z = 0), polar_function_1, start_angle=0, end_angle=2 * pi, segments=300)
infill = solidLayerInfill(polarShape, 0.6)
listOfPoints = [polarShape]
listOfPoints.extend(infill)
nonPlanarV = nonPlanarVase(polarShape, 3.6, 50, 0.6, 0.3)
listOfPoints.append(nonPlanarV)
'''
control_points = [
    Point(x=0, y=0, z=0),
    Point(x=10, y=20, z=0),
    Point(x=20, y=0, z=0),
    Point(x=30, y=40, z=0),
    Point(x=50, y=20, z=0),
    Point(x=70, y=0, z=0)
]

# Define uniform weights
weights = [1, 1, 1, 1, 1, 1]

# Degree of the curve
degree = 3

# Knot vector (open configuration)
knot_vector = [0, 0, 0, 1, 2, 4, 7, 9, 9, 9]

stationaryExtrusion = stationaryExtrusion(50,300)

# Generate the NURBS curve points using the extended control points
nurbs_points = nurbs_curve(control_points, weights, degree)
#listOfPoints = [nurbs_points]
#listOfPoints.append(stationaryExtrusion)

#listOfPointsAcr.append(polarShape)
#listOfPointsAcr.append(rotated)
#listOfPointsAcr.append(moveWithNoExtrusion(Point(x = 0, y = 0, z = 0)))
#print(polarShape)
#write a test that test move, rotate, scale function from baseTools.py on all the shapes and waves
# so all of those: sinusoidalWave, squareWave, tringleWave, cubic_bezier_curve, bezier_curve_de_casteljau, varyingArc, spiral, helix, polar_function_1, polar_function_2, generatePolarShape, polygon, circle, rectangle, square
# and then test the visualizator with the result of the test
"""
listOfPointsAcr.append(stationaryExtrusion(50, 600))
listOfPointsAcr.append(moveWithNoExtrusion(Point(x = 25, y = 25, z = 0)))
listOfPointsAcr.append(stationaryExtrusion(50, 600))
listOfPointsAcr.append(moveWithNoExtrusion(Point(x = 50, y = 50, z = 0)))
listOfPointsAcr.append(stationaryExtrusion(50, 600))
listOfPointsAcr.append(moveWithNoExtrusion(Point(x = 70, y = 70, z = 0)))
"""
#listOfPointsAcr.append(retraction(5))
#print(listOfPointsAcr)

#vase = vaseMode(polarShape2, 50, 0.6, 0.3)

#listOfPointsAcr.append(vase)


gcode = parseStepsToGcode(listOfPoints, 'output.gcode', [0.4, 0.2])
softwareRender = main.SoftwareRender(listOfPoints)
softwareRender.run()