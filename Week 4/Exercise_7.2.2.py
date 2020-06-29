"""
Gourav Verma
DSC550 - Data Mining
Summer - 2020
Week-2 : Exercise- 7.2.2 : Hierarchical Clustering
Book - Mining of Massive Datasets
"""
"""
Exercise 7.2.2 : How would the clustering of Example 7.2 change if we used
for the distance between two clusters:
(a) The minimum of the distances between any two points, one from each
cluster.
(b) The average of the distances between pairs of points, one from each of the
two clusters.
"""

from sklearn.cluster import AgglomerativeClustering
import numpy as np
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram

pt = np.array([[2, 2], [3, 4], [5, 2], [4, 8], [4, 10], [6, 8], [7, 10], [9, 3], [10, 5], [12, 6], [11, 4], [12, 3]])

model = AgglomerativeClustering(affinity='euclidean', linkage='average')
model = model.fit(pt)


# Children of hierarchical clustering
children = model.children_

# Distances between each pair of children
# Since we don't have this information, we can use a uniform one for plotting
distance = np.arange(children.shape[0])

# The number of observations contained in each cluster level
no_of_observations = np.arange(2, children.shape[0]+2)

# Create linkage matrix and then plot the dendrogram
linkage_matrix = np.column_stack([children, distance, no_of_observations]).astype(float)

# Plot the corresponding dendrogram
dendrogram(linkage_matrix)
plt.show()



