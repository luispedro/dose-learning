import numpy as np
N = 450_000_000
VD = 1_000_000

class StrictlySecond:
    def v2(self, vd, state):
        available = state[-2]
        return min(available, vd)


class StrictlyFirst:
    def v2(self, vd, state):
        missing = N - state.sum()
        return max(0, vd - missing)

def simulate(strategy, p1, p2):
    P = []
    Vstate = np.zeros(shape=22)
    while Vstate[-1] < N:
        Vstate = np.concatenate([[0], Vstate[:-3], [Vstate[-2]+Vstate[-3], Vstate[-1]]])
        ready_for_2 = Vstate[-2]
        protection = p2 * Vstate[-1] + p1 * Vstate[12:-1].sum()
        P.append(protection)
        v2 = strategy.v2(VD, Vstate)
        Vstate[-1] += v2
        Vstate[-2] -= v2
        Vstate[0] = VD - v2
    return np.array(P)

P1 = simulate(StrictlyFirst(), p1=.1, p2=.95)
P2 = simulate(StrictlySecond(), p1=.1, p2=.95)
print(P1.sum()/P2.sum())

(P1[:900]+1)/(1+P2[:900])
