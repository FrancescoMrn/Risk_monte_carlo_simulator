import numpy as np
import pandas as pd
import logging
import matplotlib.pyplot as plt
from collections import Counter

from src.game.play import State
from src.simulation.mc import AttackerDeltaSimulation

# initiliaze logger 
logger = logging.getLogger(__name__)

# import style
plt.style.library['seaborn-v0_8-dark']


def plot_hist_probability(simout: Counter, state: State, save_root: str="plots") -> None:
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
    save_path = f"{save_root}/campain_units.png"
    fig.savefig(save_path, dpi=fig.dpi)
    logger.info(f"-- Plot saved at the following path: {save_path}")

def plot_delta_sensitivity(simpout_delta: list[AttackerDeltaSimulation], save_root: str="plots"):
    fig = plt.figure(figsize=(10, 7))
    for sim in simpout_delta:
        plt.plot(sim.n_defenders, sim.p_win_high_history, marker="o", label=f'delta={sim.delta:2}')
        plt.title('Attacker with delta(±) units than the Defender')
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.xlabel('Number of units of the defender [Units]')
        plt.ylabel('Probability of win of the attacker')
        plt.grid()
    save_path = f"{save_root}/risk_global_strategy.png"
    fig.savefig(save_path, dpi=fig.dpi, bbox_inches="tight")
    logger.info(f"-- Plot saved at the following path: {save_path}")
