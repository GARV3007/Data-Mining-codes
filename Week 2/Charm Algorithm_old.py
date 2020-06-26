

import sys
import pandas as pd
from itertools import combinations
from operator import itemgetter

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

if __name__ == '__main__':
    minsup=1000                                                        # Define minimum support
    filename = 'mushroom.txt'
    dict_itemset = create_dict_from_file(filename)                     # Create dictionary from the file
    df_itemset = pd.DataFrame.from_dict(dict_itemset, orient='index')  # Create pandas dataframe from dict

    # Calculate the frequency of each individual number in whole file
    single_items = df_itemset.apply(pd.value_counts).sum(axis=1).where(lambda value: value > minsup).dropna()

    # Create Dataframe for each item having frequency greater than minimum support
    apriori_data = pd.DataFrame({'items': single_items.index.astype(int),
         'support_count': single_items.values,
         'set_size': 1})
    # print(apriori_data)

    # Create a single set of all items whose support is greater than or equal to support level.
    single_items_set = set(single_items.index.astype(int))
    print('\nThere are %d items in the set whose support is greater than minsup' %  len(single_items_set))
    df_itemset['set_size'] = df_itemset.count(axis='columns')
    # df_itemset = df_itemset.apply(lambda row: set(map(int)))
    # print(df_itemset.head())

    for length in range(2, len(single_items_set) + 1):
        df_itemset = df_itemset[df_itemset['set_size'] >= length]
        d = df_itemset\
            .apply(lambda st: pd.Series(s if set(s).issubset(st) else None
                                        for s in combinations(single_items_set, length))) \
            .apply(lambda col: [col.dropna().unique()[0], col.count()] if
        col.count() >= minsup else None).dropna()

        if d.empty:
            break
        print('here')
        apriori_data = apriori_data.append(pd.DataFrame(
            {'items': list(map(itemgetter(0), d.values)),
             'support_count': list(map(itemgetter(1), d.values)),
             'set_size': length}), ignore_index=True)

    print(apriori_data)