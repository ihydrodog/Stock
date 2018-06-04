import pandas as pd
import numpy as np

import scipy.optimize as spo

def f(X):
    Y = (X-1.5)**2 + 0.5

    return Y



def test_run():
    Xguess = 2.0

    min_result = spo.minimize( f, Xguess, method='SLSQP', options={'disp':True})

    print( min_result)



if __name__ == "__main__":
    test_run()