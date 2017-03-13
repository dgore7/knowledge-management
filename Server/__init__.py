__author__ = 'JosePalacios'
connections = []


class verboseFunc:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print("\n=========== Entering " + self.func.__name__ + " ===========\n")
        print("called with: ")
        print(locals())
        print('\targs: ', args)
        print('\tkwargs: ', kwargs)
        result = self.func(*args, **kwargs)
        print("\n=========== Exiting " + self.func.__name__ + " ===========\n")
        return result