from collections import defaultdict
import sys

def load_jprobs(path):
    epron_pairs = defaultdict(list)
    with open(path, "r") as f:
        for line in f:
            first_part = line.split(":")
            eng_pron = first_part[0].strip()
            second_part = first_part[1].split("#")

            jprons = second_part[0].split()

            prob = float(second_part[1].strip())

            epron_pairs[eng_pron].append([jprons, prob])

    return epron_pairs

def load_eprobs(path):

    eprobs = defaultdict(lambda: defaultdict(float))

    with open(path, "r") as f:
        for line in f:
            first_part = line.split(":")

            tags = first_part[0].split()

            state = tags[0] + " " + tags[1]

            second_part = first_part[1].split("#")

            output_tag = second_part[0].strip()

            next_state = tags[1] + " " + output_tag

            prob = float(second_part[1].strip())

            eprobs[state][next_state] = prob

    return eprobs


def decode_top_k(kata, ej_probs, eprobs, states_possible, p_states, state_probs, start_state, state_to_phoneme, final_states, k=1):

    best = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: -1.0)))
    back = defaultdict(lambda: defaultdict(dict))
    
    best[0][start_state][0] = 1.0

    for i, letter in enumerate(kata.split() + ["*e*"], 1):
        #going through every state that is possible given the observed output
        #print(i)
        for pos_state in states_possible[letter]:
            top_states = []
            #only checking previous states that are possible
            for prev in best[i - 1]:
                for j in best[i - 1][prev]:
                #print(prev)
                #checking to see if the current state could have come from the previous one
                #print(prev)

                    if pos_state in p_states[prev]:
                   
                        score = best[i - 1][prev][j] * state_probs[pos_state] * p_states[prev][pos_state]
                        if (len(top_states) < k):
                            top_states.append((score, prev, j))
                            top_states.sort(reverse=True)
                        elif(score > top_states[-1][0]):
                            top_states.pop()
                            top_states.append((score, prev, j))
                            top_states.sort(reverse=True)

            if (len(top_states) > k):
                print("What the hell")
            for j in range(len(top_states)):            
                best[i][pos_state][j] = top_states[j][0]
                back[i][pos_state][j] = (top_states[j][1], top_states[j][2])



    max_scores = []
    output_steps = len(kata.split()) + 1
    #output_steps = 2
    for f in best[output_steps]:

        if (f not in final_states):
            continue

        for j in best[output_steps][f]:
            score = best[output_steps][f][j]
        #print("%f %d" % (score, state))
            if (len(max_scores) < k):
                max_scores.append((score, f, j))
                max_scores.sort(reverse=True)
            elif (score > max_scores[-1][0]):
                max_scores.pop()
                max_scores.append((score, f, j))
                max_scores.sort(reverse=True)


    #print(max_score)
    #print(max_state)

    for j in range(len(max_scores)):
        max_states = [max_scores[j][1]]

        prev_state = max_scores[j][1]
        prev_k = max_scores[j][2]
        for i in range(output_steps, 0, -1):
            max_states.append(back[i][prev_state][prev_k][0])
            cur_state = prev_state
            prev_state = back[i][prev_state][prev_k][0]
            prev_k = back[i][cur_state][prev_k][1]

        final_string = []
        for state in reversed(max_states):
            if state in state_to_phoneme:
                final_string.append(state_to_phoneme[state])

        fmt_string = " ".join(final_string[1:])
        sys.stdout.write("%s # %.6e\n" % (fmt_string, max_scores[j][0]))
    return

