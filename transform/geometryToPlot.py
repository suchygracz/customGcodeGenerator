import design
from design.geometricTools.baseTools import flatten, flattenPoints

from design.point import Point
"""
point = Point(x = 1, y = 2, z = 3)
print(point)
listA = []
listA.append(Point(x = 1.0, y = 1.0, z = 1.0))
listA.append(rectangle(Point(x = 1.0, y = 1.0, z = 1.0), 4, 6))
print(listA)
listFlat = flattenPoints(listA)
print(listFlat)
"""
"""
counter = 0
for point in listFlat:
    counter +=1
    if counter < len(listFlat):
        print(f"{point},")
    else:
        print(point)
    
"""
pt = Point(x = 1.0, y = 1.0, z = 1.0)
print(pt)

def pointsIndiciesToStrRepresentation(points: list) -> list:

    flatList = flattenPoints(points)
    counter = 0
    listOfPoints = []
    for point in flatList:
        counter += 1
        if counter < len(flatList):
            listOfPoints.append(point.listRepresentation())
            #print(f"{point},")
        else:
            #print(point)
            listOfPoints.append(point.listRepresentation())
    return listOfPoints
