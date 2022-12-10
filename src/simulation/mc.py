import numpy as np
import logging
from collections import Counter
from dataclasses import dataclass
from src.game.play import State, RiskGame

# initiliaze logger 
logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SimoutResults:
    p_win: float # Winning probability
    p_win_low: float # Winning probability low boundary (+3sigma)
    p_win_high: float # Winning probability high boundary (-3sigma)


@dataclass(frozen=True)
class AttackerDeltaSimulation:
    delta: int
    n_defenders: list[int]
    p_win_history: list[float] # Winning probability of the attacker
    p_win_low_history: list[float] # Winning probability of the attacker low boundary (+3sigma)
    p_win_high_history: list[float] # Winning probability of the attacker high boundary (-3sigma)


@dataclass(frozen=True)
class DefenseImprovement:
    n_defenders: int
    p_win: float # Winning probability of the defender 
    p_win_low: float # Winning probability low boundary (+3sigma)
    p_win_high: float # Winning probability high boundary (-3sigma)


class MCSimulation(object):
    def __init__(self, riskgame: RiskGame, runs: int=1) -> None:
        self.riskgame = riskgame
        self.runs = runs

    def simulate_single_attack(self, state: State) -> State:
        """
        Simulate a single attack campaign with random rolls and returs the final state.

        Args:
            state (_type_): _description
            riskgame (RiskGame): _description_

        Returns:
            State: _description_
        """
    
        while not self.riskgame.check_game_status(state):
            dead  = self.riskgame.battle_outcome(
                A_rolls_n_dice=(min(3, state.A - 1)),
                D_rolls_n_dice=(min(2, state.D))
                )
            
            state = self.riskgame.update(state, dead)
        return state

    def simulate_multiple_attack(self, state: State, normalization: bool=True) -> Counter | list:
        simulate_game_p = [] 
        for _ in range(self.runs):
            simulate_game_p.append(self.simulate_single_attack(state))
        if normalization:
            simulate_game_p = Counter(list(simulate_game_p))
            for k in simulate_game_p: simulate_game_p[k] /= self.runs
        
        return simulate_game_p

    def simulate_defense_improvement(self, n_defenders: int, n_attacker: int, max_defenders: int) -> list[DefenseImprovement]:
        defense_probability = []
        for n_defenders in range(n_defenders, max_defenders + 1):
            prob_distribution = []
            state = State(A=n_attacker, D=n_defenders)
            for _ in range(self.runs):
                prob_distribution.append(self.simulate_single_attack(state))
            prob_distribution = Counter(list(prob_distribution))
            for k in prob_distribution: prob_distribution[k] /= self.runs
            p_win_defender =  self.pwin_probability(prob_distribution, entity="defender")
            defense_probability.append(
                DefenseImprovement(
                    n_defenders,
                    p_win_defender.p_win, 
                    p_win_defender.p_win_low,
                    p_win_defender.p_win_low
                    )
                )

        return defense_probability

    def pwin_probability(self, prob_distribution: Counter, entity="attacker") -> SimoutResults:
        if entity=="attacker":
            p_win = sum(prob_distribution[s] for s in prob_distribution if not s.D)
        elif entity=="defender":
            p_win = sum(prob_distribution[s] for s in prob_distribution if s.A <= s.D)
        else:
            raise ValueError("Entity not reconize select between: attacker or defender")
        # using the expected value of the binomial variable it is possible to calculate the standard deviation
        expected_value = np.sqrt(p_win*(1-p_win)/self.runs)
        return SimoutResults(np.round(p_win, 3), np.clip(np.round(p_win-3*expected_value, 3), 0, 1), np.clip(np.round(p_win+3*expected_value, 3), 0, 1))


def attacker_delta_simulator(sim_delta: tuple, max_defenders: int, die: tuple=(1, 2, 3, 4, 5, 6), mc_runs: int = 1000) -> list[AttackerDeltaSimulation]:
    simout_delta = []
    for delta in sim_delta:
        logger.info(f" -- Simulation delta: {delta:2}")
        p_win = []
        p_win_low = []
        p_win_high = []

        for n_defender in range(1, max_defenders+1):
            n_attacker = max(2, n_defender+delta)
            state = State(A=n_attacker, D=n_defender)
            risk = RiskGame(die=die)
            mcsim = MCSimulation(riskgame=risk, runs=mc_runs)
            simout = mcsim.simulate_multiple_attack(state, normalization=True)
            results = mcsim.pwin_probability(simout, entity="attacker")
            p_win.append(results.p_win)
            p_win_low.append(results.p_win_low)
            p_win_high.append(results.p_win_high)
        
        simout_delta.append(AttackerDeltaSimulation(delta, list(range(1, max_defenders+1)), p_win, p_win_low, p_win_high))
    
    return simout_delta
