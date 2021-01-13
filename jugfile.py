from jug import TaskGenerator
import numpy as np

import strategy
from simulate import simulate
simulate = TaskGenerator(simulate)

P2 = 0.95

results = {}
for p1 in np.linspace(0, 1, 100):
    for s in [strategy.StrictlyFirst(), strategy.StrictlySecond()]:
        results[s.name(), p1] = simulate(s, p1, P2)

