def viterbi(obs, states, start, trans, emit):
    now = {}
    for state in states:
        now[state] = (start[state], [state], start[state])
    for ob in obs:
        next = {}
        for next_state in states:
            total = 0
            path_max = None
            val_max = 0
            for state in states:
                (base, path, rate) = now[state]
                p = trans[state][next_state] * emit[state][ob]
                total += base * p
                rate = rate * p
                if rate > val_max:
                    path_max = path + [next_state]
                    val_max = rate
            next[next_state] = (total, path_max, val_max)
        now = next
    total = 0
    path_max = None
    val_max = 0
    for state in states:
        (base, path, rate) = now[state]
        total += base
        if rate > val_max:
            path_max = path
            val_max = rate
    return (total, path_max, val_max)


obs = ['Walk', 'Shop', 'Clean']
states = ['Sunny', 'Rainy']
start = {'Rainy': 0.6, 'Sunny': 0.4}
trans = {'Rainy': {'Rainy': 0.7, 'Sunny': 0.3}, 'Sunny': {'Rainy': 0.4, 'Sunny': 0.6}}
emit = {'Rainy': {'Walk': 0.1, 'Shop': 0.4, 'Clean': 0.5}, 'Sunny': {'Walk': 0.6, 'Shop': 0.3, 'Clean': 0.1}}
print(viterbi(obs, states, start, trans, emit))
