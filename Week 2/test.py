import pandas as pd
import sys

# based on the given matrix in fig 3.6
element_list = [0, 1, 2, 3, 4, 5]
# variables for each set in matrix
set1 = (0, 0, 1, 0, 0, 1)
set2 = (1, 1, 0, 0, 0, 0)
set3 = (0, 0, 0, 1, 1, 0)
set4 = (1, 0, 1, 0, 1, 0)


# first hash formula as a function
def hash1(a):
    return ((2 * a) + 1) % 6


# secons hash formula as a function
def hash2(b):
    return ((3 * b) + 2) % 6


# third hash formula as a function
def hash3(c):
    return ((5 * c) + 2) % 6


# passing element list to first hash function
def hash_1(ele_list):
    # list variable to capture hash results
    hash_list = []
    # compute hash and add to hash list
    for i in ele_list:
        hash_list.append(((2 * i) + 1) % 6)
    return hash_list


# compile hash of element list using second hash function
def hash_2(ele_list):
    # list variable to capture hash results
    hash_list = []
    # compute hash and add to hash list
    for i in ele_list:
        hash_list.append(((3 * i) + 2) % 6)
    return hash_list


# compile hash of element list using third hash function
def hash_3(ele_list):
    # list variable to capture hash results
    hash_list = []
    # compute hash and add to hash list
    for i in ele_list:
        hash_list.append(((5 * i) + 2) % 6)
    return hash_list


# function to create matrix of elements, sets, and hash lists
def create_combined_matrix(hash_list_1, hash_list_2, hash_list_3):
    # dataframe to hold full matrix, with column headers
    hash_matrix = pd.DataFrame(columns=['element_list', 'set1', 'set2', 'set3', 'set4', 'hash1', 'hash2', 'hash3'])
    # loop through elements, construct full matrix
    for i in range(0, len(element_list)):
        hash_matrix.loc[i] = [element_list[i], set1[i], set2[i], set3[i], set4[i], hash_list_1[i], hash_list_2[i],
                              hash_list_3[i]]
    # list full matrix
    print('\nMatrix of Elements, Sets, Hash of Elements:\n' + str(hash_matrix))
    return hash_matrix


# function to determine true permutation of the elements list
def compare_hash_element_list(hash_list_name, hash_list):
    # sort the lists
    hash_list.sort()
    element_list.sort()
    # compare elements to determine and report on permutation
    if hash_list == element_list:
        print(hash_list_name + ' is a true permutation of elements list')
    else:
        print(hash_list_name + ' is not a true permutation of elements list')


# function to compute Jaccard Similarity of two lists
def jaccard_similarity(a, b):
    # determine intersection
    inter = intersection_cardinality(a, b)
    # determin union
    union = union_cardinality(a, b)
    # compute and return similiarty
    return round(float(inter) / union, 3)


# function to compute intersection of two lists
def intersection_cardinality(a, b):
    return len(list(set(a).intersection(b)))


# function to compute union of two lists
def union_cardinality(a, b):
    return (len(a) + len(b)) - intersection_cardinality(a, b)


# function to reverse columns and rows within the sets, filling a single ilst
def create_set_data():
    # variable to hold matrix
    hold_matrix = []
    # loop through the sets and create matrix of sets, placing column values in rows
    for i in range(0, len(set1)):
        hold_matrix.append([set1[i], set2[i], set3[i], set4[i]])
    print('\nRow Set Data: ' + str(hold_matrix))
    return hold_matrix


# function to create signature matrix
def minhash(data, hashfuncs):
    ''' pesudo-code for minhash
    for each row r do begin
        for each hash function hi do
            compute hi(r)   (do this only once...)
        for each column c
            if c has 1 in row r
                for each hash function hi do
                    if h1(r) is smaller than M(i,c) then
                        M(i,c) := hi(r)  (replace)
    '''
    # initialize each variables
    rows = len(data)
    print('rows', rows)
    cols = len(data[0])
    print('cols', cols)
    sigrows = len(hashfuncs)
    print(sigrows)
    # initialize signature matrix with maxsize
    sigmatrix = []
    for i in range(sigrows):
        sigmatrix.append([sys.maxsize] * cols)
    # loop throug rows
    for r in range(rows):
        hashvalue = list(map(lambda a: a(r), hashfuncs))
        # if data != 0 and signature > hash value, replace signature with hash value
        for c in range(cols):
            if data[r][c] == 0:
                continue
            for i in range(sigrows):
                # if the sigmatrix value is greater than the hashvalue, replace with hashvalue
                if sigmatrix[i][c] > hashvalue[i]:
                    sigmatrix[i][c] = hashvalue[i]
    return sigmatrix


