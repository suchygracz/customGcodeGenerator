from numpy.ma.core import shape
from manim import *

from design.geometricTools.extraTools import nonPlanarVase, vaseMode, solidLayerInfill
from design.geometricTools.vector import Vector
from design.geometries.curves import sinusoidalWave, cosineWave, squareWave, tringleWave, cubic_bezier_curve, bezier_curve_de_casteljau, cardinal_spline, nurbs_curve
from design.geometries.shapes import varyingArc, spiral, helix, polar_function_1, polar_function_2, generatePolarShape, polygon, circle, rectangle, square, arcXY
from design.layer import Layer
from transform.transformations import pointsIndiciesToStrRepresentation, parseStepsToGcode
from design.geometricTools.baseTools import move, scale, rotate, copy
from design.point import Point
from design.layer import Layer
from math import pi, sin, cos
from visualizator import main
from visualizator.main import visualize
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
listOfPoints = varc['shape']

listOfPoints += movedCircle['shape']
"""
"""
sq = square(Point(x = 0, y = 0, z = 0), 30)
#scaledCircle = scale(varc, 2, 'xy')
rotatedCircle = rotate(sq, 1, 'z', False)
print(sq)
#listOfPoints = sq['shape']

listOfPoints = rotatedCircle['shape']
"""

lista_instrukcji = []
listOfPoints = []


#polarShape2 = generatePolarShape(Point(x = 0, y = 0, z = 0), polar_function_2, start_angle=0, end_angle=10 * pi, segments=300)
#rotated = rotate(polarShape, 1, 'z', True)

#cardinalS = cardinal_spline([Point(x = 0, y = 0, z = 0), Point(x = 10, y = 10, z = 0), Point(x = 20, y = 0, z = 0), Point(x = 30, y = 10, z = 0), Point(x = 40, y = 0, z = 0)], 0, 1000)
'''
#simple low res circle
circle = circle(Point(x = 0, y = 0, z = 0), 30, 8)
listOfPoints = [circle]
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




# Generate the NURBS curve points using the extended control points
#nurbs_points = nurbs_curve(control_points, weights, degree, 122)



'''
b =11999//100
print(len(nurbs_points['shape']))
print(nurbs_points['shape'][b])
'''
'''
heliks = helix(Point(x = 0, y = 0, z = 0), 30, 30, 0, 200, 0, 80, 3000)
for point in heliks['shape']:
    lista_instrukcji.append(moveWithNoExtrusion(point))
    lista_instrukcji.append(stationaryExtrusion(7,100))
'''

#listOfPoints.append(stationaryExtrusion)

#listOfPoints.append(polarShape)
#listOfPoints.append(rotated)
#listOfPoints.append(moveWithNoExtrusion(Point(x = 0, y = 0, z = 0)))
#print(polarShape)
#write a test that test move, rotate, scale function from baseTools.py on all the shapes and waves
# so all of those: sinusoidalWave, squareWave, tringleWave, cubic_bezier_curve, bezier_curve_de_casteljau, varyingArc, spiral, helix, polar_function_1, polar_function_2, generatePolarShape, polygon, circle, rectangle, square
# and then test the visualizator with the result of the test
# Append different types of commands


#listOfPoints.append(stationaryExtrusion(50, 600))

#listOfPoints.append(retraction(5))
#sE = stationaryExtrusion(50,300)
#listOfPoints.append(sE)


'''
# stationary extrusion and move with no extrusion
listOfPoints.append(stationaryExtrusion(50, 600))
listOfPoints.append(stationaryExtrusion(75, 400))
listOfPoints.append(stationaryExtrusion(75, 400))
listOfPoints.append(moveWithNoExtrusion(Point(x=50, y=50, z=0)))
listOfPoints.append(stationaryExtrusion(100, 500))
listOfPoints.append(retraction(5))
'''
#listOfPoints.append(retraction(5))
#print(listOfPoints)

#vase = vaseMode(polarShape2, 50, 0.6, 0.3)
'''
#listOfPoints.append(vase)
base_point = Point(x = 0, y = 0, z = 0.17)
base_shape = circle(base_point, 30, 100)
#gcode = parseStepsToGcode(listOfPoints, 'output.gcode', [0.4, 0.2], hotendTemp=200, bedTemp=60)

listOfPoints.append(arcXY(Point(x = 0, y = 0, z = 0), 30, 0, pi, 100))
listOfPoints.append(moveWithNoExtrusion(Point(x = -30, y = -0.6, z = 0)))
listOfPoints.append(arcXY(Point(x = 0, y = -0.6, z = 0), 30, pi, 2*pi, 100))
listOfPoints.append(circle(Point(x = -30, y = -30.3, z = 0), 30, 100))
'''

'''
#Krok 0: Zadeklaruj listę instrukcji

listOfInstructions = []

# Krok 1: Zdefiniuj punkt bazowy
# pamiętaj by zacząć pierwszą warstwe minimalnie niżej niż wysokość lini drukowania dla
# poprawienia przywierania druku do stołu roboczego
#pamiętaj, by przy definiowaniu punktów używać zapisu Point(x=0, y=0, z=0.17) gdyż Point(0, 0, 0.17) wywoła błąd
base_point = Point(x=0, y=0, z=0.17)

# Krok 2: zdefiniuj kształt podstawy
base_shape = circle(base_point, 30, 100)

# Krok 3: stwórz wypełnienie kształtu bazowego
infill = solidLayerInfill(base_shape, 0.6, 'x')

# Krok 4: stwórz wazę z kształtu bazowego
vase = vaseMode(base_shape, 150, 0.6, 0.2)

# Krok 5: Dodaj kształt bazowy, wypełnienie i wazę do listy instrukcji kolejność ma znaczenie!
listOfInstructions.append(base_shape)
listOfInstructions.extend(infill)
listOfInstructions.append(vase)

# Krok 6: Zwerifikuj listę instrukcji za pomocą wizualizacji


# Krok 7: Po zweryfikowaniu designu, zapisz listę instrukcji do pliku G-code
parseStepsToGcode(listOfInstructions, 'output.gcode', [0.4, 0.2], hotendTemp=200, bedTemp=60)
'''


'''
okrąg = circle(Point(x=0, y=0, z=0), 75, 1000)

#okrąg = generatePolarShape(Point(x=0, y=0, z=0), polar_function_1, start_angle=0, end_angle=2 * pi, segments=1000)




myWave = sinusoidalWave(Point(x=0, y=0, z=0), 0, 5, 10, 10, 100)
for i in range(0, 1000):
    okrąg['shape'][i].z += myWave['shape'][i].y

secondCircle = move(okrąg, Vector(x=0, y=0, z=10.2))
secondRotatedCircle = rotate(secondCircle, 0.1*pi, 'z', True)
for i in range(0, 1000):
    secondRotatedCircle['shape'][i].z += myWave['shape'][i].y

lista_instrukcji.append(okrąg) 
lista_instrukcji.append(secondRotatedCircle)

for i in range(0, 10):
    lista_instrukcji.append(move(okrąg, Vector(x=0, y=0, z=20.4*i)))
    lista_instrukcji.append(move(secondRotatedCircle, Vector(x=0, y=0, z=20.4*i)))
'''


#move(secondCircle, Vector(x=0, y=0, z=10))
#rotationAngle = 0.1*pi
#rotatedCircle = rotate(secondCircle, rotationAngle, 'z', True)

#fRectangle = rectangle(Point(x=0, y=0, z=0), 30, 30)
#move(fRectangle, Vector(x=0, y=0, z=10))
#sRectangle = rotate(fRectangle, rotationAngle, 'z', False)

okrąg = circle(Point(x=0, y=0, z=0), 75, 1000)

#squareWaveee = squareWave(Point(x=0, y=0, z=0), 0, 5, 10, 10,100)

#myWave = sinusoidalWave(Point(x=0, y=0, z=0), 0, 5, 10, 10, 100)

myWave = cosineWave(Point(x=0, y=0, z=0), 0, 5, 10, 10, 100)



lista_instrukcji.append(myWave)

for i in range(0, 1000):
    okrąg['shape'][i].z += myWave['shape'][i].y

print('points: \n')
print(okrąg['shape'])
print('\n points end')

secondCircle = move(okrąg, Vector(x=0, y=0, z=10.2))
secondRotatedCircle = rotate(secondCircle, 0.1*pi, 'z', True)
for i in range(0, 1000):
    secondRotatedCircle['shape'][i].z += myWave['shape'][i].y

lista_instrukcji.append(okrąg) 
lista_instrukcji.append(secondRotatedCircle)

for i in range(0, 10):
    #lista_instrukcji.append(stationaryExtrusion(5,5))
    lista_instrukcji.append(move(okrąg, Vector(x=0, y=0, z=20.4*i)))
    #lista_instrukcji.append(retraction(5))
    lista_instrukcji.append(move(secondRotatedCircle, Vector(x=0, y=0, z=20.4*i)))


'''
mcircle = circle(Point(x = 0, y = 0, z = 0), 30, 1000)
circinfill = solidLayerInfill(mcircle, 0.6)
vase = vaseMode(mcircle, 120, 0.6, 0.2)
listOfPoints = [mcircle]
listOfPoints.extend(circinfill)
listOfPoints.append(vase)
'''


'''
#creation of non polar vase with infill
polarShape = generatePolarShape(Point(x = 0, y = 0, z = 0), polar_function_1, start_angle=0, end_angle=2 * pi, segments=300)
infill = solidLayerInfill(polarShape, 0.6, 'x')
listOfPoints = [polarShape]
listOfPoints.extend(infill)
#nonPlanarV = nonPlanarVase(polarShape, 1.6, 50, 0.6, 0.3)
vase = vaseMode(polarShape, 50, 0.6, 0.3)
listOfPoints.append(vase)
#listOfPoints.append(nonPlanarV)
'''


#visualize(lista_instrukcji)
#visualize(listOfPoints)
#parseStepsToGcode(lista_instrukcji, 'outputt.gcode', [0.4, 0.2], hotendTemp=200, bedTemp=60)





#softwareRender = main.SoftwareRender(listOfPoints)
#softwareRender.run()