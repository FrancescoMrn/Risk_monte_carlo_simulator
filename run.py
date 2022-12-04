#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main script to run the simulaion of Risk (board game)
"""
from src.game.play import RiskGame, State
from src.simulation.mc import MCSimulation


# Parameters
# define the die 
DIE  = (1, 2, 3, 4, 5, 6)

if __name__ == "__main__":
    start = State(A=8, D=4)
    risk = RiskGame(state=start, die=DIE)
    mcsim = MCSimulation(state=start, riskgame=risk, runs=1000)
    simout = mcsim.simulate_multiple_attack(normalization=True)
    print(mcsim.attacker_win_prob(simout))