""" This program creates the brute force algorithm
    for itemset mining. This algorithm is detailed
    on page 223 in Data Mining and Machine Learning
"""
import sys
import pandas as pd

def create_dict_from_file(filename):
    """ Read in a file of itemsets
        each row is considered the transaction id
        and each line contains the items associated
        with it.
        This function returns a dictionary that
        has a key set as the tid and has values
        of the list of items (strings)
    """
    f = open(filename, 'r')
    d = {}
    for tids, line_items in enumerate(f):
           d[tids] = [j for j in line_items.split(' ')
                           if j != '\n']
    return d
def create_database(itemset):
    "Uses dummy indexing to create the binary database"
    return pd.Series(itemset).str.join('|').str.get_dummies()
def compute_support(df, column):
    "Exploits the binary nature of the database"
    return df[column].sum()

if __name__ == '__main__':
    minsup=1000
    filename = 'mushroom.txt'
    dict_itemset = create_dict_from_file(filename)
    database = create_database(dict_itemset)
    print(database)

    # Executes the brute force algorithm
    # NOTE: a list comprehension is faster
    freq_items = []
    for col in database.columns:
        sup = compute_support(database, col)
        if sup >= minsup:
            freq_items.append(int(col))
        else:
            pass
    print('There are %d items with frequency' \
          ' greater than or equal to minsup.' % len(freq_items))
    print(sorted(freq_items))