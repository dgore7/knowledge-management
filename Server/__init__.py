__copyright__ = "Copyright 2017. DePaul University. "
__license__ =  "All rights reserved. This work is distributed pursuant to the Software License for Community Contribution of Academic Work, dated Oct. 1, 2016. For terms and conditions, please see the license file, which is included in this distribution."
__author__ = "Ayadullah Syed, Jose Palacios, David Gorelik, Joshua Smith, Jasmine Farley, Jessica Hua, Steve Saucedo, Serafin Balcazar"


connections = []


class verboseFunc:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print("\n=========== Entering " + self.func.__name__ + " ===========\n")
        print("called with: ")
        print('\targs: ', args)
        print('\tkwargs: ', kwargs)
        result = self.func(*args, **kwargs)
        print("\n=========== Exiting " + self.func.__name__ + " ===========\n")
        return result