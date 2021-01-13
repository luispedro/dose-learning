import numpy as np
N = 450_000_000
VD = 1_000_000
N2 = 20

class StrictlySecond:
    def v2(self, vd, pop):
        available = pop.ready_for_2()
        return min(available, vd)


class StrictlyFirst:
    def v2(self, vd, pop):
        missing = pop.ready_for_1()
        return max(0, vd - missing)

class Population:
    def __init__(self, total):
        self.total = total
        self.vaccinated1 = np.array([])
        self.vaccinated2 = 0

    def next_day(self):
        self.vaccinated1 = np.concatenate([[0], self.vaccinated1])

    def vaccinate(self, v1, v2):
        self.vaccinated1[0] = v1
        while v2 > 0:
            v = max(v2, self.vaccinated1[-1])
            v2 -= v
            self.vaccinated1[-1] -= v
            self.vaccinated2 += v
            if self.vaccinated1[-1] == 0:
                self.vaccinated1 = self.vaccinated1[:-1]

    def ready_for_1(self):
        return self.total - self.vaccinated2 - self.vaccinated1.sum()

    def ready_for_2(self):
        return self.vaccinated1[N2:].sum()
    
    def fully_protected(self):
        return self.vaccinated2 == self.total

def simulate(strategy, p1, p2):
    pop = Population(N)
    P = []
    while not pop.fully_protected():
        pop.next_day()
        ready_for_2 = pop.ready_for_2()
        protection = p2 * pop.vaccinated2 + p1 * pop.vaccinated1[11:].sum()
        P.append(protection)
        v2 = strategy.v2(VD, pop)
        pop.vaccinate(VD - v2, v2)
    return np.array(P)

P1 = simulate(StrictlyFirst(), p1=.1, p2=.95)
P2 = simulate(StrictlySecond(), p1=.1, p2=.95)
print(P1.sum()/P2.sum())

