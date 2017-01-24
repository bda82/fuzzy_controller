from __future__ import division
import numpy as np

class Functions:
    def __init__(self):
        """
        https://github.com/scikit-fuzzy/scikit-fuzzy/blob/master/skfuzzy/membership/generatemf.py
        """
        pass

    def __del__(self):
        pass

    def nearest(self, x, y):
        """
        input:
            x:          (1d array)  input array
            y:          (float)     matching value
        return :
            index:      (float)     index of nearest value
            x[index]:   (float)     nearest value from x array
        """
        dist = np.abs(x - y)
        index = np.nonzero(dist == dist.min())[0][0]
        return  index, x[index]

    def difference_of_sigmoid(self, x, b1, c1, b2, c2):
        """
        Return difference between two membership functions
        input:
            x:      (1d array)  independent variable
            b1:     (float)     midpoint of first sigmoid
            b2:     (float)     midpoint of second sigmoid
            c1:     (float)     width and sign of first sigmoid
            c2:     (float)     width and sign of second sigmoid
        return:
            y:      (1d array)  values, defined as y = f1 - f2
        """
        y = (self.sigmoid(x, b1, c=c1) - self.sigmoid(x, b2, c=c2))
        return y

    def gaussian(self, x, mean, sigma):
        """
        Return Gaussian membership function
        input:
            x:      (1d array)  array or iterable
            mean:   (float)     Gaussian parameter for center value
            sigma:  (float)     Gaussian parameter for standart deviation
        return:
            y:      (1d array)  Gaussian function for x
        """
        y = np.exp(-((x - mean) ** 2.) / float(sigma) ** 2.)
        return y

    def gaussian_combined(self, x, mean1, sigma1, mean2, sigma2):
        """
        Return Gaussian function of two combined Gaussian
        input:
            x:      (1d array)  or iterable
            mean1:  (float)     Gaussian parameter of center value
                                of left-side Gaussian
            mean2:  (float)     Gaussian parameter of center value
                                of right-side Gaussian
            sigma1: (float)     standart deviation of left-side Gaussian
            sigma2: (float)     standart deviation of right-side Gaussian
        return:
            y:      (1d array)  Membership function with left side up to `mean1` defined by the first
                                Gaussian, and the right side above `mean2` defined by the second.
        """
        assert mean1 <= mean2, 'mean1 must be less then mean2'
        y = np.ones(len(x))
        index1 = x <= mean1
        index2 = x > mean2
        y[index1] = self.gaussian(x[index1], mean1, sigma1)
        y[index2] = self.gaussian(x[index2], mean2, sigma2)
        return y

    def sigmoid(self, x, b, c):
        pass



class Fuzzyfication:
    def __init__(self):
        pass

    def __del__(self):
        pass

class Defuzzification:
    def __init__(self):
        pass

    def __del__(self):
        pass

class Rules:
    def __init__(self):
        pass

    def __del__(self):
        pass
