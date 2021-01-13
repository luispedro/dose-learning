from jug import TaskGenerator
import numpy as np

import strategy
from simulate import simulate
simulate = TaskGenerator(simulate)
P2 = 0.95
P1 = np.linspace(0, 1, 101)
STRATEGIES = [
        strategy.StrictlyFirst,
        strategy.StrictlySecond,
        strategy.StartFirstLearnFullInformation,
        ]

@TaskGenerator
def plot_results(results):
    import seaborn as sns
    from matplotlib import pyplot as plt
    fig,ax = plt.subplots()
    lines = set(k[0] for k in results)
    for k in lines:
        line = np.array([results[k, p1].sum() for p1 in P1])
        ax.plot(P1, line/1000., label=k, lw=2, alpha=.6)
    ax.set_xlabel('Protection with 1 dose')
    ax.set_ylabel('Total number of deaths (1,000s)')
    ax.legend(loc='best')
    sns.despine(fig, trim=True)
    fig.tight_layout()
    fig.savefig('compare.png', dpi=150)

results = {}
for p1 in P1:
    for s in STRATEGIES:
        results[s().name(), p1] = simulate(s(), p1, P2)

plot_results(results)
