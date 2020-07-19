"""
Gourav Verma
DSC550 - Data Mining
Summer-2020
Week-6 : Exercise 12.4.3 (a) & (b) : Nearest Neighbor
Books-Mining of Massive Datasets
"""
# Import important libraries
import numpy as np
import matplotlib.pyplot as plt
import traceback


def get_xy(points):
    """
    Function to get x and y points
    """
    x = []
    y = []
    for i in range(len(points)):
        x.append(points[i][0])
        y.append(points[i][1])
    return x, y


def get_avg(x, y):
    """
    Function to calculate average of y points
    """
    ya = []
    for i in range(len(y)-1):
        ya.append((y[i]+y[i+1])/2)
    xa = x[:5]
    return xa, ya


if __name__ == '__main__':
    # Given set of points
    points = np.array([[1, 1], [2, 2], [4, 3], [8, 4], [16, 5], [32, 6]])

    # Get individual x and y points
    x, y = get_xy(points)

    try:
        # 12.4.3 (a)
        # Plot the step graph for nearest neighbors
        title = 'Nearest Neighbors'
        plt.step(x, y)
        plt.plot(x, y, 'bo')
        plt.xticks(x)
        plt.title(title)
        plt.show()

        # 12.4.3 (b)
        # Get average points
        xa, ya = get_avg(x, y)

        # Plot the step graph for average of nearest neighbors
        title = 'Average of Nearest Neighbors'
        plt.step(xa, ya)
        plt.plot(x, y, 'bo')
        plt.xticks(x)
        plt.yticks(ya)
        plt.title(title)
        plt.show()

    except Exception as exception:
        print('exception')
        traceback.print_exc()
        print('\nAn exception of type {0} occurred. Arguments:\n{1!r}'.format(type(exception).__name__, exception.args))
    finally:
        print("\nfinally block is executed whether exception is handled or not!!")

