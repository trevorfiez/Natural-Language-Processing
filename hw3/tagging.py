


from collections import defaultdict

def tag_sentence(sentence):
	best = defaultdict(lambda: defaultdict(float))

	best[0]["<s>"] = 1
	back = defaultdict(dict)

	words = sentence.split()

	tags = {"a": ["PREP"],
		"like": ["PREP", "V", "CONJ"],
		"an": ["PREP"],
		"panda": ["N"],
		"shoots": ["N", "V"],
		"leaves": ["N", "V"],
		"can": ["N", "V", "AUX"],
		"time": ["N", "V"],
		"flies": ["N", "V"],
		"arrow": ["N"],
		"eats": ["V"],
		"and": ["CONJ"],
		"they": ['PRO'],
		"</s>": ["</s>"]}

	ptag = {"<s>": {"DT": 0.4, "PRO": 0.2, "N": 0.2, "PREP": 0.1, "AUX": 0.05, "V": 0.05},
		"DT": {"N": 1.0},
		"PRO": {"V": .4, "AUX": 0.1, "CONJ": 0.15, "PREP": 0.25, "</s>": 0.1},
		"N": {"N": 0.1, "V": 0.3, "PREP": 0.1, "CONJ": 0.3, "</s>": 0.2},
		"AUX": {"V": 1.0},
		"V": {"CONJ": 0.1, "PRO": 0.1, "DT": 0.6, "N": 0.15, "PREP": 0.05, "</s>": 0.1},
		"CONJ" : {"DT": 0.4, "PRO": 0.2, "N": 0.3, "V": 0.1},
		"PREP": {"DT": 0.6, "PRO": 0.2, "N": 0.125, "V": 0.025, "</s>": 0.05}}



	pword = {"PREP": {"a": 0.05, "like": 0.01, "an": 0.2},
		"N": {"panda": 0.00001, "shoots": 0.00001, "leaves": 0.00001, "can": 0.00001, "time": 0.00001, "flies": 0.00001, "arrow": 0.00001},
		"V": {"eats": 0.00001, "shoots": 0.00001, "leaves": 0.00001, "can": 0.00001, "time": 0.00001, "flies": 0.00001, "like": 0.00001},
		"CONJ": {"and": 0.4, "like": 0.5 },
		"PRO": {"they", 0.07},
		"AUX": {'can': 0.21},
		"</s>": {'</s>': 1.0}}

	for i, word in enumerate(words[1:], 1):
		for tag in tags[word]:
			
			for prev in best[i - 1]:

				if tag in ptag[prev]:
					score = best[i - 1][prev] * ptag[prev][tag] * pword[tag][word]
					if (score > best[i][tag]):
						best[i][tag] = score
						back[i][tag] = prev

	def backtrack(i, tag):
		if (i == 0):
			return []

		return backtrack(i - 1, back[i][tag]) + [(words[i], tag)]

	print(backtrack(len(words) - 1, "</s>")[:-1])

def main():
	tag_sentence("<s> a panda eats shoots and leaves </s>")
		


if __name__ == "__main__":
	main()

