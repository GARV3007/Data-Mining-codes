"""
Gourav Verma
DSC550 - Data Mining
Summer-2020
Week-4 : Assignment- 7.3.4 : BFR Algorithm
Book-Mining of Massive Datasets
"""

# Import important libraries
import numpy as np
import math

# Given 3 clusters
c1 = np.array([[4, 8], [4, 10], [6, 8], [7, 10]])
c2 = np.array([[9, 3], [10, 5], [11, 4], [12, 3], [12, 6]])
c3 = np.array([[2, 2], [3, 4], [5, 2]])


def cal_BFR(c):
    """
    Function to calculate BRF representations
    """
    # Initialize the variables
    n = len(c)
    sumc = [0, 0]
    sumsqc = [0, 0]
    varc = [0, 0]
    sdc = [0, 0]

    for i in range(n):                     # Loop for number of elements in cluster
        sumc[0] += c[i][0]                 # Calculate SUM
        sumc[1] += c[i][1]
        sumsqc[0] += pow(c[i][0], 2)       # Calculate SUM SQUARE
        sumsqc[1] += pow(c[i][1], 2)

    print('==> Cluster - ', c)
    print('N for cluster is     : ', n)
    print('SUM for cluster is   : ', sumc)
    print('SUMSQ for cluster is : ', sumsqc, '\n')

    varc[0] = round(sumsqc[0]/n - pow(sumc[0]/n, 2), 2)    # Calculate Variance for 1st dimension
    varc[1] = round(sumsqc[1]/n - pow(sumc[1]/n, 2), 2)    # Calculate Variance for 2nd dimension

    sdc[0] = round(math.sqrt(varc[0]), 2)                  # Calculate Standard Deviation for 1st dimension
    sdc[1] = round(math.sqrt(varc[1]), 2)                  # Calculate Standard Deviation for 2nd dimension

    print('Variance for cluster is : ', varc)
    print('Standard Deviation for cluster is : ', sdc, '\n')

    return


if __name__ == '__main__':
    print('\n(a) Compute the representation of the cluster as in the BFR Algorithm. Compute N, SUM, and SUMSQ.')
    print('(b) Compute the variance and standard deviation of each cluster in each of the two dimensions.\n')
    cal_BFR(c1)
    cal_BFR(c2)
    cal_BFR(c3)

