import sys
from tree import Tree
import re

def main():
   pcfg, rpcfg = get_pcfg(open(sys.argv[1]))

   print(pcfg)

   sys.stdin.readline()
   parse(sys.stdin.readline(), pcfg, rpcfg)

   #for line in sys.stdin:
   #	parse(line, pcfg, rpcfg)


def parse(sentence, pcfg, rpcfg):
    words = sentence.rstrip("\n").split(" ")

    chart = [[{} for x in range(len(words))] for y in range(len(words))]

    back = [[{} for x in range(len(words))] for y in range(len(words))]


    #init lexicon
    for idx, word in enumerate(words):
	if word in rpcfg:
	    chart[idx][idx] = rpcfg[word]
	else:
	    chart[idx][idx] = rpcfg["<unk>"]  

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
			back[idx][idx][A] = None

		    if prob > chart[idx][idx][A]:
			chart[idx][idx][A] = prob
			back[idx][idx][A] = B
			added = True

    # CKY loop
    # start with (w,w) pairs, then ((w,w),w) and (w,(w,w)) pairs, etc
    for span in range(1, len(words)): 

	for begin in range(0, len(words) - span):

	    end = begin + span

	    for split in range(begin, end): # enumerate binary splits

		print(str(begin) + ", " + str(end))
		print(str(begin) + ", "+ str(split))
		print(str(split+1)+", "+str(end) )
		

		print(chart[begin][split])
		print(chart[split+1][end])

		for A in pcfg: # all A, B, C for A -> BC in grammar
		    for rule in pcfg[A]:
			if len(rule.split(" ")) > 1: # rule not a unary
			    B, C = rule.split(" ")
			    B_prob = 0 if B not in chart[begin][split] else chart[begin][split][B]
			    C_prob = 0 if C not in chart[split+1][end] else chart[split+1][end][C]
			
			    print("---------")
			    #print(B in chart[begin][split] and C in chart[split+1][end])

			    prob = B_prob * C_prob * pcfg[A][rule]
			    
			    if A not in chart[begin][end]:
				chart[begin][end][A] = 0
				back[begin][end][A] = None
			
			    if prob > chart[begin][end][A]:
				chart[begin][end][A] = prob
				
			    
			    #print(A + " -> " + B + " " + C)

	    #handle unaries:
	    added = True
	    while added:
		added = False
	
    print_chart(chart, words)
    #print_chart(back)


# for debugging
def print_chart(chart, words):
    print(words)
    for i in range(len(chart)):
	print(chart[i])
    

def get_pcfg(pcfg_file):
    start = pcfg_file.readline()

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

    return pcfg, reverse_pcfg


if __name__ == "__main__":
    main()