# main function
def main():
    # try block for execution
    try:
        # printing four lists
        print('\n first Set 1: ' + str(set1))
        print('second Set 2: ' + str(set2))
        print('third Set 3: ' + str(set3))
        print('fourth Set 4: ' + str(set4))

        # passing element list as parameter to calculat hash list based on hash functions
        hash_list_1 = hash_1(element_list)
        hash_list_2 = hash_2(element_list)
        hash_list_3 = hash_3(element_list)
        # printing each values
        print('\nFirst hash list: ' + str(hash_list_1))
        print('Second hash list: ' + str(hash_list_2))
        print('Third hash list: ' + str(hash_list_3))

        # generate full matrix of elements, sets, and hash of elements
        create_combined_matrix(hash_list_1, hash_list_2, hash_list_3)

        # generating  minhash signature for given functions
        # first question
        print('\n(1) Compute the minhash signature for each column using three hash functions.')
        minhash_sig = minhash(create_set_data(), [hash1, hash2, hash3])
        print('\nFinal Minhash Signature: ' + str(minhash_sig))

        # secons questions
        print('\n(2) Which of these hash functions are true permutations?')
        compare_hash_element_list('\nHash 1', hash_list_1)
        compare_hash_element_list('Hash 2', hash_list_2)
        compare_hash_element_list('Hash 3', hash_list_3)

        # comparing estimated Jaccard similarities
        # Third questions
        print('\n(3) How close are the estimated Jaccard Similarities to the true Jaccard Similarities?')
        # similarities of 6 pairs of columns

        print('\nColumn 1 and Column 2: ' + str(intersection_cardinality(set1, set2)) + ' / ' + str(
            union_cardinality(set1, set2)) + str(' or ' + str(jaccard_similarity(set1, set2))))
        print('Column 1 and Column 3: ' + str(intersection_cardinality(set1, set3)) + ' / ' + str(
            union_cardinality(set1, set3)) + str(' or ' + str(jaccard_similarity(set1, set3))))
        print('Column 1 and Column 4: ' + str(intersection_cardinality(set1, set4)) + ' / ' + str(
            union_cardinality(set1, set4)) + str(' or ' + str(jaccard_similarity(set1, set4))))
        print('Column 2 and Column 3: ' + str(intersection_cardinality(set2, set3)) + ' / ' + str(
            union_cardinality(set2, set3)) + str(' or ' + str(jaccard_similarity(set2, set3))))
        print('Column 2 and Column 4: ' + str(intersection_cardinality(set2, set4)) + ' / ' + str(
            union_cardinality(set2, set4)) + str(' or ' + str(jaccard_similarity(set2, set4))))
        print('Column 3 and Column 4: ' + str(intersection_cardinality(set3, set4)) + ' / ' + str(
            union_cardinality(set3, set4)) + str(' or ' + str(jaccard_similarity(set3, set4))))

        # similarities of signatures
        # establish columns of signatures
        minhash_1 = [minhash_sig[0][0], minhash_sig[1][0], minhash_sig[2][0]]
        minhash_2 = [minhash_sig[0][1], minhash_sig[1][1], minhash_sig[2][1]]
        minhash_3 = [minhash_sig[0][2], minhash_sig[1][2], minhash_sig[2][2]]
        minhash_4 = [minhash_sig[0][3], minhash_sig[1][3], minhash_sig[2][3]]

        print(minhash_1)
        print(minhash_2)
        print(minhash_3)
        print(minhash_4)

        # similarities of signatures 1 & 2, 1 & 3, 1 & 4, 2 & 3, 2 & 4, 3 & 4
        print('\nSig 1 and Sig 2: ' + str(intersection_cardinality(minhash_1, minhash_2)) + ' / ' + str(
            union_cardinality(minhash_1, minhash_2)) + str(' or ' + str(jaccard_similarity(minhash_1, minhash_2))))
        print('Sig 1 and Sig 3: ' + str(intersection_cardinality(minhash_1, minhash_3)) + ' / ' + str(
            union_cardinality(minhash_1, minhash_3)) + str(' or ' + str(jaccard_similarity(minhash_1, minhash_3))))
        print('Sig 1 and Sig 4: ' + str(intersection_cardinality(minhash_1, minhash_4)) + ' / ' + str(
            union_cardinality(minhash_1, minhash_4)) + str(' or ' + str(jaccard_similarity(minhash_1, minhash_4))))
        print('Sig 2 and Sig 3: ' + str(intersection_cardinality(minhash_2, minhash_3)) + ' / ' + str(
            union_cardinality(minhash_2, minhash_3)) + str(' or ' + str(jaccard_similarity(minhash_2, minhash_3))))
        print('Sig 2 and Sig 4: ' + str(intersection_cardinality(minhash_2, minhash_4)) + ' / ' + str(
            union_cardinality(minhash_2, minhash_4)) + str(' or ' + str(jaccard_similarity(minhash_2, minhash_4))))
        print('Sig 3 and Sig 4: ' + str(intersection_cardinality(minhash_3, minhash_4)) + ' / ' + str(
            union_cardinality(minhash_3, minhash_4)) + str(' or ' + str(jaccard_similarity(minhash_3, minhash_4))))

        # summary of comparision of Jaccard Similarities of columns and signatures
        print('\nThe estimated Jaccard similarities are not close to the true Jaccard similarities.')

    # exception block to catch any exceptions during execution
    except Exception as exception:
        print('exception')

        # list name of exception and any arguments
        print('An exception of type {0} occurred.  Arguments:\n{1!r}'.format(type(exception).__name__, exception.args));


if __name__ == '__main__':
    main()