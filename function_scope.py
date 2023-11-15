def BMI(weight, height):
    breakpoint()
    return weight / height**2


def bmi_curried(height):
    def bmi_weight(weight):
        return BMI(weight, height)

    return bmi_weight


def bmi_scoped(height):
    locally_bound_height = height * 2

    def bmi_scoped_weight(weight):
        return BMI(weight, locally_bound_height)

    return bmi_scoped_weight


from copy import copy, deepcopy


def get_locally_scoped_object_key(object, key):
    locally_bound_object = deepcopy(object)

    def get_key(key):
        inner_object = object
        return inner_object.get(key)

    return get_key(key)
