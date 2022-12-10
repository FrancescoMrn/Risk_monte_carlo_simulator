#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main script to run the simulaion of Risk (board game) attack campaign 
"""
import logging
from src.game.play import RiskGame, State
from src.simulation.mc import MCSimulation
from src.visualization.plots import plot_hist_probability

# initiliaze logger 
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

# Parameters
# define the die 
DIE  = (1, 2, 3, 4, 5, 6)

if __name__ == "__main__":
    start = State(A=6, D=4)
    logger.info(f"Initial conditions: {start}")
    risk = RiskGame(state=start, die=DIE)
    logger.info("Run simulation...")
    mcsim = MCSimulation(state=start, riskgame=risk, runs=1000)
    simout = mcsim.simulate_multiple_attack(normalization=True)
    plot_hist_probability(simout, start)
    results = mcsim.attacker_win_prob(simout)
    logger.info(f"Aggregated probability of win is: {results.p_win}")
    logger.info(f"Uncertainty range (±3sigma): {results.p_win_low, results.p_win_high}")
