
def linespace(start: float, end: float, numberOfPoints: int) -> list:

    return [start + float(p) * (end - start) / (numberOfPoints - 1) for p in range(numberOfPoints)]

def flatten(listOfPoints: list) -> list:
    return [item for sublist in listOfPoints for item in sublist]

