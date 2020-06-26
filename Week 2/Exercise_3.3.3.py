"""
Gourav Verma
DSC550 - Data Mining
Summer-2020
Week-2 : Assignment- 3.3.3
Book-Mining of Massive Datasets : Minhash Signature
"""

# Import important libraries
import pandas as pd
import sys

def initialize():
    # Given hash matrix
    h_dict = {'Element': [0, 1, 2, 3, 4, 5], 'S1': [0, 0, 1, 0, 0, 1], 'S2': [1, 1, 0, 0, 0, 0], 'S3': [0, 0, 0, 1, 1, 0],
          'S4': [1, 0, 1, 0, 1, 0]}
    matrix = pd.DataFrame(data=h_dict)     # Convert to DataFrame
    return matrix


def cal_hash(h_matrix):
    """
    Function to calculate 3 hash functions for all columns
    """
    rows = list(h_matrix['Element'])  # Convert values of Element column to a list
    h_matrix1 = h_matrix              # Copy initial matrix

    for r in h_matrix.itertuples():   # Iterate over all Elements
        i = r.Element
        h_matrix1.loc[r.Index, 'h1'] = ((2 * i) + 1) % 6      # Hash Function 1
        h_matrix1.loc[r.Index, 'h2'] = ((3 * i) + 2) % 6      # Hash Function 2
        h_matrix1.loc[r.Index, 'h3'] = ((5 * i) + 2) % 6      # Hash Function 3

    # Convert output hash values to Int type
    h_matrix1["h1"] = h_matrix1["h1"].astype(int)
    h_matrix1["h2"] = h_matrix1["h2"].astype(int)
    h_matrix1["h3"] = h_matrix1["h3"].astype(int)

    return h_matrix1


def cal_hashsign(df):
    """
    Function to calculate Hash Signatures
    """
    signmatrix = []
    for i in range(3):                               # 3x4 List of lists for storing Hash Signatures
        signmatrix.append([sys.maxsize] * 4)         # Set each elements of signature matrix with high value

    h_list = []
    h_list = df[['h1', 'h2', 'h3']].values.tolist()  # 6x3 List of lists for Hash Functions

    # Logic to calculate hash Signature
    for i, row in df.iterrows():                     # Iterate over rows of hash Matrix
        col_count = 0
        for col in df.columns[1:5]:                  # Iterate over columns S1, S2, S3, and S4
            col_count += 1
            if row[col] == 0:                        # If row-col has value '0' do nothing
                continue
            for s in range(3):                       # Iterate 3 times for 3 hash functions
                if signmatrix[s][col_count-1] > h_list[i][s]:   # Check if sign matrix value is greater than hash value
                    signmatrix[s][col_count-1] = h_list[i][s]   # Yes, replace signature value with hash value

    # Convert Hash signature matrix into DataFrame
    signmatrix_df = pd.DataFrame(signmatrix, columns=['S1', 'S2', 'S3', 'S4'], index=['h1', 'h2', 'h3'])

    return signmatrix_df


def hash_perm(h_matrix):
    """
    Function to check the true permutations
    """
    # Create lists
    Element_l = sorted(h_matrix['Element'].tolist())
    h1_l = sorted(h_matrix['h1'].tolist())
    h2_l = sorted(h_matrix['h2'].tolist())
    h3_l = sorted(h_matrix['h3'].tolist())

    # Compare each hast function list with Element list to check for true permutations.
    if Element_l == h1_l:
        print('\n==> Hash Function 1 is true permutations of Element list.', '\n')
    elif Element_l == h2_l:
        print('\n==> Hash Function 2 is true permutations of Element list.', '\n')
    elif Element_l == h3_l:
        print('\n==> Hash Function 3 is true permutations of Element list.', '\n')
    return


def jaccard(a, b):
    """
    Function to compute Jaccard similarity between 2 sets
    """
    intr = len(list(set(a).intersection(b)))             # Compute Intersection
    uni = (len(a) + len(b)) - intr                       # Compute Union
    return intr/uni


def comp_jaccard(h_matrix, h_sign):
    """
    Function to compare Jaccard similarities between 6 pairs of columns
    """
    TruJ = []        # Initialize list for True Jaccard similarities
    EstJ = []        # Initialize list for Estimate Jaccard similarities

    # Compute True Jaccard similarities between column pairs
    TruJ.append(jaccard(h_matrix['S1'], h_matrix['S2']))
    TruJ.append(jaccard(h_matrix['S1'], h_matrix['S3']))
    TruJ.append(jaccard(h_matrix['S1'], h_matrix['S4']))
    TruJ.append(jaccard(h_matrix['S2'], h_matrix['S3']))
    TruJ.append(jaccard(h_matrix['S2'], h_matrix['S4']))
    TruJ.append(jaccard(h_matrix['S3'], h_matrix['S4']))

    # Compute Estimate Jaccard similarities between column pairs
    EstJ.append(jaccard(h_sign['S1'], h_sign['S2']))
    EstJ.append(jaccard(h_sign['S1'], h_sign['S3']))
    EstJ.append(jaccard(h_sign['S1'], h_sign['S4']))
    EstJ.append(jaccard(h_sign['S2'], h_sign['S3']))
    EstJ.append(jaccard(h_sign['S2'], h_sign['S4']))
    EstJ.append(jaccard(h_sign['S3'], h_sign['S4']))

    J_dict = {'TruJ': TruJ, 'EstJ': EstJ}     # Add lists to dictionary
    J_matrix = pd.DataFrame(J_dict, index=['S1-S2', 'S1-S3', 'S1-S4', 'S2-S3', 'S2-S4', 'S3-S4'])  # Convert to DF

    print('Comparision of Jaccard Similarities:\nTruJ- True Jaccard Similarity | EstJ- Estimate Jaccard Similarity\n',
          J_matrix)
    if TruJ == EstJ:
        print('\n==> The Estimated Jaccard similarity is close to True Jaccard similarity')
    else:
        print('\n==> The Estimated Jaccard similarity is NOT close to True Jaccard similarity')

    return

if __name__ == '__main__':

    matrix = initialize()
    print('Given Matrix - \n', matrix, '\n')

    """
    Calculate the minhash signature for each column if we use 3 hash functions
    h1(x) = 2x+1 mod 6; h2(x) = 3x+2 mod 6; h3(x) = 5x+2 mod 6
    """
    h_matrix = cal_hash(matrix)
    print('Matrix with hash function values -\n', h_matrix, '\n')
    h_sign = cal_hashsign(h_matrix)
    print('==> Minhash Signature Matrix -\n', h_sign)

    """
    Which of these hash functions are true permutations?
    """
    hash_perm(h_matrix)

    """
    How close are the estimated Jaccard similarities for the six pairs of columns to the true Jaccard similarities?
    """
    comp_jaccard(h_matrix, h_sign)



