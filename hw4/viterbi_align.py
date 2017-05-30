import sys
import re
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


def viterbi_decode(ek_pairs, ek_prob):
    for ek in ek_pairs:
	print(" ".join(ek[0]))
        print(" ".join(ek[1]))
	
        forward = defaultdict(lambda:defaultdict(float))
        back = defaultdict(lambda: defaultdict(int))        
        n, m = len(ek[0]), len(ek[1])

        forward[0][0] = 1.0
        

        for i in xrange(n):
            epron = ek[0][i]

            for j in forward[i]:
                for k in range(1, min(m - j, 3) + 1):

                    jseg = " ".join(ek[1][j: j + k])
                    #print(jseg)

                    if jseg in ek_prob[epron]:
                         score = forward[i][j] * ek_prob[epron][jseg]
		    else:
     			 score = 0

                    if (score >= forward[i + 1][j + k]):
                        back[i + 1][j + k] = (i, j)
                        forward[i + 1][j + k] = score

        max_kata = m
        max_pron = n

        ordering = []

        while(max_pron != 0):
            #print(back[max_pron][max_kata])
            new_pron, new_kata = back[max_pron][max_kata]
            
            #print(max_pron)
            for i in range(max_kata - new_kata):         
                ordering.append(max_pron)

            max_kata = new_kata
            max_pron = new_pron
        
        ordering.reverse()
        print(" ".join([str(ord) for ord in ordering]))


def get_ek_probs(epron_file):
    ek_probs = {}
    for line in epron_file:
        pron = line.split(" ")[0]
	kata = re.search(':(.*)#', line).group(1)[1:-1]
	prob = float(re.search('#(.*)', line).group(1)[1:-1])
	
	if pron not in ek_probs:
            ek_probs[pron] = {}

        ek_probs[pron][kata] = prob

    return ek_probs


def get_ek_from_data():
    raw = sys.stdin.read().split("\n")
    del raw[2::3]
    return "\n".join(raw)[0:-1]
    

def main():
    epron_file = open(sys.argv[1], 'r')

    ek_raw = get_ek_from_data()
    ek_pairs = generate_pairs(ek_raw)

    ek_probs = get_ek_probs(epron_file)

    viterbi_decode(ek_pairs, ek_probs)


if __name__ == "__main__":
    main()
