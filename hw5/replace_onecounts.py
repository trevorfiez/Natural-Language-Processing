import sys
from tree import Tree as treelib


def main():

    word_counts = {}
    trees = []

    for line in sys.stdin:
	tree = treelib.parse(line)
	trees.append(tree)

        for word in get_words(tree):
	    if word not in word_counts:
	        word_counts[word] = 1
	    else:
	        word_counts[word] += 1

    for tree in trees:
	print(replace_onecount(tree, word_counts))


def get_words(tree, words=[]):

    if not tree.is_terminal():
	for sub in tree.subs:
	    get_words(sub, words)
    else:
        words.append(tree.word)
	return words

    return words


def replace_onecount(tree, word_counts):
    if not tree.is_terminal():
	for sub in tree.subs:
	    replace_onecount(sub, word_counts)
    else:
	if word_counts[tree.word] == 1:
	     tree.word = "<unk>"

    return tree

if __name__ == "__main__":
	main()
