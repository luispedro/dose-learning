import numpy as np
from collections import namedtuple

N = 450_000_000
VD = 1_000_000
DAYS_TO_P1 = 11
N2 = 20

IFR = 0.01
INF0 = 100_000
INF_RATE = INF0/N

Events = namedtuple('Events', ['unvacinated', 'protected1', 'protected2'])

class Population:
    def __init__(self, total):
        self.vaccinated0 = total
        self.vaccinated1 = np.array([])
        self.vaccinated2 = 0

    def vaccinate(self, v1, v2):

        self.vaccinated1 = np.concatenate([[0], self.vaccinated1])

        assert v1 <= self.vaccinated0
        assert v2 <= self.ready_for_2()

        self.vaccinated0 -= v1
        self.vaccinated1[0] = v1
        while v2 > 0:
            v = min(v2, self.vaccinated1[-1])
            v2 -= v
            self.vaccinated1[-1] -= v
            self.vaccinated2 += v
            if self.vaccinated1[-1] == 0:
                self.vaccinated1 = self.vaccinated1[:-1]

    def ready_for_2(self):
        return self.vaccinated1[N2:].sum()
    
    def fully_protected(self):
        return self.vaccinated0 <= 0 and self.ready_for_2() <= 0

    def sus0(self):
        return self.vaccinated0 + self.vaccinated1[:DAYS_TO_P1].sum()

    def sus1(self):
        return self.vaccinated1[DAYS_TO_P1:].sum()

    def deaths(self, p1, p2):
        return Events(IFR * INF_RATE * self.sus0(),
                IFR * INF_RATE * self.sus1() * (1 - p1),
                IFR * INF_RATE * self.vaccinated2 * (1 - p2))

def simulate(strategy, p1, p2):
    pop = Population(N)
    deaths = []
    while not pop.fully_protected():
        deaths.append(pop.deaths(p1, p2))

        strategy.observe(pop, deaths[-1])
        v2 = strategy.v2(VD, pop)
        assert v2 <= VD
        pop.vaccinate(VD - v2, v2)
    return np.array(deaths)


