import sys
import string

def main():
	sys.stdout.write('0\n')

	cur_state = 1
	f = open('hw2-data/eword-epron.data', 'r')

	for line in f:
		s = line.split()[0]
		sys.stdout.write('(0 (' + str(cur_state) + " *e* *e* 1.0))\n")
		cur_state += 1
		for c in s:
			sys.stdout.write('(' + str(cur_state - 1) + ' (' + str(cur_state) + ' ' + c + ' *e* 1.0))\n')
			cur_state += 1

		sys.stdout.write('(' + str(cur_state - 1) + ' (0 *e* ' + s + ' 1.0))\n')
		#cur_state += 1



if __name__ == "__main__":
	main()
