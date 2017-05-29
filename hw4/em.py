from __future__ import print_function
import sys
from collections import defaultdict


def generate_pairs(ek_raw):
    ek_lines = ek_raw.split("\n")

    ek_pairs = []
    for i in range(0, len(ek_lines), 2):
        e_pron = ek_lines[i].split()
        letters = ek_lines[i + 1].split()

        if (len(e_pron) == 0):
            continue

        ek_pairs.append((e_pron, letters))

    return ek_pairs

def generate_legal_alignments(prons, kata):
    if (len(prons) == 1):
        return [[(prons[0], " ".join(kata))]]

    possible = []
    for i in range(min(3, len(kata) - len(prons) + 1)):
        my_kata = " ".join(kata[:i + 1])

        rest_pos = generate_legal_alignments(prons[1:], kata[i + 1:])
        possible = possible + [[(prons[0], my_kata)] + r for r in rest_pos]

    return possible

def normalize_ek_prob(ek_prob):
    for pron in ek_prob.keys():
        counts = 0.0
        for kata in ek_prob[pron].keys():
            counts += ek_prob[pron][kata]

        for kata in ek_prob[pron].keys():
            ek_prob[pron][kata] = ek_prob[pron][kata] / counts



def initialize_ek_prob(ek_prob, ek_pairs):

    for ek in ek_pairs:
        la = generate_legal_alignments(ek[0], ek[1])

        for a in la:
            for pair in a:
                ek_prob[pair[0]][pair[1]] += 1

    normalize_ek_prob(ek_prob)

def print_ek_probs(ek_probs):
    
    for pron in ek_probs.keys():
        line = "%s|->" % (pron)

        kata = ["\t%s: %.2f" % (k, ek_probs[pron][k])  for k in ek_probs[pron].keys() if (ek_probs[pron][k] >= 0.01)]

        line += "".join(kata)

        print(line, file=sys.stderr)


def print_probs(ek_probs):
    for pron in ek_probs.keys():
        for kata in ek_probs[pron].keys():
            prob = ek_probs[pron][kata]
            if prob >= 0.01:
            	print("{0} : {1} # {2}".format(pron, kata, prob))


def count_non_zero(ek_probs):
    nonzero = 0
    for pron in ek_probs.keys():
        for kata in ek_probs[pron].keys():
            if (ek_probs[pron][kata] >= 0.01):
                nonzero += 1

    return nonzero

'''
def fb_em()
    ek_raw = get_ek_from_data()

    ek_pairs = generate_pairs(ek_raw)
    
    ek_prob = defaultdict(lambda: defaultdict(float))

    initialize_ek_prob(ek_prob, ek_pairs)

    print_ek_probs(ek_prob)
'''

def viterbi_decode(ek_pairs, ek_prob):
    
    orderings = []
    for ek in ek_pairs:
        forward = defaultdict(lambda:defaultdict(float))
        back = defaultdict(lambda: defaultdict(int))        
        n, m = len(ek[0]), len(ek[1])

        forward[0][0] = 1.0
        

        for i in xrange(n):
            epron = ek[0][i]

            for j in forward[i]:
                for k in range(1, min(m - j, 3) + 1):

                    jseg = " ".join(ek[1][j: j + k])
                    print(jseg)
                    score = forward[i][j] * ek_prob[epron][jseg]

                    if (score >= forward[i + 1][j + k]):
                        back[i + 1][j + k] = (i, j)
                        forward[i + 1][j + k] = score

        max_kata = m
        max_pron = n

        ordering = []

        while(max_pron != 0):
            print(back[max_pron][max_kata])
            new_pron, new_kata = back[max_pron][max_kata]
            
            print(max_pron)
            for i in range(max_kata - new_kata):         
                ordering.append(max_pron)

            max_kata = new_kata
            max_pron = new_pron
        
        ordering.reverse()
        print(ordering)

        orderings.append(ordering)
    return orderings
   
                


def get_ek_from_data():
    raw = sys.stdin.read().split("\n")
    del raw[2::3]
    return "\n".join(raw)[0:-1]

def main():
    ek_raw = get_ek_from_data()

    ek_pairs = generate_pairs(ek_raw)

    #print(ek_pairs)

    # e step

    ek_prob = defaultdict(lambda: defaultdict(float))

    initialize_ek_prob(ek_prob, ek_pairs)

    print_ek_probs(ek_prob)

    for it in range(int(sys.argv[1])):

        total_probs = 0

        new_ek = defaultdict(lambda: defaultdict(float))
        for ek in ek_pairs:
            legal_alignments = generate_legal_alignments(ek[0], ek[1])

            align_probs = []
            
            for align in legal_alignments:
                cur_prob = 1.0
                for pair in align:
                    cur_prob *= ek_prob[pair[0]][pair[1]]

                align_probs.append(cur_prob)
                total_probs += cur_prob

            align_sum = sum(align_probs)
            align_probs = [a / align_sum  for a in align_probs]

            for i, align in enumerate(legal_alignments):
                for pair in align:
                    new_ek[pair[0]][pair[1]] += align_probs[i]

        print("iteration %d\t----- corpus prob= %f" %(it, total_probs), file=sys.stderr)
        print_ek_probs(ek_prob)
        normalize_ek_prob(new_ek)

        nonzero = count_non_zero(ek_prob)
        print("nonzeros = %d\n" % (nonzero), file=sys.stderr)

        ek_prob = new_ek

    viterbi_decode(ek_pairs, ek_prob)

    print_probs(ek_prob)
        

if __name__ == "__main__":
    main()
