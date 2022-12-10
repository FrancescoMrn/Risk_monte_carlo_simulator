#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to explore the best global strategy to play Risk (board game). 
"""
import logging
from src.simulation.mc import risk_delta_simulator
from src.visualization.plots import plot_delta_sensitivity

# initiliaze logger 
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

# Parameters
# define the die 
DIE  = (1, 2, 3, 4, 5, 6) # define the die 
RANGE_DEFENDERS = 65 # max number of defenders to be condidered
DELTA = (10, 8, 5, 2, 1, 0, -1, -2, -5, -8, -10) # numerical delta (+/-) of the attacker

if __name__ == "__main__":
    logger.info("Running attacker delta simulation. Hold on...")
    simout = risk_delta_simulator(sim_delta=DELTA, max_defenders=RANGE_DEFENDERS, die=DIE, mc_runs=1000)
    plot_delta_sensitivity(simout)