"""
Gourav Verma
DSC550 - Data Mining
Summer-2020
Week-2 : Assignment- Charm Algorithm
"""

# Import Important libraries
from copy import copy
import pandas as pd
import time
import sys


# Class to do data preparation for Algorithm
class GetData:
    tran = []                             # Create an empty list
    tid_ct = 0                            # Initialize transaction id count

    def read_data(self, filename):
        """
        Read the input data into tran list
        """
        with open(filename, 'r') as file:
            tid = 1                       # Initialize transaction Id number
            for line in file:
                line = line.strip().split()
                for element in line:
                    self.tran.append({'tid': tid, 'item': element})
                tid += 1
        self.tid_ct = tid - 1

    def alter_data(self):
        """
        Convert list into DataFrame
        """
        df = pd.DataFrame(self.tran)
        self.itemsGrouped = df.groupby(['item'])['tid'].apply(list)   # Groupby elements
        self.itemsGrouped = pd.DataFrame({'item': self.itemsGrouped.index, 'tid': self.itemsGrouped.values})
        self.itemsGrouped['item'] = self.itemsGrouped['item'].apply(lambda x: {x})

    def get_frequent(self, minsup):
        """
        Filter the grouped items having support greater than or equal to minimum support
        """
        return self.itemsGrouped[self.itemsGrouped['tid'].map(len) >= minsup]


class CharmAlgorithm:
    def __init__(self, min_sup):
        """
        Initialize output DataFrame
        """
        self.result = pd.DataFrame(columns=['item', 'tid', 'support'])
        self.min_sup = min_sup

    @staticmethod
    def replace_values(df, column, find, replace):
        """
        Static function to replace old values
        """
        for row in df.itertuples():
            if find <= row[column]:
                row[column].update(replace)

    def charm_property(self, row1, row2, items, new_item, new_tid):
        """
        Apply CHARM Properties
        """
        if len(new_tid) >= self.min_sup:
            if set(row1[2]) == set(row2[2]):                     # Property-1: Check if sets of Tid is equal?
                items = items[items['item'] != row2[1]]          # Yes, remove row2[1] from items
                find = copy(row1[1])                             # replace all row1[1] with new_item
                self.replace_values(items, 1, find, new_item)
                self.replace_values(self.items_tmp, 1, find, new_item)
            elif set(row1[2]).issubset(set(row2[2])):            # Property-2: Check if 1st set of Tid is subset of 2nd
                find = copy(row1[1])                             # Yes, replace 1st set with 2nd set of Tid
                self.replace_values(items, 1, find, new_item)
                self.replace_values(self.items_tmp, 1, find, new_item)
            elif set(row2[2]).issubset(set(row1[2])):            # Property-2.1:Check if 2nd set of Tid is subset of 1st
                # items = items[items['item'] != row2[1]]          # Yes, remove 2nd set from items
                # add {item, tid} to self.items_tmp
                self.items_tmp = self.items_tmp.append({'item': new_item, 'tid': new_tid}, ignore_index=True)
            elif set(row1[2]) != set(row2[2]):                   # Property-3: Check if sets of Tid are not equal?
                # add {item, tid} to self.items_tmp
                self.items_tmp = self.items_tmp.append({'item': new_item, 'tid': new_tid}, ignore_index=True)

    def charm_apply(self, items_grouped):
        """
        CHARM Algorithm
        """
        # sort items by ascending support and reset index
        s = items_grouped.tid.str.len().sort_values().index
        items_grouped = items_grouped.reindex(s).reset_index(drop=True)

        for row1 in items_grouped.itertuples():      # Apply CHARM Property for each row
            self.items_tmp = pd.DataFrame(columns=['item', 'tid'])  # Temp DataFrame to iterate over the results
            for row2 in items_grouped.itertuples():  # 2nd loop to compare with all other rows
                if row2[0] >= row1[0]:
                    item = set()
                    item.update(row1[1])
                    item.update(row2[1])
                    tid = list(set(row1[2]) & set(row2[2]))
                    self.charm_property(row1, row2, items_grouped, item, tid)   # Apply CHARM properties
            if not self.items_tmp.empty:              # If temp DataFrame is not empty then reapply CHARM Properties
                self.charm_apply(self.items_tmp)
            # check if item subsumed
            is_subsumption = False
            for row in self.result.itertuples():
                if row1[1].issubset(row[1]) and set(row[2]) == set(row1[2]):
                    is_subsumption = True
                    break
            # append to result if element not subsumed
            if not is_subsumption:
                self.result = self.result.append({'item': row1[1], 'tid': row1[2], 'support': len(row1[2])},
                                                 ignore_index=True)
        return self.result


if __name__ == '__main__':
    start = time.time()

    # Check if the command line arguments are given
    try:
        print('Filename: ', sys.argv[1])
        print('Min Support: ', sys.argv[2])
    except:
        print('You need both a filename and a minimum support value!')

    filename = (sys.argv[1])
    support = int(sys.argv[2])

    # Data Preparation
    data = GetData()                            # Prepare data for algorithm
    data.read_data(filename)
    data.alter_data()                           # Modify data for algorithm
    freq = data.get_frequent(support)           # Get the items with required support

    # Apply Charm Algorithm
    algorithm = CharmAlgorithm(support)
    result = algorithm.charm_apply(freq)
    print(result)
