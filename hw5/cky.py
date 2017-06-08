import sys
from tree import Tree
import re


from binarize import binarize

def main():
#   pcfg, rpcfg, START = get_pcfg(open(sys.argv[1]))
#   print(parse("I need a flight from Atlanta to Charlotte North Carolina next Monday", pcfg, rpcfg, START))
 

   for line in sys.stdin:
        pcfg, rpcfg, START = get_pcfg(open(sys.argv[1]))
   	print(parse(line, pcfg, rpcfg, START))


def parse(sentence, pcfg, rpcfg, START):
    words = sentence.rstrip("\n").split(" ")
    #print(words)

    chart = [[{} for x in range(len(words))] for y in range(len(words))] # cky table
    back = [[{} for x in range(len(words))] for y in range(len(words))] # backpointer table

    #init lexicon
    for idx, word in enumerate(words):
	if word in rpcfg:
	    chart[idx][idx] = rpcfg[word]
            back[idx][idx] = {rpcfg[word].keys()[0]: word}
	else:
	    chart[idx][idx] = rpcfg["<unk>"]  
	    back[idx][idx] = {key: "<unk>" for key, value in rpcfg["<unk>"].items()}

	#handle lexical unaries:
	added = True
	while added == True:

	    added = False
	    labels = [x for x in chart[idx][idx]]
	    for B in labels:

	        if B in rpcfg: #A -> B in grammar
		    A = rpcfg[B].keys()[0]

		    prob = rpcfg[B][A] * chart[idx][idx][B] # P(A->B)*P(B->w)

		    #print(B+"->"+words[idx]+" # " + str(chart[idx][idx][B]))
		    #print(A + "->" + B + " # " + str(rpcfg[B][A]))
		    #print(str(prob) + "\n")

		    if A not in chart[idx][idx]:
		        chart[idx][idx][A] = 0

		    if prob > chart[idx][idx][A]:
			chart[idx][idx][A] = prob
			back[idx][idx][A] = ((idx, idx, B),) 
			added = True

    # CKY loop
    # START with (w,w) pairs, then ((w,w),w) and (w,(w,w)) pairs, etc
    for span in range(1, len(words)): 

	for begin in range(0, len(words) - span):

	    end = begin + span

	    for split in range(begin, end): # enumerate binary splits

		#print(str(begin) + ", " + str(end))
		#print(str(begin) + ", "+ str(split))
		#print(str(split+1)+", "+str(end) )
		
		#print(chart[begin][split])
		#print(chart[split+1][end])

		for A in pcfg: # all A, B, C for A -> BC in grammar
		    for rule in pcfg[A]:
			if len(rule.split(" ")) > 1: # rule is NOT unary
			    B, C = rule.split(" ")

			    B_prob = 0 if B not in chart[begin][split] else chart[begin][split][B]
			    C_prob = 0 if C not in chart[split+1][end] else chart[split+1][end][C]
			
			    #print("---------")
			    #print(B in chart[begin][split] and C in chart[split+1][end])

			    prob = B_prob * C_prob * pcfg[A][rule]
			    
			    if A not in chart[begin][end]:
				chart[begin][end][A] = 0
			
			    if prob > chart[begin][end][A]:
				chart[begin][end][A] = prob
				back[begin][end][A] = ((begin, split, B), (split+1, end, C))
				
			    #print(A + " -> " + B + " " + C)

	    # handle unaries:
	    added = True
	    while added:
		added = False
		for A in pcfg: # enumerate all A, B for A -> B in grammar
		    for rule in pcfg[A]:
		        if len(rule.split(" ")) == 1: # rule IS unary
		  	    B, = rule.split()

		            prob = pcfg[A][rule] * 0 if B not in chart[begin][end] else chart[begin][end][B]
			    
 			    if A not in chart[begin][end]:
				chart[begin][end][A] = 0
			    
			    if prob > chart[begin][end][A]:
			        chart[begin][end][A] = prob
				back[begin][end][A] = ((begin, end, B),)
			        added = True
			    
    #print(chart)
    #print_chart(chart, words)
    #print(" ")
    #print_chart(back, words)

    #print("-----------")
    #print(back[0][0])
    #print("------------")
    #print(back[8][8])

    tree = build_tree(chart, back, words, START)


    if tree == None: # failed to parse
	return "NONE"
    else:
	return tree


# for debugging
def print_chart(chart, words):
    for row in remove_zero_probs(chart):
        print(row)


def remove_zero_probs(chart):
   return [[{key: value for key, value in d.items() if value != 0} for d in row] for row in chart]
    

def build_tree(chart, bp, words, START):
    chart = remove_zero_probs(chart)
    bp = remove_zero_probs(bp)

    if START not in bp[0][-1]:
        print("weird failure")
        return None

    else:
        tree = Tree(START, (0, 0), None, [])

        try:
            dfs_tree(words, tree, bp, 0, -1, START)
	except KeyError:
	    return None

        return debinarize(tree)
    

def dfs_tree(words, tree, bp, i, j, label):
   p = bp[i][j][label]

   #print(p)

   if type(p) == str:
        if p != "<unk>":
	    tree.word = p
	else:
	    tree.word = words[i]

   elif len(p) == 1:
	i, j, label = p[0]
        tree.subs = [Tree(label, (0,0), None, [])]
	dfs_tree(words, tree.subs[0], bp, i, j, label)

   else:
	(l_i, l_j, l_label), (r_i, r_j, r_label) = p
        
        tree.subs = [Tree(l_label, (0,0), None, []), Tree(r_label, (0,0), None, [])]

	dfs_tree(words, tree.subs[0], bp, l_i, l_j, l_label)
	dfs_tree(words, tree.subs[1], bp, r_i, r_j, r_label)


def get_pcfg(pcfg_file):
    START = pcfg_file.readline().rstrip("\n")

    pcfg = {}
    reverse_pcfg = {} ###

    for line in pcfg_file:
	from_label = re.search('(.*) ->', line).group(1)
	to_label = re.search('-> (.*) #', line).group(1)
	prob = re.search('# (.*)', line).group(1)
	
	if from_label not in pcfg:
	    pcfg[from_label] = {}
	
	pcfg[from_label][to_label] = float(prob)

	if to_label not in reverse_pcfg: ###
	    reverse_pcfg[to_label] = {}  ###

	reverse_pcfg[to_label][from_label] = float(prob) ###

    return pcfg, reverse_pcfg, START


def debinarize(tree):
    if not tree.is_terminal():

        if tree.subs[-1].label[-1] == "'":
	    tmp = tree.subs[-1].subs

	    del tree.subs[-1] 
	    for sub in tmp:
	        tree.subs.append(sub)

            debinarize(tree)
    
	for sub in tree.subs:
	    debinarize(sub)

    return tree


if __name__ == "__main__":
    main()
