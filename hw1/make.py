import sys


def main():
	sys.stdout.write('F\n')

	max_state = 1

	for line in sys.stdin:

		letters = line.split()
		sys.stdout.write('(0 (%d *e* *e*))\n' % (max_state))
		max_state += 1
		for l in letters:
			sys.stdout.write('(%d (%d ' % (max_state - 1, max_state) + l + ' ' + l + '))\n' )
			max_state += 1
		sys.stdout.write('(%d (%d _ _))\n' % (max_state - 1, 0))
		sys.stdout.write('(%d (F *e* *e*))\n' % (max_state - 1))



if __name__ == "__main__":
	main()
