
# Import important libraries
from sklearn import tree
import pandas as pd
import graphviz
import traceback


def des_tree(n):
    # Load in our dataset
    df = pd.read_csv('caesarian.csv')
    mtx = df[df.columns[1:5]].to_numpy()
    cae = df[df.columns[5]].to_numpy()

    # Initialize our decision tree object
    classification_tree = tree.DecisionTreeClassifier(max_depth=n)
    classification_tree = classification_tree.fit(mtx, cae)

    # Plot the tree
    dot_data = tree.export_graphviz(classification_tree, out_file=None,
                                    feature_names=df.columns[1:5],
                                    class_names=['apt', 'inept'],
                                    filled=True, rounded=True,
                                    special_characters=True)
    graph = graphviz.Source(dot_data)
    filename = "Tree_Max_D_%s" % n
    graph.render(filename, view=True)

    return


if __name__ == '__main__':
    try:
        des_tree(2)  # Create Decision tree for depth 2
        des_tree(4)  # Create decision tree for depth 4
    except Exception as exception:
        print('exception')
        traceback.print_exc()
        print('\nAn exception of type {0} occurred. Arguments:\n{1!r}'.format(type(exception).__name__, exception.args))
    finally:
        print("\nfinally block is executed whether exception is handled or not!!")
