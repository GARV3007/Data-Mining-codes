"""
Gourav Verma
DSC550 - Data Mining
Summer-2020
Week-2 : Assignment- NonDerivable Itemset
"""

# Import important libraries
import pandas as pd
from itertools import chain, combinations


class DataPreparation:
    def __init__(self):
        self.itemset = []
        self.lists = []
        # self.st = set()
        self.itemset_df = pd.DataFrame(columns=['sets', 'support'])
        self.list_df = pd.DataFrame(columns=['sets'])

    def read_txt1(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                line = line.rstrip('\n').split(' - ')
                self.itemset.append({'sets': line[0], 'support': line[1]})
        itemset_df = pd.DataFrame(self.itemset)
        itemset_df['sets'] = itemset_df['sets'].apply(lambda x: set(x))
        return itemset_df

    def read_txt2(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                self.st = set()
                line = line.rstrip('\n').split(' ')
                for element in line:
                    self.st.add(int(element))
                self.lists.append({'sets': self.st})
        list_df = pd.DataFrame(self.lists)
        return list_df


class CheckNonDerivable:

    @staticmethod
    def powerset(s):
        l = list(s)
        return chain.from_iterable(combinations(l, r) for r in range(len(l) + 1))

    def get_support(self, file1, sst):
        for row in file1.itertuples():
            rw = row[0]
            #if sst == row[0]:
            #    return row[1]
            #else:
            #    continue
               #    return sst # row['support']

        return type(row[0])

    def cal_bound(self, main_set, subs, file1):
        """
        :param main_set: Primary set from ndi.txt
        :param subs:  Subset of primary set
        :param pwr_set: List of all subsets of primary set
        :param file1: itemsets txt file for support
        :return:
        """
        bound = 0
        supp_st = 0
        pwr_set1 = self.powerset(main_set)
        for st in pwr_set1:
            sst = set(st)
            #print(sst)
            if subs.issubset(sst) and len(sst) < len(main_set):
                coef = pow(-1, ((len(main_set) - len(st)) + 1))
                get = self.get_support(file1, sst)
                supp_st += 10
                #supp_st += coef * 10
                # print(coef, subs)
                print(get)
        return supp_st

    def applyprinciple(self, file1, file2):
        for index, row in file2.iterrows():
            main_set = row['sets']
            pwr_set = self.powerset(main_set)
            for sub in pwr_set:
                subs = set(sub)
                len_diff = len(main_set) - len(subs)
                #sup_st = file1['support'][if (file1['sets'] < subs): False;].values
                #print(sup_st)
                # print(len(main_set), len(subs), len(main_set) - len(subs), subs)
                if len(subs) == 0:
                    continue
                if len_diff == 0:
                    continue
                elif (len_diff % 2) == 0:    # Even?
                    # Lower Bound
                    lbound = self.cal_bound(main_set, subs, file1)
                    print('L', lbound)
                else:                        # Odd
                    # Upper Bound
                    ubound = self.cal_bound(main_set, subs, file1)
                    print('U', ubound)
        return

if __name__ == '__main__':

    file1 = 'itemsets.txt'
    file2 = 'ndi.txt'

    data = DataPreparation()
    itemset_df = data.read_txt1(file1)
    list_df = data.read_txt2(file2)
    print(list_df)
    print(itemset_df.head())

    NonDer = CheckNonDerivable()
    Result = NonDer.applyprinciple(itemset_df, list_df)

