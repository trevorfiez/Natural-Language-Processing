import sys
import os
from collections import Counter

def main():
    # change the os environment to wherever the hw data directory is
    vocab = open('{0}/vocab'.format(os.environ['HW1DATA']), 'r').read().lower().split(' \n')
    corpus = sys.stdin.read().lower().split()

    counts = Counter(corpus)

    freq = dict(zip(vocab, [1] * len(vocab)))

    for word in vocab:
        if word in counts:
            freq[word] = counts[word]
        sys.stdout.write('{0},{1} \n'.format(word.upper(), freq[word]))

if __name__ == "__main__":
    main()
