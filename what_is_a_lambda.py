
sample_iterable = [({'feature':4},5),({'feature':4}, 5),({'feature':4},5)]

def get_feature(x):
    return x['feature']

result = map(lambda x : get_feature(x[0]) + x[1], sample_iterable)

alternate_result = ((lambda x,y : x['feature'] + y)(*args) for args in sample_iterable)