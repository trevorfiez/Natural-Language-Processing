




from collections import defaultdict

def load_jprobs():
	epron_pairs = []
	with open("hw3-data/epron-jpron.probs", "r") as f:
		for line in f:
			first_part = line.split(":")
			eng_pron = first_part[0].strip()
			second_part = first_part[1].split("#")

			jprons = second_part[0].split()

			prob = float(second_part[1].strip())

			epron_pairs.append([eng_pron, jprons, prob])

	return epron_pairs
			

def decode_katakana(kata):
	ej_probs = load_jprobs()

	beginning_tags = []

	end_tags = []

	#keeps track of what states each letter can actually go to
	#for example the letter I cannot belong to the state that corresponds to HH so we should not check that
	#state when we are computing viterbi
	#not actually necessary but should make it faster
	states_possible = {}

	#keep track to only check states that have completed a katakana sound
	completed_phonemes = []

	#keep track of which states can begin a phoneme
	starting_phonemes = []

	state_to_phoneme = {}

	cur_state = 0
	for ej in ej_probs:
		states = []
		for j in range(len(ej[1])):
			
			#checking to see if
			if (ej[1][j] not in states_possible):
				states_possible[ej[1][j]] = []

			if (j == len(ej[1]) - 1):
				completed_phonemes.append(cur_state)
				state_to_phoneme[cur_state] = ej[0]

			if (j == 0):
				starting_phonemes.append(cur_state)

			states_possible[ej[1][j]].append(cur_state)
			states.append(cur_state)

			cur_state += 1
		ej.append(states)

	print(len(completed_phonemes))

	#dict to keep track of possible states we previously had

	p_states = {}
	state_probs = {}
	for ej in ej_probs:
		for j in range(len(ej[1])):
			if (j == 0):
				p_states[ej[3][j]] = completed_phonemes
				#probability p(letter | phoneme)
				#eventually include p(phoneme)
				state_probs[ej[3][j]] = ej[2]
			else:
				p_states[ej[3][j]] = [ej[3][j - 1]]
				#in the middle of a phoneme to katakana transition so probabilty is just 1
				#an example of this is IY to I I
				state_probs[ej[3][j]] = 1.0

	
	
	print(cur_state)
	#for ej in ej_probs:
		
		

	print(ej_probs[-1])
	print(p_states[273])
	print(p_states[274])

	letters = kata.split()
	
	best = defaultdict(lambda: defaultdict(float))
	back = defaultdict(dict)

	for l_state in states_possible[letters[0]]:
		if (l_state in starting_phonemes):
			score = state_probs[l_state]
			best[0][l_state] = score
			back[0][l_state] = 0

	for i, letter in enumerate(letters[1:], 1):
		#going through every state that is possible given the observed output
		#print(i)
		for pos_state in states_possible[letter]:
			#only checking previous states that are possible
			for prev in best[i - 1]:
				#print(prev)
				#checking to see if the current state could have come from the previous one
				if prev in p_states[pos_state]:
					score = best[i - 1][prev] * state_probs[pos_state]
					if (score > best[i][pos_state]):
						best[i][pos_state] = score
						back[i][pos_state] = prev
	

	max_end_score = 0.0
	max_end_state = 0
	
	for state in best[len(letters) - 1]:
		if (state not in completed_phonemes):
			continue
		score = best[len(letters) - 1][state]
		#print("%f %d" % (score, state))
		if (score > max_end_score):
			max_end_score = score
			max_end_state = state

	max_states = [max_end_state]

	prev_state = max_end_state
	for i in range(len(letters) - 1, 0, -1):
		max_states.append(back[i][prev_state])
		prev_state = back[i][prev_state]

	final_string = []
	for state in reversed(max_states):
		if state in state_to_phoneme:
			final_string.append(state_to_phoneme[state])

	print(final_string)

	print(max_end_score)
	print(max_end_state)




def main():
	decode_katakana("N A I T O")

if __name__ == "__main__":

	main()
