
def geometryDecorator(shape_function):
    def wrapper(*args, **kwargs):
        list_of_points = shape_function(*args, **kwargs)
        return {'shape': list_of_points}
    return wrapper
