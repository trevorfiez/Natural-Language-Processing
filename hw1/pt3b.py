import sys
import os
import re
from collections import Counter

def main():
    # change the os environment to wherever the hw data directory is
    vocab = []
    f = open(sys.argv[1], 'r')
    
    for line in f:
        vocab.append(line.strip().replace(' ', ''))

   
    #vocab = sys.stdin.read().lower().split(' \n')
    corpus = re.findall(r'\w+', sys.stdin.read().upper())

    #print(len(corpus))
    counts = Counter(corpus)

    freq = dict(zip(vocab, [1] * len(vocab)))

    total = 0
    for word in vocab:
        if word in counts:
            freq[word] += counts[word]
            total += freq[word]
    
    for word in vocab:
        sys.stdout.write('{0},{1} \n'.format(' '.join(list(word)), freq[word] / float(total)))
	
if __name__ == "__main__":
    main()
