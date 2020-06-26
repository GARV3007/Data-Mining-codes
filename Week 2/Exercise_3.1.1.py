"""
Gourav Verma
DSC550 - Data Mining
Summer-2020
Week-2 : Assignment- 3.1.1,
Book-Mining of Massive Datasets : Jaccard Similarities
"""

# 3 given sets
set1 = {1, 2, 3, 4}
set2 = {2, 3, 5, 7}
set3 = {2, 4, 6}


def jaccard(s1, s2):
    """
    Function to calculate Jaccard Similarity between 2 sets
    """
    return len(s1.intersection(s2))/len(s1.union(s2))


if __name__ == '__main__':
    print(' set1 = ', set1, '\n', 'set2 = ', set2, '\n', 'set3 = ', set3, '\n')

    print('Jaccard Similarity between set1 & set2 - ', round(jaccard(set1, set2), 2))
    print('Jaccard Similarity between set1 & set3 - ', round(jaccard(set1, set3), 2))
    print('Jaccard Similarity between set2 & set3 - ', round(jaccard(set2, set3), 2))