def create_base_tables(ej_probs, eprobs):
    input_states = defaultdict(list)

    output_states = defaultdict(list)


    #keeps track of what states each letter can actually go to
    #for example the letter I cannot belong to the state that corresponds to HH so we should not check that
    #state when we are computing viterbi
    #not actually necessary but should make it faster
    states_possible = defaultdict(list)

    #keeps track of P(w | t) basically probability letter correspond to the given english phoneme
    state_probs = {}

    p_states = defaultdict(lambda: defaultdict(float))

    p_count = 0
    cur_state = 0
    start_state = 0
    #going over every phenome pair

    for eprob in eprobs:
        #tags = eprobs.split()

        starting_states = []
        prev_states = []

        #going over each phenome

        non_null_tags = []
        for x in eprob.split():
            if x not in ["<s>", "</s>"]:
                non_null_tags.append(x)

        if (len(non_null_tags) == 0):
            output_states[eprob] = [cur_state]
            state_probs[cur_state] = 1.0
            start_state = cur_state
            cur_state += 1
            continue


        for j, tag in enumerate(eprob.split()[-1:]):
            next_states = []

            #going over how each phenome can be generated from katakana
            for j_spell in ej_probs[tag]:
                #print(j_spell)
                for i in range(len(j_spell[0])):

                    if (i == 0):
                        if (j == 0):
                            #if start of phoneme and first phonem then it can be an input state
                            starting_states.append(cur_state)
                        else:
                            for p in prev_states:
                                p_states[cur_state][p] = 1.0

                        state_probs[cur_state] = j_spell[1]


                    else:
                        state_probs[cur_state] = 1.0
                        #if phoneme corresponds to only one tag then the previous state must be
                        #the only one possible
                        p_states[cur_state - 1][cur_state] = 1.0

                    if (i == len(j_spell[0]) - 1):
                        next_states.append(cur_state)


                    states_possible[j_spell[0][i]].append(cur_state)

                    cur_state += 1

                prev_states = next_states

        input_states[eprob] = starting_states
        output_states[eprob] = prev_states


    state_to_phoneme = {}

    final_states = []

    for eprob in eprobs:


        for next_state in eprobs[eprob]:


            if ("</s>" in next_state and next_state not in input_states):
                states_possible["*e*"].append(cur_state)
                state_probs[cur_state] = 1.0
                input_states[next_state].append(cur_state)
                final_states.append(cur_state)
                cur_state += 1



            for n in input_states[next_state]:
                for p in output_states[eprob]:

                    p_states[p][n] = eprobs[eprob][next_state]

                    state_to_phoneme[p] = eprob.split()[-1]


    return states_possible, p_states, state_probs, start_state, state_to_phoneme, final_states

def decode_katakana(kata, ej_probs, eprobs, states_possible, p_states, state_probs, start_state, state_to_phoneme, final_states):

    best = defaultdict(lambda: defaultdict(lambda: -1.0))
    back = defaultdict(dict)
    best[0][start_state] = 1.0


    for i, letter in enumerate(kata.split() + ["*e*"], 1):
        #going through every state that is possible given the observed output
        #print(i)
        for pos_state in states_possible[letter]:

            #only checking previous states that are possible
            for prev in best[i - 1]:
                #print(prev)
                #checking to see if the current state could have come from the previous one
                #print(prev)

                if pos_state in p_states[prev]:
                    
                    score = best[i - 1][prev] * state_probs[pos_state] * p_states[prev][pos_state]
                    if (score > best[i][pos_state]):
                        best[i][pos_state] = score
                        back[i][pos_state] = prev



    max_score = -1
    max_state = 0
    output_steps = len(kata.split()) + 1
    #output_steps = 2
    for f in best[output_steps]:

        if (f not in final_states):
            continue

        score = best[output_steps][f]
        #print("%f %d" % (score, state))
        if (score > max_score):
            max_score = score
            max_state = f


    #print(max_score)
    #print(max_state)

    max_states = [max_state]

    prev_state = max_state
    for i in range(output_steps, 0, -1):
        max_states.append(back[i][prev_state])
        prev_state = back[i][prev_state]

    final_string = []
    for state in reversed(max_states):
        if state in state_to_phoneme:
            final_string.append(state_to_phoneme[state])

    fmt_string = " ".join(final_string[1:])
    #print(final_string[1:])
    #print(fmt_string)
    sys.stdout.write("%s # %.6f" % (fmt_string, max_score))
    return


def main():
    eprobs = load_eprobs(sys.argv[1])
    ej_probs = load_jprobs(sys.argv[2])
    states_possible, p_states, state_probs, start_state, state_to_phoneme, final_states = create_base_tables(ej_probs, eprobs)

    for line in sys.stdin:
        #decode_katakana(line, ej_probs, eprobs, states_possible, p_states, state_probs, start_state, state_to_phoneme, final_states)
        decode_top_k(line, ej_probs, eprobs, states_possible, p_states, state_probs, start_state, state_to_phoneme, final_states, 10)


if __name__ == "__main__":

    main()
