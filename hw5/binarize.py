from tree import Tree as treelib
import sys


def main():
    for line in sys.stdin:
	tree = treelib.parse(line)
        
	binarize(tree)
        print(tree)


# Still has unit rules so not CNF?
def binarize(tree):
    if not tree.is_terminal():

        l_subtree = tree.subs[0]

        if len(tree.subs) > 2:
	    r_subtree = treelib(tree.label + "'", tree.span, None, tree.subs[1:])
	    tree.subs[1:] = []
	    tree.subs.append(r_subtree)

        if len(tree.subs) > 1: # prevent index oob on unary preterminals
            r_subtree = tree.subs[1]

            binarize(l_subtree)
            binarize(r_subtree)
	    


if __name__ == "__main__":
    main()
