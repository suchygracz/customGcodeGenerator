from design import *
from visualizator import *
from transform import *

# Now use Point in your code
listOfInstruction = []

#my_rectangle = rectangle(Point(x=0, y=0, z=0), 10, 10)
my_circle = circle(Point(x=0, y=0, z=0), 10)
myCircleInfill = solidLayerInfill(my_circle, 0.6, 'x')


listOfInstruction.append(my_circle)
listOfInstruction.extend(myCircleInfill)

#print(listOfInstruction)

visualize(listOfInstruction)

parseStepsToGcode(listOfInstruction, 'outputt.gcode', [0.4, 0.2], hotendTemp=200, bedTemp=60)

