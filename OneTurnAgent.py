import Pokemon
import Move
import Effects

class Agent:
    def get_percepts(self):
        pass
    def choose_turn(self):
        pass


class OneTurnAgent(Agent):
    def __init__(self, current_pokemon: Pokemon.Pokemon, inventory, opponent):
        self.inventory = inventory
        self.opponent = opponent
        self.current_pokemon = current_pokemon

    def get_max_harm_move(self, pokemon=None):
        '''
        Returns what move will inflict the maximum amount of damage to the enemy, given what we currently know
        :return: A pair with the move to play
        '''
        if pokemon is not None:
            for move in pokemon.moveList:

        # First, let's search all the moves for the current pokemon

