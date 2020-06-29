import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
import random as rand
from sys import maxsize
from sklearn import datasets

print(__doc__)

'''sigma is actually covariance, which is either spherical or diagonal type 
Covariance indicates the level to which two variables vary together
From the multivariate normal distribution, we draw N-dimensional samples, 
X = [x_1, x_2, ... x_N]. The covariance matrix element C_{ij} is the covariance 
of x_i and x_j.           
The element C_{ii} is the variance of x_i (i.e. its “spread”).
Diagonal covariance (cov has non-negative elements, and only on the diagonal)
Diagonal covariance means that points are oriented along x or y-axis:
Note that the covariance matrix must be positive semidefinite    
'''
iris = datasets.load_iris()
X = iris.data[:, :2]  # we only take the first two features.
Y = iris.target
Y[:] = Y + 1  # labelling the data in (1,2,3)

data = {'x': X[:, 0], 'y': X[:, 1], 'label': Y}
df = pd.DataFrame(data=data)

# Y.tolist()

# inspect the data
print(df.head())
df.tail()

# Visualize the iris data
fig = plt.figure()
plt.scatter(data['x'], data['y'], 34, c=Y)
fig.savefig("Actual_Iris_data_spread.png")

''' Initialize three random index'''
k1 = rand.randrange(len(X))
k2 = rand.randrange(len(X))
k3 = rand.randrange(len(X))

''' make intial guess using the three choosen random index'''
guess = {'mu1': [X[k1, 0], X[k1, 1]],
         'sig1': [[1, 0], [0, 1]],
         'mu2': [X[k2, 0], X[k2, 1]],
         'sig2': [[2, 0], [0, 1]],
         'mu3': [X[k3, 0], X[k3, 1]],
         'sig3': [[0.5, 0], [0, 1]],
         'lambda': [0.3, 0.3, 0.4]
         }

'''guess = { 'mu1': [np.random.choice(X[:k,0]),np.random.choice(X[:k,1])],
          'sig1': [ [1, 0], [0, 1] ],
          'mu2': [np.random.choice(X[k+1:ke,0]),np.random.choice(X[k+1:ke,1])],
          'sig2': [ [1, 0], [0, 1] ],
          'mu3': [np.random.choice(X[ke+1:,0]),np.random.choice(X[ke+1:,1])],
          'sig3': [ [0.5, 0], [0, 1] ],
          'lambda': [0.3, 0.3, 0.4]
        }
'''


#  lambda is the probablility that the point comes from that particular gaussian
# note that the covariance must be diagonal for this to work

# Probability of data point Val belonging to a cluster
def prob(val, mu, sig, lam):
    p = lam
    for i in range(len(val)):
        p *= norm.pdf(val[i], mu[i], sig[i][i])
    return p


# Expectation step - checking to which cluster the data point is expected to be came
# from given the initial parameter setting
def expectation(dataFrame, parameters):
    # print 'dataFrame.shape[0]:', dataFrame.shape[0]
    for i in range(dataFrame.shape[0]):
        x = dataFrame['x'][i]
        y = dataFrame['y'][i]
        # assigning the probablilities of each cluster
        p_cluster1 = prob([x, y], list(parameters['mu1']), list(parameters['sig1']), parameters['lambda'][0])
        p_cluster2 = prob([x, y], list(parameters['mu2']), list(parameters['sig2']), parameters['lambda'][1])
        p_cluster3 = prob([x, y], list(parameters['mu3']), list(parameters['sig3']), parameters['lambda'][2])
        # Labelling each data according to the probabilities of cluster
        if (p_cluster1 >= p_cluster2) & (p_cluster1 >= p_cluster3):
            #dataFrame['label'][i] = 1
            dataFrame.loc[i, 'label'] = 1
        elif (p_cluster2 >= p_cluster1) & (p_cluster2 >= p_cluster3):
            #dataFrame['label'][i] = 2
            dataFrame.loc[i, 'label'] = 2
        elif (p_cluster3 >= p_cluster1) & (p_cluster3 >= p_cluster2):
            #dataFrame['label'][i] = 3
            dataFrame.loc[i, 'label'] = 3
        else:
            dataFrame.loc[i, 'label'] = np.random.choice(3, len(df)) + 1

    return dataFrame


# Maximization step - Given the parameters and the model, whther the parameter maximizes the likelihood of being
# sampled correctly from the gaussian distribution
# Alternatively this step finds the parameters that maximizes/suits the given setting
def maximization(dataFrame, parameters):
    points_assigned_to_cluster1 = dataFrame[dataFrame['label'] == 1]
    points_assigned_to_cluster2 = dataFrame[dataFrame['label'] == 2]
    points_assigned_to_cluster3 = dataFrame[dataFrame['label'] == 3]
    percent_assigned_to_cluster1 = len(points_assigned_to_cluster1) / float(len(dataFrame))
    percent_assigned_to_cluster2 = len(points_assigned_to_cluster2) / float(len(dataFrame))
    percent_assigned_to_cluster3 = 1 - percent_assigned_to_cluster1 - percent_assigned_to_cluster2
    parameters['lambda'] = [percent_assigned_to_cluster1, percent_assigned_to_cluster2, percent_assigned_to_cluster3]
    parameters['mu1'] = [points_assigned_to_cluster1['x'].mean(), points_assigned_to_cluster1['y'].mean(), None]
    parameters['mu2'] = [points_assigned_to_cluster2['x'].mean(), points_assigned_to_cluster2['y'].mean(), None]
    parameters['mu3'] = [points_assigned_to_cluster3['x'].mean(), points_assigned_to_cluster3['y'].mean(), None]
    parameters['sig1'] = [[points_assigned_to_cluster1['x'].std(), 0], [0, points_assigned_to_cluster1['y'].std()],
                          None]
    parameters['sig2'] = [[points_assigned_to_cluster2['x'].std(), 0], [0, points_assigned_to_cluster2['y'].std()],
                          None]
    parameters['sig3'] = [[points_assigned_to_cluster3['x'].std(), 0], [0, points_assigned_to_cluster3['y'].std()],
                          None]

    return parameters


# get the distance between points
# used for determining if params have converged or not
def distance(old_params, new_params):
    dist = 0
    for param in ['mu1', 'mu2', 'mu3']:
        for i in range(len(old_params)):
            dist += (old_params[param][i] - new_params[param][i]) ** 2
    return dist ** 0.5


# loop until parameters converges
shift = maxsize
epsilon = 0.01
iters = 0
df_copy = df.copy()

df_copy['label'] = map(lambda x: x + 1, np.random.choice(3, len(df)))
# randomly assign points to their initial clusters


params = pd.DataFrame.from_dict(guess, orient='index')
params = params.transpose()

# print params

while shift > epsilon:
    iters += 1
    # E-step
    updated_labels = expectation(df_copy.copy(), params)

    # M-step
    updated_parameters = maximization(updated_labels, params.copy())

    # see if our estimates of mu have changed
    # could incorporate all params, or overall log-likelihood
    shift = distance(params, updated_parameters)

    # Printing the mean shift output
    print("iteration_new {}, shift_new {}".format(iters, shift))

    # update labels and params for the next iteration
    df_copy = updated_labels
    params = updated_parameters
    print(params)

    fig = plt.figure()
    plt.scatter(df_copy['x'], df_copy['y'], 24, c=df_copy['label'])
    fig.savefig("iteration_new{}.png".format(iters))