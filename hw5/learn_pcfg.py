from tree import Tree as treelib
import sys


def print_pcfg(pcfg):
    print("TOP")
    for from_label in pcfg:
	for to_label in pcfg[from_label]:
	    print("%s -> %s # %.4f" % (from_label, to_label, pcfg[from_label][to_label]))


def normalize_pcfg(pcfg, label_counts):
    for from_label in pcfg:
	for to_label in pcfg[from_label]:
	    pcfg[from_label][to_label] /= float(label_counts[from_label])

    
def update_counts(tree, label_counts, pcfg):

    if tree.label not in label_counts:
        label_counts[tree.label] = 1
    else: 
	label_counts[tree.label] += 1

    if tree.label not in pcfg:
	pcfg[tree.label] = {}

    if not tree.is_terminal():
	to_label = tree.subs[0].label
	if len(tree.subs) > 1:
		to_label += " " + tree.subs[1].label

	if to_label not in pcfg[tree.label]:
	    pcfg[tree.label][to_label] = 1
	else:
	    pcfg[tree.label][to_label] += 1

	update_counts(tree.subs[0], label_counts, pcfg)

        if len(tree.subs) > 1:
            update_counts(tree.subs[1], label_counts, pcfg)

    else:
	if tree.word not in pcfg[tree.label]:
	    pcfg[tree.label][tree.word] = 1
	else:
	    pcfg[tree.label][tree.word] += 1


def main():

    label_counts = {}
    pcfg = {}
    
    for line in sys.stdin:
	tree = treelib.parse(line)

        update_counts(tree, label_counts, pcfg)

    normalize_pcfg(pcfg, label_counts)

    print_pcfg(pcfg)

        
if __name__ == "__main__":
    main()
