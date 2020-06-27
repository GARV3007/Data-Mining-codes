# Name:Pritam Shrestha
# FileName:Non_derivable_itemsets
# Date:06/17/2020
# Course: DSC550-Data Mining
# Professor/Instructor:Brant Abeln
# Description:Non Derivable Itemsest
# Due Date:06/21/20
# Assignment No:2


# In[17]:


import pandas as pd
from itertools import combinations
import traceback                                                      # GV change for traceback.print_exc()


# creating function to pass arguments
def calculate_combinations(itemset, num_combinations):
    # creating list
    list_of_combination = []
    # loop through itemset
    for comb in combinations(itemset, num_combinations):
        # appending in empty list
        list_of_combination.append(comb)
    return list_of_combination


# function to calculate the bound value
def calc_value(st, itemset, dictionary, n):
    # build subsets based on combinations
    value = 0.0
    for num in range(n - 1, 0, -1):
        # build list of combinations
        subsets = calculate_combinations(itemset, num)
        # looping through combinations list
        for comb in subsets:
            # get all items in combination based on items in itemset
            ck = all(item in comb for item in st)
            # increment value by i
            if ck or st == ():
                i = int(dictionary[comb]) * pow(-1.0, (n + 1) - num)
                value += i
    # if combination set is empty, update dictionary values
    if st == ():
        empty = 0
        for dict_value in dictionary.values():
            empty += int(dict_value)
        value += empty * pow(-1.0, (n + 1))

    # returning value
    return value


# function to obtain upper and lower bounds
def evaluate_bounds(itemset, dictionary):
    # set variables to obtain and determin upper and lower bound per itemset
    upper_bounds = []
    lower_bounds = []
    lower_bound = 0
    upper_bound = 0
    n = len(itemset)

    # loop through itemset and break down the combinations into subsets
    for index in range(len(itemset)):
        subsets = calculate_combinations(itemset, index)
        # checking odd or even
        boolean_Odd = (n - len(subsets[0])) % 2
        for comb in subsets:
            # if the length is odd, update upper bound list
            if boolean_Odd:
                upper_bounds.append(calc_value(comb, itemset, dictionary, n))
            # if length is even, update lower bound list
            else:
                lower_bounds.append(calc_value(comb, itemset, dictionary, n))

    # if the maximum number in the lower bound list is less than zero, set lower bound to zero
    if max(lower_bounds) < 0:
        lower_bound = 0
    # if maxium number is 0 or greater, set lower bound to that number
    else:
        lower_bound = max(lower_bounds)

    # set upper bound to the minumum number within the upper bound list
    upper_bound = min(upper_bounds)

    # applying condition for upper and lower bound
    if lower_bound == upper_bound:
        bound = 'This Itemset is derivable'
    else:
        bound = 'This Itemset is non-derivable'

    # returning valuse using format function
    return '{}: [{}, {}] {}'.format(itemset, lower_bound, upper_bound, bound)


# main function for exercise three
def main():
    # reading data as dataframe
    itemset_df = pd.read_csv('itemsets.txt', header=None)
    ndi_df = pd.read_csv('ndi.txt', header=None)

    # converting itemsets to dictionary
    itemset_dict = {}
    for i, itemset_support in enumerate(itemset_df[0]):
        set_support_list = []
        # splitting
        for val in itemset_support.split(' '):
            # passing hypen condition
            if val == '-':
                continue
            else:
                set_support_list.append(val)
        itemset_dict[tuple(set_support_list[:-1])] = set_support_list[-1]
        # processing ndi datasets
    ndi_dict = {}
    # iterating over ndi
    for i, itemset in enumerate(ndi_df[0]):
        ndi_dict[i] = itemset.split(' ')
    for itemset in ndi_dict.values():
        # printing values
        print(evaluate_bounds(itemset, itemset_dict))


if __name__ == '__main__':
    # calling function inside try blck to catch the eror
    try:
        main()
    except Exception as exception:
        print('exception')
        traceback.print_exc()
        print('An exception of type {0} occurred.  Arguments:\n{1!r}'.format(type(exception).__name__, exception.args));
    finally:
        print("finally block is executed whether exception is handled or not!!")