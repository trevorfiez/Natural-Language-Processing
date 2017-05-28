import sys

pair_dict = {}

#pairs = sys.stdin.split("\n")
pairs = "W AY N\nW A I N\n".split("\n")

for i in range(0, len(pairs) - 1, 2):
	pair_dict[pairs[i]] = pairs[i + 1]

prob_table = {}

for pair in pair_dict.items():
	e_syllables = pair[0].split(" ")

	for e_syl in e_syllables:
		if e_syl not in prob_table:
			prob_table[e_syl] = {}

for pair in pair_dict.items():
	e_syllables = pair[0].split(" ")
	j_syllables = pair[1].split(" ")

	for i, e_syl in enumerate(e_syllables):
		if i < len(j_syllables):
			prob_table[e_syl][j_syllables[i]] = 1
			if i > 0:
				prob_table[e_syl][j_syllables[i-1] + " " + j_syllables[i]] = 1
				prob_table[e_syl][j_syllables[i-1]] = 1
			if i < len(j_syllables) - 1:
				prob_table[e_syl][j_syllables[i] + " " + j_syllables[i+1]] = 1
				prob_table[e_syl][j_syllables[i+1]] = 1


for e_pair in prob_table.items():
	e_key = e_pair[0]
	uniform = 1/len(prob_table[e_key])
	for j_pair in prob_table[e_key].items():
		j_key = j_pair[0]
		prob_table[e_key][j_key] = uniform

print(prob_table)
#for pair in pair_dict:
	

	
