import logging
import numpy as np
import pandas as pd
from collections import Counter
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from src.game.play import State
from src.simulation.mc import AttackerDeltaSimulation, DefenseImprovement

# initiliaze logger 
logger = logging.getLogger(__name__)

# import style
plt.style.use('seaborn-v0_8-deep')

def plot_histogram_probability(simout: Counter, state: State, save_root: str="plots", save_fig: bool=True) -> Figure:
    """
    Histogram plot of the probabilty for Attacker and Defender
    """
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

    fig = plt.figure(figsize=(11, 7))
    plt.bar(w_attacker["attacker"]+0.15, w_attacker["probability"], width=0.3, alpha=1, label="Attacker", color = "#C44E52")
    plt.bar(w_defender["defender"]-0.15, w_defender["probability"], width=0.3, alpha=1, label="Defender", color = "#4C72B0")
    plt.legend()
    plt.title(f'Win probability and remaining units\n Initial {state}')
    plt.xlabel('Number of units remaning after the campaign [Units]')
    plt.ylabel('Probability of win')
    plt.grid()
    
    if save_fig:
        save_path = f"{save_root}/risk_status_simulation.png"
        fig.savefig(save_path, dpi=fig.dpi, bbox_inches="tight")
        logger.info(f" -- Plot saved at the following path: {save_path}")
    else:
        return fig


def plot_defence_improvements(simout_defender: list[DefenseImprovement], state: State, marginal_gain: list, save_root: str="plots",  save_fig: bool=True) -> Figure:
    """
    Plot reporting the marginal improvement of the defence.
    """
    fig = plt.figure(figsize=(11, 7))
    for index, sim in enumerate(simout_defender):
        if index==0:
            plt.bar(sim.n_defenders, sim.p_win, color="#4C72B0")
            plt.scatter(sim.n_defenders, None, color="#DD8452", marker="o", s=45, label="Marginal improvement")
            plt.grid()
        else:
            plt.bar(sim.n_defenders, sim.p_win, color="#4C72B0")
            plt.scatter(sim.n_defenders, marginal_gain[index, 0], color="#DD8452", marker="o", s=45)
        plt.title(f'Defender probability of win for incremental number of units\n Initial {state}')
        plt.legend()
        plt.xlabel('Number of units of the Defender [Units]')
        plt.ylabel('Probability of win of the defender')
    
    if save_fig:
        save_path = f"{save_root}/risk_defender_strategy.png"
        fig.savefig(save_path, dpi=fig.dpi, bbox_inches="tight")
        logger.info(f" -- Plot saved at the following path: {save_path}")
    else:
        return fig


def plot_delta_sensitivity(simpout_delta: list[AttackerDeltaSimulation], save_root: str="plots"):
    """

    """
    fig = plt.figure(figsize=(10, 7))
    for sim in simpout_delta:
        plt.plot(sim.n_defenders, sim.p_win_history, marker="o", label=f'delta={sim.delta:2}')
        plt.title('Attacker with delta(±) units than the Defender')
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.xlabel('Number of units of the defender [Units]')
        plt.ylabel('Probability of win of the attacker')
        plt.grid()
    plt.axhline(y = 0.5, color = 'r', linestyle = '-.')
    plt.xlim(left=3)
    save_path = f"{save_root}/risk_attacker_strategy.png"
    fig.savefig(save_path, dpi=fig.dpi, bbox_inches="tight")
    logger.info(f" -- Plot saved at the following path: {save_path}")
