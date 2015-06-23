__author__ = 'irismonster'
from random import randint
import numpy as np

def meanStream():
    mean = 0
    count = 0
    for i in range (1000):
        print(i)
        mean = mean + (i - mean) / (count + 1)
        count = count + 1
        print(mean)

def varianceStream():
    variance = 0
    count = 0
    mean = 0
    squares = 0
    for i in range(100):
        number = randint(1,100)
        count = count + 1
        mean = mean + (number - mean) / (count)
        squares = squares + (number - mean) * (number - mean)
        variance = squares / (count)
        print(mean)
        print(variance)

def LRstream():
    X = np.random.randint(low=1, high=10, size=(1000,4))
    B = np.matrix('4 3 2 5')
    Y = []
    A = np.matrix('1 0 0 0; 0 1 0 0; 0 0 1 0; 0 0 0 1')
    b = np.matrix('0 0 0 0; 0 0 0 0; 0 0 0 0; 0 0 0 0')
    for i in range(1000):
        g = np.multiply(X[i], B)
        y = g.sum()

        A = A + X[i] * X[i][np.newaxis].T
        b = b + X[i] * y
    Bs = A.getI() * b
    print(Bs)

LRstream()

me