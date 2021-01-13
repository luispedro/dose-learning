from jug import TaskGenerator
import numpy as np

import strategy
from simulate import simulate
simulate = TaskGenerator(simulate)
P2 = 0.95
P1 = np.linspace(0, 1, 100)

@TaskGenerator
def plot_results(results):
    import seaborn as sns
    from matplotlib import pyplot as plt
    fig,ax = plt.subplots()
    first = np.array([results['strictly-first', p1].sum() for p1 in P1])
    second = np.array([results['strictly-second', p1].sum() for p1 in P1])
    ax.plot(np.linspace(0, 1, 100), first/1000., label='strictly first')
    ax.plot(np.linspace(0, 1, 100), second/1000, label='strictly second')
    ax.set_xlabel('protection with 1 dose')
    ax.set_ylabel('Total number of deaths (1,000s)')
    sns.despine(fig, trim=True)
    fig.tight_layout()
    fig.savefig('compare.png', dpi=150)

results = {}
for p1 in P1:
    for s in [strategy.StrictlyFirst(), strategy.StrictlySecond()]:
        results[s.name(), p1] = simulate(s, p1, P2)

plot_results(results)
