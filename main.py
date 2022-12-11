#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main script to run the simulaion of Risk (board game) attack campaign 
"""
import logging
from src.game.play import RiskGame, State
from src.simulation.mc import MCSimulation
from src.visualization.plots import plot_histogram_probability, plot_defence_improvements

# initiliaze logger 
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

# Parameters
DIE  = (1, 2, 3, 4, 5, 6) # define the die 

if __name__ == "__main__":
    # Set the initial state of the simulation
    state = State(A=10, D=10)
    logger.info(f"Initial conditions: {state}")

    # Set up the game and the MC Simulation
    risk = RiskGame(die=DIE)
    mcsim = MCSimulation(riskgame=risk, runs=1000)

    # Attacker MC Simulation
    logger.info("Run simulation to estimate the attacker position...")
    simout_attacker = mcsim.simulate_multiple_attack(state=state, normalization=True)
    plot_histogram_probability(simout_attacker, state)
    attacker_pwin = mcsim.pwin_probability(simout_attacker)
    logger.info(f"Cumulative probability of attacker win is: {attacker_pwin.p_win}")
    logger.info(f"Binomial Distr. Std (±3sigma): {attacker_pwin.p_win_low, attacker_pwin.p_win_high}")

    # Defender MC Simulation
    logger.info("Run simulation to estimate the defender position...")
    simout_defender = mcsim.simulate_defense_improvement(n_defenders = state.D, n_attacker = state.A, max_defenders = max(state.A * 2, state.D + 5))
    defender_additional_units, marginal_gain = mcsim.marginal_defence_improvement(simout_defender)
    plot_defence_improvements(simout_defender, state, marginal_gain, save_fig=True)
