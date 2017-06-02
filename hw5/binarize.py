from tree import Tree as treelib
import sys


# Still has unit rules so not CNF?
def binarize(tree):
    if not tree.is_terminal():

        l_subtree = tree.subs[0]

        if len(tree.subs) > 2:
	    r_subtree = treelib(tree.label + "'", tree.span, None, tree.subs[1:])
	    tree.subs[1:] = []
	    tree.subs.append(r_subtree)

        binarize(l_subtree)

        if len(tree.subs) > 1: # prevent index oob on unary preterminals/start token
            r_subtree = tree.subs[1]

            binarize(r_subtree)

    return tree
	  
  
def main():

    for line in sys.stdin:
	tree = treelib.parse(line)
        
	tree = binarize(tree)
        print(tree)


if __name__ == "__main__":
    main()
