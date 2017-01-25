from __future__ import division
import numpy as np

""" TEST """

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

    def sigmoid(self, wx, b):
        """
        Base Sigmoid function
        input:
            wx:         (2d array)  sized as (K,N). Sum of the inner
                                    product of W and X, where W is a
                                    KxM data matrix and X is a MxN weight
                                    matrix.
            b:          (1d array)  bias or thershold
        return:
            y:          (2d array)  sigmoid function
        """
        y = 1. / (1. + np.exp(-(wx + np.dot(np.atleast_2d(b).T, np.ones((1, wx.shape[1]))))))

        return y

    def mf_sigm(self, x, b, c):
        """
        Sigmoid membership function
        input:
            x:          (1d array)  independent variable
            b:          (float)     offset or bias (magnitude)
            c:          (float)     controls width of the sigmoidal region about b
        return:
            y:          (1d array)  sigmoidal membership function
        """
        y = 1. / (1. + np.exp(- c * (x - b)))

        return y

    def mf_s(self, x, a, b):
        """
        S- membership function
        input:
            x:          (1d array)  independent variable
            b:          (float)     foot of function (from 0)
            c:          (float)     ceiling of function (to 1)
        return:
            y:          (1d array)  S- membership function
        """
        assert a <= b, 'a <= b is required.'

        y = np.ones(len(x))

        index = x <= a

        y[index] = 0

        index = np.logical_and(a <= x, x <= (a + b) / 2.)
        y[index] = 2. * ((x[index] - a) / (b - a)) ** 2.

        index = np.logical_and((a + b) / 2. <= x, x <= b)
        y[index] = 1 - 2. * ((x[index] - b) / (b - a)) ** 2.

        return y

    def mf_z(self, x, a, b):
        """
        Z- membership function
        input:
            x:          (1d array)  independent variable
            a:          (float)     ceiling where falling from 1
            b:          (float)     foot where zero
        return:
            y:          (1d array)  Z- membership function
        """
        assert a <= b, 'a <= b is required.'

        y = np.ones(len(x))

        idx = np.logical_and(a <= x, x < (a + b) / 2.)
        y[index] = 1 - 2. * ((x[index] - a) / (b - a)) ** 2.

        index = np.logical_and((a + b) / 2. <= x, x <= b)
        y[index] = 2. * ((x[index] - b) / (b - a)) ** 2.

        index = x >= b
        y[index] = 0

        return y

    def mf_trapezoidal(self, x, abcd):
        """
        Trapezoidal membership function
        input:
            x:          (1d array)  independent variable
            abcd:       (1d array)  len 4 vector.
                                    a <= b <= c <= d is required.
        return:
            y:          (1d array)  Trapezoidal membership function
        """

        assert type(abcd) == type([]), 'abcd parameter must have list type.'

        assert len(abcd) == 4, 'abcd parameter must have exactly four elements.'

        a, b, c, d = np.r_[abcd]

        assert a <= b and b <= c and c <= d, 'abcd requires the four elements \
                                              a <= b <= c <= d.'
        y = np.ones(len(x))

        index = np.nonzero(x <= b)[0]
        y[index] = trimf(x[index], np.r_[a, b, b])

        index = np.nonzero(x >= c)[0]
        y[index] = trimf(x[index], np.r_[c, c, d])

        index = np.nonzero(x < a)[0]
        y[index] = np.zeros(len(index))

        index = np.nonzero(x > d)[0]
        y[index] = np.zeros(len(index))

        return y

    def mf_triangular(self, x, abc):
        """
        Triangular membership function
        input:
            x:          (1d array)  independent variable
            abc:        (1d array)  len 3 vector.
                                    a <= b <= c is required.
        return:
            y:          (1d array)  triangular membership function
        """
        assert type(abc) == type([]), 'abc parameter must have list type.'

        assert len(abc) == 3, 'abc parameter must have exactly three elements.'

        a, b, c = np.r_[abc]     # Zero-indexing in Python

        assert a <= b and b <= c, 'abc requires the three elements a <= b <= c.'

        y = np.zeros(len(x))

        # Left side of triangle
        if a != b:
            index = np.nonzero(np.logical_and(a < x, x < b))[0]
            y[index] = (x[index] - a) / float(b - a)

        # Right side of triangle
        if b != c:
            index = np.nonzero(np.logical_and(b < x, x < c))[0]
            y[index] = (c - x[index]) / float(c - b)

        index = np.nonzero(x == b)
        y[index] = 1

        return y


    def mf_sigm_diff(self, x, b1, c1, b2, c2):
        """
        Return difference between two membership functions
        input:
            x:          (1d array)  independent variable
            b1:         (float)     midpoint of first sigmoid
            b2:         (float)     midpoint of second sigmoid
            c1:         (float)     width and sign of first sigmoid
            c2:         (float)     width and sign of second sigmoid
        return:
            y:          (1d array)  values, defined as y = f1 - f2
        """
        y = (self.sigmoid(x, b1, c=c1) - self.sigmoid(x, b2, c=c2))

        return y

    def mf_gauss(self, x, mean, sigma):
        """
        Return Gaussian membership function
        input:
            x:          (1d array)  array or iterable
            mean:       (float)     Gaussian parameter for center value
            sigma:      (float)     Gaussian parameter for standart deviation
        return:
            y:          (1d array)  Gaussian function for x
        """
        y = np.exp(-((x - mean) ** 2.) / float(sigma) ** 2.)

        return y

    def mf_gauss_combined(self, x, mean1, sigma1, mean2, sigma2):
        """
        Return Gaussian function of two combined Gaussian
        input:
            x:          (1d array)  or iterable
            mean1:      (float)     Gaussian parameter of center value
                                    of left-side Gaussian
            mean2:      (float)     Gaussian parameter of center value
                                    of right-side Gaussian
            sigma1:     (float)     standart deviation of left-side Gaussian
            sigma2:     (float)     standart deviation of right-side Gaussian
        return:
            y:          (1d array)  Membership function with left side up to `mean1` defined by the first
                                    Gaussian, and the right side above `mean2` defined by the second.
        """
        assert mean1 <= mean2, 'mean1 must be less then mean2'

        y = np.ones(len(x))

        index1 = x <= mean1
        index2 = x > mean2

        y[index1] = self.gaussian(x[index1], mean1, sigma1)
        y[index2] = self.gaussian(x[index2], mean2, sigma2)

        return y

    def mf_piece(self, x, abc):
        """
        Piecewise membership function
        input:
            x:          (1d array)  independent variable
            abc:        (1d array)  3 values [a, b c], define Piecewise funciton
                                    a <= b <= c is required
        return:
            y:          (1d array)  piecewise function
        """
        if (type(abd) != type([])):
            return None

        if len(abd) != 3:
            return None

        a, b, c = abc

        if c != x.max():
            c = x.max()

        assert a <= b and b <= c, '`abc` requires a <= b <= c.'

        n = len(x)

        y = np.zeros(n)

        index0 = _nearest(x, 0)[0]
        indexa = _nearest(x, a)[0]
        indexb = _nearest(x, b)[0]

        n = np.r_[0:n - index0]

        y[index0 + n] = n / float(c)
        y[index0:indexa] = 0

        m = np.r_[0:indexb - indexa]

        y[indexa:indexb] = b * m / (float(c) * (b - a))

        return y / y.max()

    def mf_gbell(self, a, b, c):
        """
        Generalized Bell membership function
        input:
            x:          (1d array)  independent variable
            a:          (float)     Bell function parameter (width)
            b:          (float)     Bell function parameter (slope)
            c:          (float)     Bell function parameter (center)
        return:
            y:          (1d array)  Generalized Bell function
        """
        y = 1. / (1. + np.abs((x - c) / a) ** (2 * b))
        return y

    def mf_pi(self, x, a, b, c, d):
        """
        Pi- membership function. Equivalently a product of SMF and ZMF
        input:
            x:          (1d array)  independent variable
            a:          (float)     left foot
            b:          (float)     left cailing
            c:          (float)     right foot
            d:          (float)     right ceiling
        return:
            y:          (1d array)  Pi-function
        """
        y = np.ones(len(x))
        assert a <= b and b <= c and c <= d, 'a <= b <= c <= d is required.'

        index = x <= a
        y[index] = 0

        index = np.logical_and(a <= x, x <= (a + b) / 2.)
        y[index] = 2. * ((x[index] - a) / (b - a)) ** 2.

        index = np.logical_and((a + b) / 2. < x, x <= b)
        y[index] = 1 - 2. * ((x[index] - b) / (b - a)) ** 2.

        index = np.logical_and(c <= x, x < (c + d) / 2.)
        y[index] = 1 - 2. * ((x[index] - c) / (d - c)) ** 2.

        index = np.logical_and((c + d) / 2. <= x, x <= d)
        y[index] = 2. * ((x[index] - d) / (d - c)) ** 2.

        index = x >= d
        y[index] = 0

        return y

    def mf_sigm_product(self, x, b1, c1, b2, c2):
        """
        Product of two mf_sigm functions
        input:
            x:          (1d array)  independent variable
            b1:         (float)     offset or bias of first sigmoind (magnitude)
            c1:         (float)     controls width of the first sigmoidal region about b1
            b2:         (float)     offset or bias of second sigmoid
            c2:         (float)     controls width of the second sigmoidal region about b2
        return:
            y:          (1d array)  values. defined as y = f1(x) * f2(x)
        """
        y = sigmf(x, b1, c1) * sigmf(x, b2, c2)
        return y

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
