class StrictlySecond:
    def v2(self, vd, pop):
        available = pop.ready_for_2()
        return min(available, vd)
    def name(self):
        return 'strictly-second'


class StrictlyFirst:
    def v2(self, vd, pop):
        missing = pop.ready_for_1()
        return max(0, vd - missing)
    def name(self):
        return 'strictly-first'
