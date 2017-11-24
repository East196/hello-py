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
    #         print now
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


class Emits:
    def __init__(self, count):
        self.emits = {}
        for i in range(1, count + 1):
            self.emits[str(i).zfill(2)] = {}
            for j in range(1, count + 1):
                self.emits[str(i).zfill(2)][str(j).zfill(2)] = 1.0


class Trans:
    def __init__(self, count):
        self.count = count
        self.trans = {}
        for i in range(1, count + 1):
            self.trans[str(i).zfill(2)] = {}
            for j in range(1, count + 1):
                self.trans[str(i).zfill(2)][str(j).zfill(2)] = 0.0

    def fill(self):
        lines = open("E:/lottor.txt", 'r').readlines()
        values = map(lambda line: line.split(' ')[0], lines)
        for i in range(1, self.count):
            self.trans[values[i - 1]][values[i]] += 1.0
        return self


count = 12
states = map(lambda value: str(value).zfill(2), range(1, count))
print states
lines = open("lottor.txt", 'r').readlines()
cols = map(lambda line: line.split(' ')[5], lines)
print cols
start = {}
for i in range(1, count + 1):
    start[str(i).zfill(2)] = 0.0
start[cols[0]] = 1.0 / count
print start
# for line in lines:
#     print line
trans = Trans(count).fill().trans
print trans
emit = Emits(count).emits
print emit

print viterbi(cols, states, start, trans, emit)
