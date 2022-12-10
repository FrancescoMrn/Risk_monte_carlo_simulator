import numpy as np
import logging
from collections import Counter
from dataclasses import dataclass
from src.game.play import State, RiskGame

# initiliaze logger 
logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class Results:
    p_win: float # Winning probability
    p_win_low: float # Winning probability low boundary (+3sigma)
    p_win_high: float # Winning probability high boundary (-3sigma)

class MCSimulation(object):
    def __init__(self, state: State, riskgame: RiskGame, runs: int=1) -> None:
        self.state = state
        self.riskgame = riskgame
        self.runs = runs

    def simulate_single_attack(self) -> State:
        """
        Simulate a single attack campaign with random rolls and returs the final state.

        Args:
            state (_type_): _description
            riskgame (RiskGame): _description_

        Returns:
            State: _description_
        """
        simout_state = self.state
        while not self.riskgame.check_game_status(simout_state):
            dead  = self.riskgame.battle_outcome(
                A_rolls_n_dice=(min(3, simout_state.A - 1)),
                D_rolls_n_dice=(min(2, simout_state.D))
                )
            
            simout_state = self.riskgame.update(simout_state, dead)
        return simout_state

    def simulate_multiple_attack(self, normalization: bool=True) -> Counter | list:
        prob_distribution = [] 
        for _ in range(self.runs):
            prob_distribution.append(self.simulate_single_attack())
        if normalization:
            prob_distribution = Counter(list(prob_distribution))
            for k in prob_distribution: prob_distribution[k] /= self.runs
        
        return prob_distribution

    def attacker_win_prob(self, prob_distribution: Counter) -> Results:
        p_win = np.round(sum(prob_distribution[s] for s in prob_distribution if not s.D), 5)
        # using the expected value of the binomial variable it is possible to calculate the standard deviation
        expected_value = np.sqrt(p_win*(1-p_win)/self.runs)
        return Results(np.round(p_win, 3), np.clip(np.round(p_win-3*expected_value, 3), 0, 1), np.clip(np.round(p_win+3*expected_value, 3), 0, 1))

@dataclass(frozen=True)
class AttackerDeltaSimulation:
    delta: int
    n_defenders: list[int]
    p_win_history: list[float] # Winning probability
    p_win_low_history: list[float] # Winning probability low boundary (+3sigma)
    p_win_high_history: list[float] # Winning probability high boundary (-3sigma)



def risk_delta_simulator(sim_delta: tuple, max_defenders: int, die: tuple=(1, 2, 3, 4, 5, 6), mc_runs: int = 1000) -> list:
    simout_delta = []
    for delta in sim_delta:
        logger.info(f"-- Simulation delta: {delta:2}")
        p_win = []
        p_win_low = []
        p_win_high = []

        for n_defender in range(1, max_defenders+1):
            n_attacker = max(2, n_defender+delta)
            start = State(A=n_attacker, D=n_defender)
            risk = RiskGame(state=start, die=die)
            mcsim = MCSimulation(state=start, riskgame=risk, runs=mc_runs)
            simout = mcsim.simulate_multiple_attack(normalization=True)
            results = mcsim.attacker_win_prob(simout)
            p_win.append(results.p_win)
            p_win_low.append(results.p_win_low)
            p_win_high.append(results.p_win_high)
        
        simout_delta.append(AttackerDeltaSimulation(delta, list(range(1, max_defenders+1)), p_win, p_win_low, p_win_high))
    
    return simout_delta
