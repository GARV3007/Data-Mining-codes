"""
Gourav Verma
DSC550 - Data Mining
Summer-2020
Week-4 : Assignment- 7.3.5 : Mahalanobis distance
Book-Mining of Massive Datasets
"""
# Import important libraries
import numpy as np
import math

# Given dimension
d = 3

# Given origin/centroid
o = np.array([0, 0, 0])

# Given point
p = np.array([1, -3, 4])

# Given standard deviation
sd = np.array([2, 3, 5])

sumsq = 0
for i in range(d):
    sumsq += pow((p[i] - o[i])/sd[i], 2)           # Calculate sum of squares

mahalanobis = round(math.sqrt(sumsq), 2)           # Calculate sq root of squares -> Mahalanobis distance

print('\nThe Mahalanobis distance between p(1,-3,4) and c(0,0,0) is - ', mahalanobis)
