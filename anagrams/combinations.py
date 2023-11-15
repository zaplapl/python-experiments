from itertools import starmap
import operator

vec1 = (2, 3)
vec2 = (4, 5)
product = sum(starmap(operator.mul, zip(vec1, vec2)))
