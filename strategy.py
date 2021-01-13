def first(vd, vaccinated0):
    return vd - min(vd, vaccinated0)

def second(vd, pop):
    return min(vd, pop.ready_for_2())

class StrictlyFirst:
    def v2(self, vd, pop):
        return first(vd, pop.vaccinated0)
    def observe(self, _, __):
        pass
    def name(self):
        return 'Strictly first'

class StrictlySecond:
    def v2(self, vd, pop):
        return second(vd, pop)
    def observe(self, _, __):
        pass
    def name(self):
        return 'Strictly second'



class StartFirstLearnFullInformation:
    def __init__(self):
        self.N0 = 0
        self.I0 = 0
        self.N1 = 0
        self.I1 = 0

    def v2(self, vd, pop):
        if self.I1 > 100:
            est_p1 = 1.0 - (self.I1/self.N1)/ (self.I0/self.N0)
            if est_p1 > 0.95 / 2:
                return first(vd, pop.vaccinated0)
            # Ooops! We need to switch:
            return second(vd, pop)
        return first(vd, pop.vaccinated0)

    def observe(self, pop, events):
        self.N0 += pop.sus0()
        self.I0 += events[0]

        self.N1 += pop.sus1()
        self.I1 += events[1]

    def name(self):
        return 'Optimal learning'


def weak_observe(n):
    import numpy as np
    return np.random.binomial(n, .1)

class StartFirstLearnWeak:
    def __init__(self):
        self.N0 = 0
        self.I0 = 0
        self.N1 = 0
        self.I1 = 0
        self.switch_to_2nd = None

    def v2(self, vd, pop):
        if self.switch_to_2nd is not None:
            if self.switch_to_2nd == 0:
                return second(vd, pop)
            self.switch_to_2nd -= 1
            return first(vd, pop.vaccinated0)

        if self.I1 > 100:
            est_p1 = 1.0 - (self.I1/self.N1)/ (self.I0/self.N0)
            # If it turns out that the first-dose-first strategy is bad:
            if est_p1 < 0.95 / 2:
                self.switch_to_2nd = 7
        return first(vd, pop.vaccinated0)

    def observe(self, pop, events):
        self.N0 += pop.sus0()
        self.I0 += weak_observe(events[0])

        self.N1 += pop.sus1()
        self.I1 += weak_observe(events[1])

    def name(self):
        return 'Weak learning'
