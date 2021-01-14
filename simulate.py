import numpy as np
from collections import namedtuple

import covid19constants

Events = namedtuple('Events', ['unvacinated', 'protected1', 'protected2'])

class Population:
    '''Vaccination in a particular population'''
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
        return self.vaccinated1[covid19constants.MIN_DAYS_TO_2ND_DOSE:].sum()
    
    def fully_protected(self):
        return self.vaccinated0 <= 0 and self.ready_for_2() <= 0

    def sus0(self):
        return self.vaccinated0 + self.vaccinated1[:covid19constants.DAYS_TO_P1].sum()

    def sus1(self):
        return self.vaccinated1[covid19constants.DAYS_TO_P1:].sum()

    def infections(self, p1, p2):
        return Events(covid19constants.INFECTION_RATE * self.sus0(),
                covid19constants.INFECTION_RATE * self.sus1() * (1 - p1),
                covid19constants.INFECTION_RATE * self.vaccinated2 * (1 - p2))

def simulate(strategy, p1, p2):
    '''Simulate a population until everyone is vaccinated'''
    pop = Population(covid19constants.SIZE_OF_POPULATION)
    infections = []
    while not pop.fully_protected():
        infections.append(pop.infections(p1, p2))

        strategy.observe(pop, infections[-1])
        v2 = strategy.v2(covid19constants.DOSES_PER_DAY, pop)
        assert v2 <= covid19constants.DOSES_PER_DAY
        pop.vaccinate(covid19constants.DOSES_PER_DAY - v2, v2)
    return np.array(infections)


