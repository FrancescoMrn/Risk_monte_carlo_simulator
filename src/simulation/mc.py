from typing import List, Iterable, Tuple, Union
from collections import Counter
import numpy as np
from src.game.play import State, RiskGame


class MCSimulation(object):
    def __init__(self, state, riskgame: RiskGame, runs: int=1) -> None:
        self.state = state
        self.riskgame = riskgame
        self.runs = runs

    def simulate_single_attack(self) -> State:
        """
        Simulate a single attack campaign with random rolls and returs the final state.

        Args:
            state (_type_): _description_
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

    def simulate_multiple_attack(self, normalization=True) -> Union[Counter, List]:
        prob_distribution = [] 
        for _ in range(self.runs):
            prob_distribution.append(self.simulate_single_attack())
        if normalization:
            prob_distribution = Counter(list(prob_distribution))
            for k in prob_distribution: prob_distribution[k] /= self.runs
        
        return prob_distribution

    def attacker_win_prob(self, prob_distribution: Counter) -> Tuple:
        p_win = np.round(sum(prob_distribution[s] for s in prob_distribution if not s.D), 5)
        # using the expected value of the binomial variable it is possible to calculate the standard deviation
        expected_value = np.round(np.sqrt(p_win*(1-p_win)/self.runs), 5)
        return (p_win, p_win-3*expected_value, p_win+3*expected_value)