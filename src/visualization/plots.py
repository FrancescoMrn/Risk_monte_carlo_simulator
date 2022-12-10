import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from src.game.play import State

# import style
plt.style.library['seaborn-dark']


def hist_probability(simout: Counter, state: State) -> None:
    records = []
    for ele in simout:
        entry = {
            "attacker": ele.A,
            "defender": ele.D,
            "probability": simout[ele]
            }
        records.append(entry)
    data = pd.DataFrame(records)

    w_attacker = data[data["defender"]==0]
    w_defender = data[data["attacker"]==1]



    fig = plt.figure(figsize=(8, 7))
    ax = plt.bar(w_attacker["attacker"]+0.15, w_attacker["probability"], width=0.3, alpha=0.8, label="Attacker")
    ax = plt.bar(w_defender["defender"]-0.15, w_defender["probability"], width=0.3, alpha=0.8, label="Defender")
    plt.legend()
    plt.title(f'Attacker and Defenders Win Probability\n Initial Conditions: {state}')
    plt.xlabel('Number of units remaning after the campaign [Units]')
    plt.ylabel('Probability of win')
    plt.grid()
    fig.savefig('plots/campain_units.png', dpi=fig.dpi)
    #plt.show()
