



def add_phonemes(phonemes, e_phonemes, j_kata, matching):
	
	for match in range(0, len(e_phonemes)):
		kata_list = []
		for i in range(len(j_kata)):
			if (matching[i] == match + 1):
				kata_list.append(j_kata[i])

		kata = " ".join(kata_list)
		if (e_phonemes[match] not in phonemes):
			phonemes[e_phonemes[match]] = {}

		if (kata not in phonemes[e_phonemes[match]]):
			phonemes[e_phonemes[match]][kata] = 1.0
		else:
			phonemes[e_phonemes[match]][kata] += 1.0


def main():

	f = open('hw2-data/epron-jpron.data', 'r')

	line_num = 0

	phonemes = {}

	e_phonemes = ""

	j_kata = ""

	matching = ""

	for line in f:
		if (line_num % 3 == 0):
			e_phonemes = line.split()
		elif (line_num % 3 == 1):
			j_kata = line.split()
		else:
			matching = [int(x) for x in line.split()]
			add_phonemes(phonemes, e_phonemes, j_kata, matching)

		line_num += 1

	output_


			

if __name__ == "__main__":
	main()
