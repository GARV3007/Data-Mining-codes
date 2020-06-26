"""
Gourav Verma
DSC550 - Data Mining
Summer-2020
Week-2 : Assignment- 3.2.1,
Book-Mining of Massive Datasets : Shingles
"""

# What are the first 10 3-shingles in the first sentence of section 3.2
# Given text
text = 'The most effective way to represent documents as sets, for the purpose of identifying lexically similar ' \
       'documents is to construct from the document the set of short strings that appear within it'

# set constant for 3-Shingles
k = 3

if __name__ == '__main__':
    print('Given text ==> ', text, '\n')               # Print given text
    tokens = text.replace(',', '').split()           # Split each word and remove comma
    print("First ten 3-shingles in text ==> " + str([tokens[x:x + k] for x in range(0, 10)]))  # Print 3-shingles
