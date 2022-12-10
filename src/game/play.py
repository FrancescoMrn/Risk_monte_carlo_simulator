import random
from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class State:
    A: int # Number of attackers
    D: int # Number of defenders


@dataclass(frozen=True)
class UnitLosses:
    """
    Number of units loss during the battle
    """
    A: int
    D: int


class RiskGame(object):
    def __init__(self, state: State, die) -> None:
        self.state = state
        self.die = die

    def _random_roll(self, n: int) -> list[int]:
        """
        Roll n dice with a customizeble dimention.


        Args:
            n (_type_): _description_
            die (_type_, optional): _description_. Defaults to DIE.

        Returns:
            Dice: _description_
        """

        return [random.choice(self.die) for _ in range(n)]


    def battle_outcome(self, A_rolls_n_dice: int, D_rolls_n_dice: int) -> UnitLosses:
        """
        How many (attacker, defender) armies perish as the result of these dice?

        Args:
            A_dice (Dice): _description_
            D_dice (Dice): _description_

        Returns:
            _type_: _description_
        """
        A_dice = self._random_roll(A_rolls_n_dice)
        D_dice = self._random_roll(D_rolls_n_dice)
        #print(sorted(A_dice, reverse=True))
        #print(sorted(D_dice, reverse=True))
        dead = Counter('D' if a > d else 'A' for a, d in zip(sorted(A_dice, reverse=True), sorted(D_dice, reverse=True)))
        return UnitLosses(dead['A'], dead['D'])

    def update(self, state: State, dead: UnitLosses) -> State:
        """
        Update the `state` of a campaign to reflect the`dead` in a battle.
        
        Args:
            state (State): _description_
            dead (UnitLosses): _description_

        Returns:
            State: _description_
        """       
        a = state.A - dead.A  # Attackers remaining
        d = state.D - dead.D  # First territory defenders remaining
        return State(a, d)      

    def check_game_status(self, state: State) -> bool: 
        """Is the game over?"""
        return state.D == 0 or state.A <= 1
