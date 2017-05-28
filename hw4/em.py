
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

        print(line)

def count_non_zero(ek_probs):
    nonzero = 0
    for pron in ek_probs.keys():
        for kata in ek_probs[pron].keys():
            if (ek_probs[pron][kata] >= 0.01):
                nonzero += 1

    return nonzero

def main():
    ek_raw = sys.stdin.read()

    ek_pairs = generate_pairs(ek_raw)

    print(ek_pairs)

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

        print("iteration %d\t----- corpus prob= %f" %(it, total_probs))
        print_ek_probs(ek_prob)
        normalize_ek_prob(new_ek)

        nonzero = count_non_zero(ek_prob)
        print("nonzeros = %d\n" % (nonzero))

        ek_prob = new_ek

        

if __name__ == "__main__":
    main()
