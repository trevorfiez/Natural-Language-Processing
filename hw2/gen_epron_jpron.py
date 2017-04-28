


import sys


def main():

	f = open('epron-jpron.probs', 'r')

	sys.stdout.write('0\n')

	cur_state = 1

	for line in f:
		first_split = line.split(" : ")
		second_split = first_split[1].split(' # ')
		pho = first_split[0]
		kata_sequence = second_split[0].split()
		prob = float(second_split[1])

		sys.stdout.write('(0 (%d %s %s %.2f))\n' % (cur_state, pho, kata_sequence[0], prob))
		cur_state += 1

		for p in kata_sequence[1:]:
			sys.stdout.write('(%d (%d *e* %s 1.0))\n' % (cur_state - 1, cur_state, p))
			cur_state += 1

		sys.stdout.write("(%d (0 *e* *e*))\n" % (cur_state - 1))
			


		


if __name__ == "__main__":
	main()
